{{config(materialized = 'table')}} 

 
with data as (
    select
        "Index" as "index",
        "ORGANIZATIONID"  as "organizationid",
        "NAME" as "name",
        "WEBSITE" as "website",
        "COUNTRY" as "country",
        "DESCRIPTION"  as "description",
        "FOUNDED" as "founded",
        "INDUSTRY" as "industry",
        "NUMBEROFEMPLOYEES" as "numberofemployees"
    from
         dbt_staging.organisation_data
)
select
    *
from
    data