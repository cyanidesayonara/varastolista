function openModal() {
  $(".modal").fadeIn();
}
function closeModal() {
  $(".modal").fadeOut();
}
function pushState(url) {
  var main = $(".main");
  var context = main[0].innerHTML;
  var state = {
    "context": context,
    "url": url,
  };
  history.pushState(state, "", "");
}
function replaceState(url) {
  var main = $(".main");
  var context = main[0].innerHTML;
  var state = {
    "context": context,
    "url": url,
  };
  history.replaceState(state, "", "");
}

$(document)
  .ready(function() {
    replaceState(window.location.href);
  })
  .on("click", ".ajax", function(e) {
    e.preventDefault();
    var url = $(this).data("url");
    var dump = $(this).data("dump");
    if (dump == ".modal") {
      openModal();
    }
    pushState(url);
    $.ajax({
      type: "GET",
      url: url,
    })
      .fail(function(xhr, ajaxOptions, thrownError) {
        console.log(thrownError);
      })
      .done(function(response) {
        $(dump).html(response);
        replaceState(url);
      });
  })
  .on("click", ".buy", function() {
    alert("Ostettu!");
  });

$(window)
  .on("popstate", function (e) {
    var state = e.originalEvent.state;
    if (state) {
      $(".main").html(state.context);
    }
  })