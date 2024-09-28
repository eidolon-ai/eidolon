{% set description = (schema | get_description) %}
{% include "header.md" %}
{% with schema=schema, skip_headers=False, depth=-1 %}
    {% include "content.md" %}
{% endwith %}

{{ md_get_toc() }}

{{ contentBase }}

----------------------------------------------------------------------------------------------------------------------------
{% if config.with_footer -%}
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans){% if config.footer_show_time %} on {{ get_local_time() }}{% endif %}
{%- endif -%}