function openModal() {
  document.getElementById("modal").style.display = "block";
};
function closeModal() {
  let modal = document.getElementById("modal");
  modal.innerHTML = "";
  modal.style.display = "";
};
function pushState(url) {
  // return if url in urls
  const urls = ["new", "plus", "minus", "edit", "delete", "upload", "language"];
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
  const urls = ["new", "plus", "minus", "edit", "delete", "upload", "language"];
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
  let el = document.createElement("video");
  el.id = "scanner";
  document.getElementById("modal").appendChild(el);
  openModal();
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
      if (cameras[1]) {
        scanner.start(cameras[1]);
      } else {
        scanner.start(cameras[0]); 
      }
      $("#modal").click(function () {
        scanner.stop();
        closeModal();
      });
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
  .on("change", ".dropdown", function (e) {
    e.preventDefault();
    const button = $(this);
    const dump = button.data("dump");
    const form = button.parents("form");
    const url = button.data("url");
    const method = form.attr("method");
    const data = form.serialize();
    $.ajax({
      type: method,
      url: url,
      data: data,
    })
      .fail(function (xhr, ajaxOptions, thrownError) {
        console.error(thrownError);
      })
      .done(function (response) {
        $(dump).html(response);
        replaceState(url);
        if (document.getElementById("errors")) {
          openModal();
        }
      });    
  })
  .on("click", ".excel-button", function (e) {
    e.preventDefault();
    $(this).siblings(".excel-show").toggleClass("d-none");
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
        let price = form.find("[name=price]").val();
        price = price.replace(",", ".");
        form.find("[name=price]").val(price)
        data = form.serialize();
      }
    }
    else {
      pushState(url);
      method = "GET";
      data = undefined;
    }
    $.ajax({
      type: method,
      url: url,
      data: data,
    })
      .fail(function(xhr, ajaxOptions, thrownError) {
        console.error(thrownError);
      })
      .done(function(response) {
        $(dump).html(response);
        replaceState(url);
        if (document.getElementById("errors")) {
          openModal();
        }
      });
  })
  .on("click", ".new", function (e) {
    e.preventDefault();
    $("#part0")
      .toggleClass("toggled d-none")
      .siblings(".toggled")
      .removeClass("toggled")
      .find(".toggled")
      .toggleClass("d-none toggled");
    $("#empty").toggleClass("d-none");
  })
  .on("click", ".edit", function (e) {
    e.preventDefault();
    $("#part0.toggled")
      .toggleClass("toggled d-none")
    $(this)
      .parents(".tr")
      .siblings(".toggled")
      .removeClass("toggled")
      .find(".toggled")
      .toggleClass("d-none toggled");
    $(this)
      .parents(".tr")
      .toggleClass("toggled")
      .find(".toggle, .edit-toggle")
      .toggleClass("d-none toggled");
  })
  .on("click", ".remove", function (e) {
    e.preventDefault();
    $("#part0.toggled")
      .toggleClass("toggled d-none")
    $(this)
      .parents(".tr")
      .siblings(".toggled")
      .removeClass("toggled")
      .find(".toggled")
      .toggleClass("d-none toggled");
    $(this)
      .parents(".tr")
      .toggleClass("toggled")
      .find(".remove-toggle")
      .toggleClass("d-none toggled");
  })
  .on("click", "#modal", function () {
    closeModal();
  })
  .on("click", ".loader", function () {
    $(this).children().toggleClass("d-none");
  });

$(window)
  .on("popstate", function (e) {
    const state = e.originalEvent.state;
    if (state) {
      $("#main").html(state.context);
    }
  });