
$(document).ready(function () {
    var json = {{projects|safe}};
    var displayTable = document.getElementById('data-table');
    var row;

    for (var i = 0; i < json.length; i++) {

        row = $('<tr id=' + json[i].fields.name + ' />');
        var lnk = '<td><a href="'+json[i].fields.url+'">'+json[i].fields.name+'</a></td>';



        row.append(lnk);
        row.append("<td>" + Date(json[i].fields.created_datetime) + "</td>");

        $('#data-table').append(row);
    }
});
