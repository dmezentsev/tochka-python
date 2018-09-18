{% if data %}
<table>
<th>date</th>
<th>transaction_type</th>
<th>owner_type</th>
<th>shares_traded</th>
<th>last_price</th>
<th>shares_held</th>
{% for row in data %}
    <tr>
        <td>{{ row.date }}</td>
        <td>{{ row.transaction_type }}</td>
        <td>{{ row.owner_type }}</td>
        <td>{{ row.shares_traded }}</td>
        <td>{{ row.last_price }}</td>
        <td>{{ row.shares_held }}</td>
    </tr>
{% endfor %}
</table>
{% else %}
NO DATA
{% endif %}