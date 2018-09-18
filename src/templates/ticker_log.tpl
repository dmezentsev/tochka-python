{% if data %}
<table>
<th>date</th>
<th>c_open</th>
<th>c_close</th>
<th>c_low</th>
<th>c_high</th>
{% for row in data %}
    <tr>
        <td>{{ row.date }}</td>
        <td>{{ row.c_open }}</td>
        <td>{{ row.c_close }}</td>
        <td>{{ row.c_low }}</td>
        <td>{{ row.c_high }}</td>
    </tr>
{% endfor %}
</table>
{% else %}
NO DATA
{% endif %}