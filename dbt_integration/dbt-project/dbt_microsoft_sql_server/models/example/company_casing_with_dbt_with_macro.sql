{{config(materialized='table')}}


select
    name as company_name,
    {{ return_value_to_divided_by_thousand('numberofemployees') }} as company_case
from
    {{ref('temp_organisation_data')}}