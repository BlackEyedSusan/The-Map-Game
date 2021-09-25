$(document).ready(function(){
    $('#getdata-button').live('click', function(){
        $.getJSON('/json-data', {'nitems': 3}, function(data) {
            $('#showdata').html("<p>item1="+data.item1+" item2="+data.item2+" item3="+data.item3+"</p>");
        });
    });
});