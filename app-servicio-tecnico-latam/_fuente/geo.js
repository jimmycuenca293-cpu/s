(function(){
var D=window.DATOS,B=document.body,M=B.dataset.marca,NM=B.dataset.nombre,btn=document.getElementById('gps'),det=document.getElementById('det');
if(!btn||!D)return;
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function slug(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
function slugloc(c,cc){var t=slug(c);return t.indexOf(D[cc].ps)>=0?t:t+'-'+D[cc].ps;}
function cercana(la,lo){var b=null;for(var cc in D){var cs=D[cc].ciudades;for(var n in cs){var d=dist(la,lo,cs[n][0],cs[n][1]);if(!b||d<b.d)b={cc:cc,city:n,d:d};}}return b;}
function barrio(la,lo,cb){var done=false,t=setTimeout(function(){if(!done){done=true;cb(null);}},4500);
 fetch('https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=16&accept-language=es&lat='+la+'&lon='+lo).then(function(r){return r.json();}).then(function(j){if(done)return;done=true;clearTimeout(t);var a=j.address||{};cb(a.neighbourhood||a.suburb||a.quarter||a.city_district||a.village||a.town||null);}).catch(function(){if(!done){done=true;cb(null);}});}
function msg(h){det.innerHTML='<div class="ok-b">'+h+'</div>';}
function mostrar(la,lo,nb){
 var c=cercana(la,lo);if(!c||c.d>600){msg('Todavía no tenemos técnicos en tu zona.');return;}if(nb&&nb.toLowerCase()===c.city.toLowerCase())nb=null;
 fetch(B.dataset.bu+'tecnicos.json').then(function(r){return r.json();}).then(function(T){
  var best=null;T.forEach(function(t){if(t.p!==c.cc)return;var d=dist(la,lo,t.la,t.lo);if(!best||d<best.d)best={t:t,d:d};});
  var num=(best&&best.t.w)||D[c.cc].wa,txt='Hola, necesito servicio técnico '+NM+' en '+(nb?nb+', ':'')+c.city+', '+D[c.cc].n+' (https://maps.google.com/?q='+la.toFixed(5)+','+lo.toFixed(5)+')';
  var url='https://wa.me/'+num+'?text='+encodeURIComponent(txt);
  var otro=B.dataset.pais&&c.cc!==B.dataset.pais?'<br><span class="mu">Tu solicitud se enviará al técnico de '+esc(D[c.cc].n)+'.</span>':'';
  msg('<b>📍 Estás en '+esc((nb?nb+', ':'')+c.city+', '+D[c.cc].n)+'</b><br>Técnico '+esc(NM)+' más cercano: '+esc(best?best.t.n:'servicio técnico')+(best?' · a '+Math.round(best.d)+' km':'')+otro+'<p><a class="btn wa" data-evt="whatsapp" target="_blank" rel="noopener" href="'+url+'">💬 Escribir por WhatsApp</a></p>'+(B.dataset.pais&&c.cc!==B.dataset.pais?'':'<a href="/soporte-tecnico-autorizado-'+M+'-'+slugloc(c.city,c.cc)+'/">Ver servicio '+esc(NM)+' en '+esc(c.city)+'</a>'));
  var f=document.getElementById('fab');if(f)f.href=url;});}
btn.addEventListener('click',function(){
 if(!navigator.geolocation){msg('Tu navegador no permite ubicación.');return;}
 msg('Buscando tu ubicación…');
 navigator.geolocation.getCurrentPosition(function(p){var la=p.coords.latitude,lo=p.coords.longitude;msg('Buscando tu barrio…');barrio(la,lo,function(nb){mostrar(la,lo,nb);});},
  function(e){msg(e&&e.code===1?'No diste permiso de ubicación. Puedes escribirnos directo por WhatsApp.':'No pudimos obtener tu ubicación. Puedes escribirnos directo por WhatsApp.');},{timeout:12000,maximumAge:600000});});
})();
