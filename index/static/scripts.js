var _scannerIsRunning = false;
var _torchIsLit = false;

function openModal() {
  $("#modal").fadeIn();
};
function closeModal() {
  $("#modal").fadeOut();
};
function toggleModal() {
  $("#modal").toggle();
};
function pushState(url) {
  // return if url in urls
  var urls = ["new", "plus", "minus", "edit", "delete"];
  for (var i = 0; i < urls.length; i++) {
    if (url.includes(urls[i])) {
      return;
    }
  }  
  var main = $("#main");
  var context = main[0].innerHTML;
  var state = {
    "context": context,
    "url": url,
  };
  history.pushState(state, "", url);
};
function replaceState(url) {
  // return if url in urls
  var urls = ["new", "plus", "minus", "edit", "delete"];
  for (var i = 0; i < urls.length; i++) {
    if (url.includes(urls[i])) {
      return;
    }
  }  
  var main = $("#main");
  var context = main[0].innerHTML;
  var state = {
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
function startQuagga() {
  Quagga.init({
    inputStream: {
      name: "Live",
      type: "LiveStream",
      target: document.querySelector('#scanner-container'),
      constraints: {
        width: 800,
        height: 600,
        facingMode: "environment"
      },
    },
    decoder: {
      readers: [
        "ean_reader",
      ],
      debug: {
        showCanvas: true,
        showPatches: true,
        showFoundPatches: true,
        showSkeleton: true,
        showLabels: true,
        showPatchLabels: true,
        showRemainingPatchLabels: true,
        boxFromPatches: {
          showTransformed: true,
          showTransformedBox: true,
          showBB: true
        }
      }
    },

  }, function(err) {
    if (err) {
      console.log(err);
      return
    }

    console.log("Initialization finished. Ready to start");
    // Set flag to is running
    _scannerIsRunning = true;
    Quagga.start();
  });

  Quagga.onProcessed(function (result) {
    var drawingCtx = Quagga.canvas.ctx.overlay,
      drawingCanvas = Quagga.canvas.dom.overlay;

    if (result) {
      if (result.boxes) {
        drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
        result.boxes.filter(function (box) {
          return box !== result.box;
        }).forEach(function (box) {
          Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, { color: "green", lineWidth: 2 });
        });
      }

      if (result.box) {
        Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, { color: "#00F", lineWidth: 2 });
      }

      if (result.codeResult && result.codeResult.code) {
        Quagga.ImageDebug.drawPath(result.line, { x: 'x', y: 'y' }, drawingCtx, { color: 'red', lineWidth: 3 });
      }
    }
  });

  Quagga.onDetected(function (result) {
    $(".textfield").val(result.codeResult.code);
    Quagga.stop();
    $('#scanner-container').empty();
    _scannerIsRunning = false;
  });
};
function toggleTorch() {
  const video = document.querySelector('video');
  if (video) {
    const stream = video.srcObject;
    
    // get the active track of the stream
    const track = stream.getVideoTracks()[0];
    const capabilities = track.getCapabilities();

    if (capabilities.torch) {
      track.applyConstraints({
        advanced: [{ torch: true }]
      })
        .catch(e => console.log(e));
    }
  }
};

$(document)
  .ready(function() {
    replaceState(window.location.href);
  })
  .on("click", ".scanner", function() {
    $('#scanner-container').empty();
    // Start/stop scanner
    if (_scannerIsRunning) {
      Quagga.stop();
      _scannerIsRunning = false;
    } else {
      startQuagga();
    }
  })
  .on("click", ".torch", function () {
    toggleTorch();
  })
  .on("click", "#modal", function(e) {
    if (e.target != this) {
      return false;
    }
    closeModal();
  })
  .on("click", ".ajax", function(e) {
    e.preventDefault();
    var button = $(this);
    var url = button.data("url");
    var dump = button.data("dump");
    var form = button.parents("form");
    if (form.length) {
      var method = form.attr("method");
      var q = form.children(".q").val();
      if (method == "GET") {
        if (q) {
          pushState(url);
          q = cleanString(q);
          console.log(q)
          url = url + "?q=" + q;
          var data = undefined;
        } else {
          return;
        }
      } else {
        var data = form.serialize();
      }
    } else {
      pushState(url);
      var method = "GET";
      var data = undefined;
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
  });

$(window)
  .on("popstate", function (e) {
    var state = e.originalEvent.state;
    if (state) {
      $("#main").html(state.context);
    }
  });