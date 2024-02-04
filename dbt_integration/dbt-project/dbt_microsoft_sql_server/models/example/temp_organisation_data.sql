{{config(materialized = 'table')}} 



with data as (
    select
        "Index",
        "OrganizationId" as organizationid,
        "Name" as name,
        "Website" as website,
        "Country" as country,
        "Description" as description,
        "Founded" as founded,
        "Industry" as industry,
        "Numberofemployees" as numberofemployees
    from
        dbo.organisation_data
)
select
    *
from
    data