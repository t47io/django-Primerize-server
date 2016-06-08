var scrollTimer, resizeTimer;

app.fnParseLocation = function() {
  var urls = {
    "design": ["design_1d", "design_2d", "design_3d", "demo_1d", "demo_2d", "demo_3d", "result"],
    "tutorial": ["tutorial"],
    "protocol": ["protocol"],
    "about": ["about"],
    "code": ["download", "docs", "license"]
  };
  app.page = window.location.pathname.replace(/\/$/, '').replace(/^\//, '');
  for (var key in urls) {
      if (urls[key].indexOf(app.page) != -1) {
          app.key = key;
          return;
      }
  }
  app.key = 'home';
};

app.fnChangeView = function() {
    app.fnParseLocation();
    $("#nav > li.dropdown.active").removeClass("active");
    $("#nav_"+ app.key).addClass("active");

    $.getScript('/site_media/js/public/' + app.DEBUG_DIR + 'page' + app.DEBUG_STR + '.js');

    $("#content").fadeTo(150, 1);
    if (typeof this.callbackChangeView === "function") {
        this.callbackChangeView();
    }
};

app.fnChangeLocation = function() {
    if (window.history.replaceState) {
        window.history.replaceState({} , '', app.href);
    } else {
        window.location.href = app.href;
    }
    $("#content").load(app.href + " #content > *", app.fnChangeView);
};


$(document).ready(function () {
  var today = new Date();
  $("#cp_year").text(today.getFullYear());

  $(".dropdown-toggle").dropdown();
  $(".dropdown").hover(
    function(){ $(this).addClass("open"); },
    function(){ $(this).removeClass("open"); }
  );
  $("[data-toggle='popover']").popover({trigger: "hover"});
  $("[data-toggle='tooltip']").tooltip();

  $("#top").on("click", function () {
    event.preventDefault();
    $('#top > div').animate({'right':'-5%', 'opacity':'0'}, 125);
    $("html, body").stop().animate({scrollTop: 0}, 250);
  });

  $("#nav a, #nav_home").on("click", function(event) {
      event.preventDefault();
      app.href = $(this).attr("href");
      $("#content").fadeTo(100, 0, app.fnChangeLocation);
  });

  $("#navbar").css({"opacity": 1, "top": "-50px"}).animate({"top": "0px"}, {"duration": 200, "queue": false});
  app.fnChangeView();
  // $("body > div").css("opacity", 1);
  // $("#page-content-wrapper").delay(500).fadeTo(150, 1);
});


$(window).on("scroll", function () {
  clearTimeout($.data(this, 'scrollTimer'));
  $.data(this, 'scrollTimer', setTimeout(function() {
    if ($(this).scrollTop() > $(window).height() / 2) {
      $('#top > div').animate({'right':'0%', 'opacity':'1.0'}, 125);
    } else {
      $('#top > div').animate({'right':'-5%', 'opacity':'0'}, 125);
    }
  }, 200));
});


// function resize() {
//   $("#col-res-l").css("height", "auto");
//   $("#col-res-r").css("height", "auto");

//   var col_h = Math.max(parseInt($("#col-res-l").css("height")), parseInt($("#col-res-r").css("height")));
//   $("#col-res-l").css("height", col_h);
//   $("#col-res-r").css("height", col_h);
// }

// $(window).on("resize", function() {
//   clearTimeout($.data(this, 'resizeTimer'));
//   $.data(this, 'resizeTimer', setTimeout(resize, 200));
// });