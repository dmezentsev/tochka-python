{% if data %}
<ul>
{% for item in data %}
    <li><a href='/{{ item }}'>{{ item }}</a></li>
{% endfor %}
</ul>
{% else %}
NO DATA
{% endif %}