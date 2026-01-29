{%macro generate_shcema_name(custom_schema_name, node) -%}

        {%-set default_schema = target.schema -%}
        {%- if custom_schema_name is none -%}

            {{default_shcema}}
        {%- else -%}
            {{custom_schema_name | trim}}
            {%- endif -%}
    {%- endmacro %}