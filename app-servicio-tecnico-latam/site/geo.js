(function(){
var D=window.DATOS,B=document.body,M=B.dataset.marca,btn=document.getElementById('geo-btn'),msg=document.getElementById('msg'),tec=document.getElementById('tec');
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function ciudadCerca(la,lo){var b=null;for(var cc in D){var cs=D[cc].ciudades;for(var n in cs){var d=dist(la,lo,cs[n][0],cs[n][1]);if(!b||d<b.d)b={cc:cc,city:n,d:d};}}return b;}
function slug(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
function barrio(la,lo,cb){var done=false,t=setTimeout(function(){if(!done){done=true;cb(null);}},4500);
  fetch('https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=16&accept-language=es&lat='+la+'&lon='+lo).then(function(r){return r.json();}).then(function(j){if(done)return;done=true;clearTimeout(t);var a=j.address||{};cb(a.neighbourhood||a.suburb||a.quarter||a.city_district||a.village||a.town||null);}).catch(function(){if(!done){done=true;cb(null);}});}
function mostrar(la,lo,nb){
  var c=ciudadCerca(la,lo);if(!c||c.d>600){msg.textContent='Todavía no tenemos técnicos en tu zona. Elige tu país abajo.';return;}
  try{localStorage.setItem('pos',JSON.stringify([la,lo]));}catch(e){}
  msg.innerHTML='Estás en <b>'+(nb?nb+', ':'')+c.city+', '+D[c.cc].n+'</b>';
  if(!M){var h='';return;}
  fetch('/'+M+'/tecnicos.json').then(function(r){return r.json();}).then(function(T){
    var best=null;T.forEach(function(t){if(t.p!==c.cc)return;var d=dist(la,lo,t.la,t.lo);if(!best||d<best.d)best={t:t,d:d};});
    var num=best&&best.t.w||D[c.cc].wa,nombre=best?best.t.n:'Servicio técnico',zona=best?best.t.z+', '+best.t.c:D[c.cc].n;
    var txt='Hola, necesito servicio técnico '+B.dataset.nombre+(nb?' en '+nb+', ':' en ')+c.city;
    tec.style.display='block';
    tec.innerHTML='<b>Técnico más cercano</b><br>'+nombre+'<br><span class="mu">'+zona+(best?' · a '+Math.round(best.d)+' km':'')+'</span><p><a class="b" data-evt="whatsapp" target="_blank" rel="noopener" href="https://wa.me/'+num+'?text='+encodeURIComponent(txt)+'">💬 Escribir por WhatsApp</a></p><p><a href="/'+M+'/'+c.cc+'/'+slug(c.city)+'/">Ver servicio en '+c.city+'</a></p>';
    var f=document.getElementById('fab');if(f)f.href='https://wa.me/'+num+'?text='+encodeURIComponent(txt);
  });}
function pedir(){if(!navigator.geolocation){msg.textContent='Tu navegador no permite ubicación. Elige tu país abajo.';return;}
  msg.textContent='Buscando tu ubicación…';
  navigator.geolocation.getCurrentPosition(function(p){var la=p.coords.latitude,lo=p.coords.longitude;msg.textContent='Buscando tu barrio…';barrio(la,lo,function(nb){mostrar(la,lo,nb);});},
    function(e){msg.textContent=e&&e.code===1?'No diste permiso de ubicación. Elige tu país abajo.':'No pudimos obtener tu ubicación. Elige tu país abajo.';},{timeout:12000,maximumAge:600000});}
if(btn){btn.addEventListener('click',pedir);
  if(navigator.permissions&&navigator.permissions.query){navigator.permissions.query({name:'geolocation'}).then(function(s){if(s.state==='granted')pedir();}).catch(function(){});}}
})();