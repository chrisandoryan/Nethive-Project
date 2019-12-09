$(document).ready(function(){
    $.ajaxPrefilter(function( options, original_Options, jqXHR ) {
        options.async = true;
    });

    var trigger = $('.sidebar nav ul li a'),
        container = $('.content-wrapper');

    //Fire on click
    trigger.on('click',function(event){
        event.preventDefault();
        //Set $this for re-use. Set target from data attribute
        var $this = $(this)
            target = $this.attr('href');

        $(trigger).removeClass("active");
        $this.addClass("active");

        //Load target page into container
        $.ajax({
            type: 'GET',
            url: target,
            dataType: 'html',
        }).done(function(html){
            container.html(html);
        });

        return false;
    });
});