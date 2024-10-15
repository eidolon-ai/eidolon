{% set depth = 0 %}
{% include "header.md" %}

{% set contentBase %}
{% with schema=schema, skip_headers=True, depth=depth %}
    {% include "content.md" %}
{% endwith %}
{% endset %}

{{ contentBase }}

----------------------------------------------------------------------------------------------------------------------------
{% if config.with_footer -%}
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans){% if config.footer_show_time %} on {{ get_local_time() }}{% endif %}

{% endif -%}
