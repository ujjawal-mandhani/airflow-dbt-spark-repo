{{config(materialized='table')}}


select
    name as company_name,
    case
        when numberofemployees < 1000 then 0
        when numberofemployees < 2000 then 1
        when numberofemployees < 3000 then 2
        when numberofemployees < 4000 then 3
        when numberofemployees < 5000 then 4
        when numberofemployees < 6000 then 5
        when numberofemployees < 7000 then 6
        when numberofemployees < 8000 then 7
        when numberofemployees < 9000 then 8
        when numberofemployees < 9000 then 8
        when numberofemployees < 10000 then 9
    end as company_case
from
    {{ref('temp_organisation_data')}}