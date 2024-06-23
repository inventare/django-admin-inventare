document.addEventListener('DOMContentLoaded', function(){
  function openWS() {
    const ws = new WebSocket('ws://localhost:9002');
        
    ws.onclose = function() {
      setTimeout(function() { openWS() }, 1000);
    };

    ws.onmessage = function(evt) {
      const data = JSON.parse(evt.data);
      if (data.event == "reload") {
        if (window.reloadTimer) {
          clearTimeout(window.reloadTimer);
        }
        window.reloadTimer = setTimeout(function() {
          location.reload(true);
        }, 300);
      }
    };

    ws.onopen = function() {
      ws.send(JSON.stringify({
        event: 'initialize_view',
        path: window.location.pathname,
      }));
    };
  };

  openWS();
});
