var _scannerIsRunning = false;
var _torchIsLit = false;

function openModal() {
  $(".modal").fadeIn();
};
function closeModal() {
  $(".modal").fadeOut();
};
function pushState(url) {
  var main = $(".main");
  var context = main[0].innerHTML;
  var state = {
    "context": context,
    "url": url,
  };
  history.pushState(state, "", "");
};
function replaceState(url) {
  var main = $(".main");
  var context = main[0].innerHTML;
  var state = {
    "context": context,
    "url": url,
  };
  history.replaceState(state, "", "");
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

  }, function (err) {
    if (err) {
      console.log(err);
      return
    }

    console.log("Initialization finished. Ready to start");
    Quagga.start();

    // Set flag to is running
    _scannerIsRunning = true;
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
  });
};
function toggleTorch() {
  const video = document.querySelector('video');
  if (video) {
    const stream = video.srcObject;
    
    // get the active track of the stream
    const track = stream.getVideoTracks()[0];
    const capabilities = track.getCapabilities();
    alert(capabilities)
    if (capabilities.torch) {
      alert(capabilities.torch)
      track.applyConstraints({
        advanced: [{ torch: true }]
      })
        .catch(e => console.log(e));
    }
  }
}

$(document)
  .ready(function() {
    replaceState(window.location.href);
  })
  .on("click", "#btn", function() {
    // Start/stop scanner
    if (_scannerIsRunning) {
      Quagga.stop();
      $('#scanner-container').empty();
      _scannerIsRunning = false;
    } else {
      startQuagga();
    }
  })
  .on("click", "#torch", function () {
    toggleTorch();
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