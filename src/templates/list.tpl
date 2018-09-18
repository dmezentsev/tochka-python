{% if data %}
<ul>
{% for item, url in data %}
    <li><a href='{{ url }}'>{{ item }}</a></li>
{% endfor %}
</ul>
{% else %}
NO DATA
{% endif %}