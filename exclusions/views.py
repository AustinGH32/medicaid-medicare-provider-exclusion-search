from django.shortcuts import render
from django.db.models import Q
from .models import Exclusion, GeorgiaExclusion, CaliforniaExclusion

# list of all state-level models
# when you add a new state, import its model and add it here
# example: if you add California, add CaliforniaExclusion to this list
# each entry is (Model, label)
STATE_MODELS = [
    (GeorgiaExclusion, 'GA - State Level'),
    (CaliforniaExclusion, 'CA - State Level'),
]

def search(request):
    # read search parameters from the URL
    # example URL: /?q=smith&state=GA&source=national
    query  = request.GET.get('q', '').strip()
    state  = request.GET.get('state', '').strip()
    source = request.GET.get('source', '').strip()

    
    # start with all federal records from oig_exclusion table
    # we'll filter this down below based on what the user searched
    federal_qs = Exclusion.objects.all()

    # if user typed something in the search box,
    # filter federal records to match any of these fields using OR logic
    if query:
        federal_qs = federal_qs.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(business_name__icontains=query) |
            Q(npi__icontains=query) |
            Q(city__icontains=query)  # federal table has city, state tables don't
        )

    # if user selected a state from the dropdown,
    # narrow federal results to that state only
    if state:
        federal_qs = federal_qs.filter(state__iexact=state)

    # loop through every state model in STATE_MODELS
    # builds a separate queryset for each state table
    all_state_qs = []
    for StateModel, label in STATE_MODELS:
        qs = StateModel.objects.all()

        # apply the same text search to the state table
        # note: no city filter here since state tables don't have a city field
        if query:
            qs = qs.filter(
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query) |
                Q(business_name__icontains=query) |
                Q(npi__icontains=query)
            )

        # apply state filter to state table
        if state:
            qs = qs.filter(state__iexact=state)

        all_state_qs.append((qs, label))

    def find_both(federal_qs, all_state_qs):
        # finds records that appear on both the federal list and at least one state list
        # uses two matching strategies:
        # 1. NPI match — most reliable since NPI is a unique identifier
        # 2. Name match — fallback for records where NPI is missing
        both = []

        for state_qs, label in all_state_qs:
            # strategy 1: match on NPI
            # get all NPIs from the state list that aren't empty
            state_npis = set(
                state_qs.exclude(npi='').values_list('npi', flat=True)
            )
            # get all NPIs from the federal list that aren't empty
            federal_npis = set(
                federal_qs.exclude(npi='').values_list('npi', flat=True)
            )

            # find federal records whose NPI appears in the state list
            federal_npi_matches = federal_qs.filter(npi__in=state_npis)
            # find state records whose NPI appears in the federal list
            state_npi_matches   = state_qs.filter(npi__in=federal_npis)

            # strategy 2: match on last name + first name for records with no NPI
            # get all (last_name, first_name) pairs from state records that have no NPI
            state_names = set(
                state_qs.filter(npi='').values_list('last_name', 'first_name')
            )
            # get all last names and first names from federal records with no NPI
            federal_last_names  = set(
                federal_qs.filter(npi='').values_list('last_name', flat=True)
            )
            federal_first_names = set(
                federal_qs.filter(npi='').values_list('first_name', flat=True)
            )

            # find federal records with no NPI whose name appears in the state list
            federal_name_matches = federal_qs.filter(npi='').filter(
                Q(last_name__in=[n[0] for n in state_names]) &
                Q(first_name__in=[n[1] for n in state_names])
            )
            # find state records with no NPI whose name appears in the federal list
            state_name_matches = state_qs.filter(npi='').filter(
                Q(last_name__in=federal_last_names) &
                Q(first_name__in=federal_first_names)
            )

            # combine all matches into the both list
            # label each record with its source so the template knows which table it came from
            both.extend([{'source': 'Both Lists', 'record': r} for r in federal_npi_matches])
            both.extend([{'source': label, 'record': r} for r in state_npi_matches])
            both.extend([{'source': 'Both Lists', 'record': r} for r in federal_name_matches])
            both.extend([{'source': label, 'record': r} for r in state_name_matches])

        return both

    # build the final results list based on which source filter was selected
    if source == 'national':
        # show only federal records
        results = [{'source': 'National', 'record': r} for r in federal_qs[:100]]

    elif source == 'state':
        # show only state records, combining all state tables into one list
        results = []
        for qs, label in all_state_qs:
            results.extend([{'source': label, 'record': r} for r in qs[:100]])

    elif source == 'both':
        both_results = find_both(federal_qs, all_state_qs)
        # remove duplicates by tracking record id AND model type
        # we need model type because federal and georgia records can have the same id number
        seen = set()
        results = []
        for r in both_results:
            key = (r['record'].__class__.__name__, r['record'].id)
            if key not in seen:
                seen.add(key)
                results.append(r)
        results = results[:100]
       
    else:
        # no source filter selected — show everything from all tables
        results = [{'source': 'National', 'record': r} for r in federal_qs[:100]]
        for qs, label in all_state_qs:
            results.extend([{'source': label, 'record': r} for r in qs[:100]])

    return render(request, 'exclusions/search.html', {
        'results': results,   # the filtered records to display in the table
        'query': query,       # keeps the search box filled in after searching
        'state': state,       # keeps the state dropdown selected after searching
        'source': source,     # keeps the source dropdown selected after searching
    })