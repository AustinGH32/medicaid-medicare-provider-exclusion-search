from django.shortcuts import render
from django.db.models import Q
from .models import MainExclusion

def search(request):
    # read search parameters from the URL
    # example URL: /?q=smith&state=GA&source=Medicare
    name_query = request.GET.get('name', '').strip()
    npi_query  = request.GET.get('npi', '').strip()
    state      = request.GET.get('state', '').strip()
    source     = request.GET.get('source', '').strip()

    # start with all records from main_exclusion table
    # this single table contains all federal, Georgia, and California records
    results = MainExclusion.objects.all()

    # if user typed something in the search box,
    # filter results to match any of these fields using OR logic
    if name_query:
        results = results.filter(
            Q(last_name__icontains=name_query) |
            Q(first_name__icontains=name_query) |
            Q(business_name__icontains=name_query) |
            Q(city__icontains=name_query)
        )

    # filter by NPI if user typed in the NPI search box
    if npi_query:
        results = results.filter(npi__icontains=npi_query)
    
    # if user selected a state from the dropdown,
    # narrow results to that state only
    if state:
        results = results.filter(state__iexact=state)

    # if user selected a source from the dropdown,
    # filter by source label
    # 'both' is a special case - finds records whose NPI appears in multiple sources
    if source == 'both':
        from django.db.models import Count
        both_npis = (
            MainExclusion.objects
            .exclude(npi='')
            .values('npi')
            .annotate(source_count=Count('source', distinct=True))
            .filter(source_count__gt=1)
            .values_list('npi', flat=True)
        )
        results = results.filter(npi__in=both_npis)
        npi_to_sources = {}
        for npi in both_npis:
            sources = (
                MainExclusion.objects
                .filter(npi=npi)
                .values_list('source', flat=True)
                .distinct()
            )
            npi_to_sources[npi] = ' & '.join(sorted(set(sources)))
        results = list(results.order_by('last_name', 'first_name')[:100])
        for result in results:
            result.combined_source = npi_to_sources.get(result.npi, result.source)
    elif source:
        # filter by exact source label for all non-both sources
        results = results.filter(source=source)
        results = results.order_by('last_name', 'first_name')[:100]
    else:
        # no source filter - show everything
        results = results.order_by('last_name', 'first_name')[:100]
    return render(request, 'exclusions/search.html', {
        'results': results,
        'name_query': name_query,
        'npi_query': npi_query,
        'state': state,
        'source': source,
    })