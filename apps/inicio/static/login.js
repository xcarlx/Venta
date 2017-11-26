$( document ).ready(function() {
    $.post( "{% url  %}", { 'choices[]': [ "Jon", "Susan" ] } );
}