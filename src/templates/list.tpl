<table>
{% for item, url in data %}
    <li><a href='{{ url }}'>{{ item }}</a></li>
{% endfor %}
</table>