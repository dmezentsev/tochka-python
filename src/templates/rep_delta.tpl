{% if data %}
<table>
<th>from</th>
<th>to</th>
{% for row in data %}
    <tr>
        <td>{{ row.date }}</td>
        <td>{{ row.todate }}</td>
    </tr>
{% endfor %}
</table>
{% else %}
NO DATA
{% endif %}