from rest_framework import serializers
from .models import Exclusion


# Converts sql row into json objects for the web API.

# exclude instead of fields — instead of listing every field we want, we list the only one we don't want. 
# search_vector contains raw PostgreSQL tsvector data that would look like gibberish in JSON so we hide it.
# read_only_fields — created_at and updated_at are included in the response but can never be 
# changed through the API since Django manages them automatically.
# We also added is_individual and is_reinstated here since this is the full detail view — 
# someone looking at a single record wants all the information.

class ExclusionListSerializer(serializers.ModelSerializer):
    full_name            = serializers.ReadOnlyField()
    exclusion_type_label = serializers.ReadOnlyField()

    class Meta:
        model = Exclusion
        fields = [
            'id', 'full_name', 'last_name', 'first_name', 'business_name',
            'npi', 'general', 'specialty',
            'city', 'state', 'zip_code',
            'exclusion_type', 'exclusion_date', 'reinstatement_date',
        ]
    