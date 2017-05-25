$(document).ready(function() {
  $(".select2").select2().on('change',function() {
    data = $('#searchForm').serialize();
    url = $('#searchForm').attr('action');
    $("#resultados").load(url + '?' + data);
  });

    var $nav = $(".navbar-fixed-top");
    function navbarScroll(){
        $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
    }
    navbarScroll();
    $(document).scroll(navbarScroll);

});



//google analytics
/*(function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
e=o.createElement(i);r=o.getElementsByTagName(i)[0];
e.src='//www.google-analytics.com/analytics.js';
r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
ga('create','UA-XXXXX-X','auto');ga('send','pageview');*/
