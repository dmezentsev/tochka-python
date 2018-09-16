<table>
{% for row in data %}
    <tr>
        {% for item in row %}
            <td>{{ item }}</td>
        {% endfor %}
    </tr>
{% endfor %}
</table>