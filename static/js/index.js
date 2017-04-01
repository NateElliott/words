



function getData(){

    var dataTable = document.getElementById('data-table');


    $.get('/list/all', function(data){

        for(var i=0;i<data.length;i++){


            var updated = new Date(data[i].data.updated);
            var now = Date.now();

            var since = Math.round(((now-updated)/1000)/60);


            row = $('<tr id="' + data[i].pid + '">');

            var link = '<td><a href="/edit/'+ data[i].pid +'">'+ data[i].data.name +'</a></td>';
            var hash = '<td><code>'+ data[i].data.hash +'</code></td>';
            var update = '<td>'+ since +'</td>';



        row.append(link+hash+update);


        $('#data-table').append(row);

        }
    });
}

$(document).ready(function(){
    getData();
});









