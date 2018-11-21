function openModal(el, id) {
  el = document.createElement(el);
  el.id = id;
  let modal = document.getElementById("modal");
  modal.appendChild(el);
  modal.style.display = "block";
};
function closeModal() {
  let modal = document.getElementById("modal");
  modal.innerHTML = "";
  modal.style.display = "";
};
function pushState(url) {
  // return if url in urls
  const urls = ["new", "plus", "minus", "edit", "delete"];
  for (let i = 0; i < urls.length; i++) {
    if (url.includes(urls[i])) {
      return;
    }
  }  
  const main = $("#main");
  const context = main[0].innerHTML;
  const state = {
    "context": context,
    "url": url,
  };
  history.pushState(state, "", url);
};
function replaceState(url) {
  // return if url in urls
  const urls = ["new", "plus", "minus", "edit", "delete"];
  for (let i = 0; i < urls.length; i++) {
    if (url.includes(urls[i])) {
      return;
    }
  }  
  const main = $("#main");
  const context = main[0].innerHTML;
  const state = {
    "context": context,
    "url": url,
  };
  history.replaceState(state, "", url);
};
// replaces spaces/&s with +, removes unwanted chars
function cleanString(q) {
  q = q.replace(/&+/g, "+");
  q = q.replace(/\s+/g, "+");
  q = q.replace(/([^a-zA-Z0-9\u0080-\uFFFF +']+)/gi, "");
  return q.toLowerCase();
};
function initScanner() {
  openModal("video", "scanner");
  let scanner = new Instascan.Scanner({
    video: document.getElementById("scanner")
  });
  scanner.addListener("scan", function (content) {
    $("#q").val(content);
    scanner.stop();
    closeModal();
  });
  Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
      scanner.start(cameras[0]);
      $("#modal").click(function () {
        scanner.stop();
        closeModal();
      })
    } else {
      console.error("No cameras found.");
      closeModal();
    }
  }).catch(function (e) {
    console.error(e);
    closeModal();
  });
};

$(document)
  .ready(function() {
    replaceState(window.location.href);
  })
  .on("click", "#scanneron", function (e) {
    e.preventDefault();
    initScanner();
  })
  .on("click", ".ajax", function (e) {
    e.preventDefault();
    const button = $(this);
    const dump = button.data("dump");
    const form = button.parents("form");
    let url = button.data("url");
    let method;
    let data;
    if (form.length) {
      console.log(form.attr("method"))
      method = form.attr("method");
      let q = form.children("#q").val();
      if (method == "GET") {
        if (q) {
          pushState(url);
          q = cleanString(q);
          url = url + "?q=" + q;
          data = undefined;
        } else {
          return;
        }
      } else {
        data = form.serialize();
      }
    }
    else {
      pushState(url);
      method = "GET";
      data = undefined;
    }
    if (dump == "#modal") {
      openModal();
    }
    $.ajax({
      type: method,
      url: url,
      data: data,
    })
      .fail(function(xhr, ajaxOptions, thrownError) {
        console.log(thrownError);
      })
      .done(function(response) {
        $(dump).html(response);
        replaceState(url);
      });
  })
  .on("click", ".edit", function (e) {
    e.preventDefault();
    let row = $(this).parents(".tr");
    row.addClass("toggled")
      .find(".toggle")
      .toggleClass("d-none");
    row.siblings(".toggled")
      .removeClass("toggled")
      .find(".toggle")
      .toggleClass("d-none");
  });

$(window)
  .on("popstate", function (e) {
    const state = e.originalEvent.state;
    if (state) {
      $("#main").html(state.context);
    }
  });