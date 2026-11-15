// Open a collapsed artifact when a link targets it, and expand every artifact for printing.
(function(){
  function openTarget(){
    var id=decodeURIComponent((location.hash||"").slice(1)); if(!id) return;
    var el=document.getElementById(id); if(!el) return;
    for(var n=el;n;n=n.parentElement){ if(n.tagName==="DETAILS") n.open=true; }
    el.scrollIntoView();
  }
  window.addEventListener("hashchange",openTarget);
  document.addEventListener("DOMContentLoaded",openTarget);
  window.addEventListener("beforeprint",function(){
    document.querySelectorAll("details.artifact").forEach(function(d){ d.dataset.wasOpen=d.open?"1":""; d.open=true; });
  });
  window.addEventListener("afterprint",function(){
    document.querySelectorAll("details.artifact").forEach(function(d){ d.open=d.dataset.wasOpen==="1"; });
  });
})();
