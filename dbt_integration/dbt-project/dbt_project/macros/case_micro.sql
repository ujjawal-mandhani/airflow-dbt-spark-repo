{% macro return_value_to_divided_by_thousand(numeric_value) %}
    case
        when {{numeric_value}} < 1000 then 0
        when {{numeric_value}} < 2000 then 1
        when {{numeric_value}} < 3000 then 2
        when {{numeric_value}} < 4000 then 3
        when {{numeric_value}} < 5000 then 4
        when {{numeric_value}} < 6000 then 5
        when {{numeric_value}} < 7000 then 6
        when {{numeric_value}} < 8000 then 7
        when {{numeric_value}} < 9000 then 8
        when {{numeric_value}} < 9000 then 8
        when {{numeric_value}} < 10000 then 9
    end
{% endmacro %}