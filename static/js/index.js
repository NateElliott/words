 $(document).ready(function(){
    var cheese = setTimeout(getData, 50);
});

function getData(){
    $.ajax({
        type: "GET",
        url: '/list/all',
        success: function(data){
            buildDataTable(data);
        }
    });
}

function buildDataTable(data) {

    var dataTable = document.getElementById('data-table');
    for(i=0;i<data.length;i++){

        var row = $('<tr id="' + data[i].pid + '"></tr>');
        var link = '<td><a href="/edit/'+ data[i].pid +'">'+ data[i].data.name +'</a></td>';
        var hash = '<td><code>'+ data[i].data.hash +'</code></td>';
        var update = '<td><p class="text-right">'+ timeSince(data[i].data.updated) +'</p></td>';

        row.append(link+hash+update);
        $('#data-table').append(row);
    }
}

function timeSince(d){

    var updated = new Date(d);
    var now = Date.now();
    var since = Math.floor((now-updated)/1000);

    var times = [
        [60, 'sec'],
        [3600, 'min'],
        [86400, 'hour'],
        [604800, 'day'],
        [4233600, 'week'],
        [16934400, 'month'],
        [203212800, 'year']
    ]


    if (since < 60) {
        return since + ' sec';
    } else if (since > 60 && since < 3600) {
        return Math.floor(since/60) + ' min';
    } else if (since > 3600 && since < 86400) {
        return Math.floor(since/60/60) + ' hr';
    } else if (since > 86400 && since < 604800) {
        return Math.floor(since/60/60/24) + ' day';
    } else if (since > 604800 && since < 4233600) {
        return Math.floor(since/60/60/24/7) + ' wk';
    } else if (since > 4233600 && since < 220147200) {
        return Math.floor(since/60/60/24/7/52) + ' yr';
    } else {
        return since;
    }
}
