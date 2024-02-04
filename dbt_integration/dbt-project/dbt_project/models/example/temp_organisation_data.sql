{{config(materialized = 'table')}} 



with data as (
    select
        "Index" as index,
        "OrganizationId" as organizationid,
        "Name" as name,
        "Website" as website,
        "Country" as country,
        "Description" as description,
        "Founded" as founded,
        "Industry" as industry,
        "Numberofemployees" as numberofemployees
    from
        dbt_transformed.organisation_data
)
select
    *
from
    data