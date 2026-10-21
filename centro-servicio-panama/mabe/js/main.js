(function(){
  window.dataLayer=window.dataLayer||[];
  document.addEventListener("click",function(e){var a=e.target.closest('a[href*="wa.me/"],a[href^="tel:"]');if(a){dataLayer.push({event:"whatsapp",ubicacion:a.getAttribute("data-wa")||"enlace",boton:(a.textContent||"").trim().slice(0,60),pagina:location.pathname})}},true);
  var b=document.querySelector(".burger"),m=document.querySelector(".mov");
  if(b&&m){b.addEventListener("click",function(){var o=m.hidden;m.hidden=!o;b.setAttribute("aria-expanded",String(o))})}
  var tabs=document.querySelectorAll(".tab");
  tabs.forEach(function(t){t.addEventListener("click",function(){tabs.forEach(function(x){x.classList.remove("on")});t.classList.add("on");var f=t.getAttribute("data-f");document.querySelectorAll(".dg").forEach(function(c){c.hidden=(f!=="todos"&&c.getAttribute("data-eq")!==f)})})});
})();