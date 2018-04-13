
(function( $ ) {

    function loadResults(resultsContainer, url){
        if (url == null || url == '' || url.startsWith('#')){
            return;
        }
        resultsContainer.addClass('loading-container');
        $.get(url, {}, function(data){
            resultsContainer.find('.results').html(data);
            resultsContainer.removeClass('loading-container');
            loadVotes(resultsContainer);
            resultsContainer.find('[data-toggle="tooltip"]').tooltip();
            var preserveHistory = resultsContainer.attr('data-preservehistory');
            if (!preserveHistory || preserveHistory != 'true')
                window.history.replaceState({}, '', url);
        });
    }

    $.fn.ajaxLoader = function( url ) {

        if ( url != null) {
            loadResults(this, url);
            return this;
        }
        var initialUrl = this.attr('data-initial');
        if ((initialUrl != null) && (initialUrl!='')){
            loadResults(this, initialUrl);
        }

        var self = this;
        self.on('click', '.pagination a', function(e){
            e.preventDefault();
            if ($(this).parent().hasClass('active'))
                return;
            var url = $(this).attr('href')
            loadResults(self, url);
        });

        return this;

    };
}( jQuery ));


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function loadVotes(elem){
    elem.find('.jury-vote input[type="radio"]').on('change', function(){
        var voteUrl = $(this).parents('.jury-vote').attr('data-vote')
        var vote = $(this).val();
        $.post(voteUrl, { 'vote':vote })
        console.log("AAAA");
   });
}

$(document).ready(function() {

    var searchForm = $('#searchForm');
    var url = searchForm.attr('action');
    var results = $("#results")

 /* $(".select2").on('change',function() {
    data = searchForm.serialize();
    results.load(url + '?' + data);
  });
*/
  $('#filter').on('click', function(e){
    e.preventDefault();
    data = searchForm.serialize();
    results.load(url + '?' + data);
  });

  $('#viewall').on('click', function(e){
    e.preventDefault();
    searchForm[0].reset();
    data = searchForm.serialize();
    results.load(url + '?' + data);
  });

    var $nav = $(".navbar-fixed-top");
    function navbarScroll(){
        $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.find('.navbar-header').height());
    }
    navbarScroll();
    $(document).scroll(navbarScroll);

    function formatTag (tag) {
      return tag;
    };

    $('a.smoothscroll').on('click', function(event) {
      var $anchor = $(this);
      $('html, body').stop().animate({
          scrollTop: $($anchor.attr('href')).offset().top
      }, 900);
      event.preventDefault();
  });


  $(".image-field").each(function(){
        var field = $(this);
        var target = field.attr('data-ref');
        var type = field.attr('data-ref-type');
        field.find('input').on('change', function(){
            var input = this;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    if (type == 'image'){
                        $(target).attr('src', e.target.result);
                    }
                    else{
                        $(target).css('background-image', 'url(' + e.target.result + ')');
                    }
                }
                reader.readAsDataURL(input.files[0]);
            }
        });
    });

   $(".linked-value").each(function(){
        var field = $(this);
        var target = field.attr('data-ref');
        field.on('change', function(){

            $(target).text(field.val());
        });
    });

    loadVotes($('body'));

});





