(function(){
var D=window.DATOS,O=window.ORDEN,B=document.body,root=document.getElementById('orden');if(!root||!D||!O)return;
var M=B.dataset.marca,NM=B.dataset.nombre,S={pais:B.dataset.pais||'',ciudad:'',barrio:'',lat:null,lon:null,equipo:B.dataset.equipo||'',falla:B.dataset.falla||'',tec:null};
try{var sv=JSON.parse(localStorage.getItem('ord')||'{}');S.nombre=sv.nombre||'';if(!S.pais&&sv.pais)S.pais=sv.pais;if(sv.ciudad)S.ciudad=sv.ciudad;}catch(e){}
var PASOS=['Ubicación','Equipo','Falla','Datos'],paso=0,tecs=null;
function $(s,r){return (r||root).querySelector(s);}
function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function slug(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');}
function cap(s){return s.charAt(0).toUpperCase()+s.slice(1);}
function termino(k){var v=(D[S.pais]||{}).voc;return v?v[k]:O.equipos[k].t;}
function cercana(la,lo){var b=null;for(var cc in D){var cs=D[cc].ciudades;for(var n in cs){var d=dist(la,lo,cs[n][0],cs[n][1]);if(!b||d<b.d)b={cc:cc,city:n,d:d};}}return b;}
function barrio(la,lo,cb){var done=false,t=setTimeout(function(){if(!done){done=true;cb(null);}},4500);
 fetch('https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=16&accept-language=es&lat='+la+'&lon='+lo).then(function(r){return r.json();}).then(function(j){if(done)return;done=true;clearTimeout(t);var a=j.address||{};cb(a.neighbourhood||a.suburb||a.quarter||a.city_district||a.village||a.town||null);}).catch(function(){if(!done){done=true;cb(null);}});}
function cargarTecs(cb){if(tecs)return cb(tecs);fetch((window.BASE?window.BASE.replace(/\/$/,'')+B.dataset.bu:B.dataset.bu)+'tecnicos.json').then(function(r){return r.json();}).then(function(t){tecs=t;cb(t);}).catch(function(){tecs=[];cb([]);});}
function elegirTec(cb){cargarTecs(function(T){var best=null;T.forEach(function(t){if(t.p!==S.pais)return;var d=S.lat!=null?dist(S.lat,S.lon,t.la,t.lo):(t.c===S.ciudad?0:99999);if(!best||d<best.d)best={t:t,d:d};});S.tec=best?best.t:null;S.dkm=best&&S.lat!=null?Math.round(best.d):null;var f=document.getElementById('fab');if(f&&D[S.pais])f.href='https://wa.me/'+numero()+'?text='+encodeURIComponent('Hola, necesito servicio técnico '+NM+' en '+D[S.pais].n);cb();});}
function numero(){return (S.tec&&S.tec.w)||(D[S.pais]||{}).wa||'';}
function render(){
 var h='<ol class="stp" aria-label="Pasos de la solicitud">'+PASOS.map(function(p,i){return '<li class="'+(i===paso?'on':i<paso?'ok':'')+'">'+(i+1)+'. '+p+'</li>';}).join('')+'</ol>';
 if(paso===0){
  h+='<h2>¿Dónde está tu equipo?</h2><p class="ay">Detectamos tu barrio para enviarte al técnico '+esc(NM)+' más cercano.</p>'
   +'<button type="button" class="btn gps" id="gps">📍 <span><b>Usar mi ubicación</b></span></button><div id="det" role="status" aria-live="polite"></div>'
   +'<p class="ay" style="margin:14px 0 8px">O elígela tú:</p><div class="fl c2"><div><label for="p-pais">País</label><select id="p-pais"><option value="">Elige tu país</option>'+Object.keys(D).map(function(k){return '<option value="'+k+'"'+(k===S.pais?' selected':'')+'>'+esc(D[k].n)+'</option>';}).join('')+'</select></div>'
   +'<div><label for="p-ciudad">Ciudad</label><select id="p-ciudad"></select></div></div>'
   +'<div class="acc"><button type="button" class="btn pr" id="sig0">Continuar</button></div>';
 }else if(paso===1){
  h+='<h2>¿Qué equipo '+esc(NM)+' quieres arreglar?</h2><p class="ay">Toca el equipo.</p><div class="tl">'+Object.keys(O.equipos).map(function(k){var e=O.equipos[k];return '<button type="button" class="opt" data-k="'+k+'" aria-pressed="'+(S.equipo===k)+'"><img src="'+e.img+'" alt="'+esc(e.alt)+'" loading="lazy" width="300" height="225"><b>'+esc(cap(termino(k)))+' '+esc(NM)+'</b></button>';}).join('')+'</div>'
   +'<div class="acc"><button type="button" class="btn gh" data-ir="0">← Atrás</button></div>';
 }else if(paso===2){
  var e=O.equipos[S.equipo];
  h+='<h2>¿Qué le pasa a tu '+esc(termino(S.equipo).replace(/s$/,''))+'?</h2><p class="ay">Elige la falla que más se parece.</p><div class="fa">'+e.fallas.map(function(f,i){return '<button type="button" class="opt" data-f="'+i+'" aria-pressed="'+(S.falla===f[0])+'"><span class="dot '+(f[2]==='Urgente'?'u':f[2]==='Revisar pronto'?'r':'')+'"></span><span>'+esc(f[1])+'</span><small>'+esc(f[2])+'</small></button>';}).join('')
   +'<button type="button" class="opt" data-f="-1" aria-pressed="'+(S.falla==='Otra falla')+'"><span class="dot"></span><span>Otra falla / no sé qué es</span></button></div>'
   +'<div class="acc"><button type="button" class="btn gh" data-ir="1">← Atrás</button><button type="button" class="btn pr" id="sig2" '+(S.falla?'':'disabled')+'>Continuar</button></div>';
 }else{
  var ubi=(S.barrio?S.barrio+', ':'')+S.ciudad+', '+(D[S.pais]||{}).n;
  h+='<h2>Casi listo</h2><p class="ay">Completa tus datos y te escribimos por WhatsApp con la solicitud lista.</p>'
   +'<div class="res"><dl><dt>Marca</dt><dd>'+esc(NM)+'</dd><dt>Equipo</dt><dd>'+esc(cap(termino(S.equipo).replace(/s$/,'')))+'</dd><dt>Falla</dt><dd>'+esc(S.falla)+'</dd><dt>Ubicación</dt><dd>'+esc(ubi)+'</dd></dl></div>'
   +'<div class="fl c2"><div><label for="d-nom">Tu nombre</label><input id="d-nom" autocomplete="name" value="'+esc(S.nombre||'')+'" required></div><div><label for="d-mod">Modelo (opcional)</label><input id="d-mod" placeholder="Está en la etiqueta del equipo"></div>'
   +'<div><label for="d-dir">Dirección o referencia</label><input id="d-dir" autocomplete="street-address" value="'+esc(S.barrio||'')+'" placeholder="Barrio, calle, edificio"></div>'
   +'<div><label for="d-hor">¿Cuándo te sirve?</label><select id="d-hor"><option>Lo antes posible</option><option>Hoy</option><option>Mañana</option><option>Esta semana</option></select></div></div>'
   +'<div style="margin-top:12px"><label for="d-obs">Cuéntanos más (opcional)</label><textarea id="d-obs" placeholder="¿Desde cuándo pasa? ¿Muestra algún código?"></textarea></div>'
   +'<div class="ok-b" id="tecbox"></div>'
   +'<button type="button" class="btn wa" id="enviar" disabled>'+'<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.2-.7-2.7-1.1-4.4-3.8-4.5-4-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6c-.2.2-.3.4-.1.7.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.4.1.1.1.6-.1 1.2z"/></svg> Enviar solicitud por WhatsApp</button>'
   +'<div class="acc"><button type="button" class="btn gh" data-ir="2">← Atrás</button></div><div id="fin"></div>';
 }
 root.innerHTML=h;wire();}
function ciudades(){var p=$('#p-pais').value,s=$('#p-ciudad');if(!p){s.innerHTML='<option value="">Elige primero el país</option>';return;}
 s.innerHTML=Object.keys(D[p].ciudades).map(function(c){return '<option'+(c===S.ciudad?' selected':'')+'>'+esc(c)+'</option>';}).join('');}
function wire(){
 root.querySelectorAll('[data-ir]').forEach(function(b){b.onclick=function(){paso=+b.dataset.ir;render();root.scrollIntoView({behavior:'smooth',block:'start'});};});
 if(paso===0){
  var det=$('#det');ciudades();$('#p-pais').onchange=function(){S.pais=this.value;S.ciudad='';S.lat=null;ciudades();};
  $('#gps').onclick=function(){if(!navigator.geolocation){det.innerHTML='<div class="ok-b">Tu navegador no permite ubicación. Elige país y ciudad abajo.</div>';return;}
   det.innerHTML='<div class="ok-b">Buscando tu ubicación…</div>';
   navigator.geolocation.getCurrentPosition(function(p){var la=p.coords.latitude,lo=p.coords.longitude,c=cercana(la,lo);
     if(!c||c.d>600){det.innerHTML='<div class="ok-b">Todavía no tenemos técnicos en tu zona. Elige país y ciudad abajo.</div>';return;}
     det.innerHTML='<div class="ok-b">Buscando tu barrio…</div>';
     barrio(la,lo,function(nb){S.lat=la;S.lon=lo;S.pais=c.cc;S.ciudad=c.city;S.barrio=nb||'';$('#p-pais').value=c.cc;ciudades();$('#p-ciudad').value=c.city;
       elegirTec(function(){var otro=B.dataset.pais&&c.cc!==B.dataset.pais?'<br><b>Esta página es de '+esc(D[B.dataset.pais].n)+'.</b> <a href="/soporte-tecnico-autorizado-'+M+'-'+D[c.cc].ps+'/">Ver el servicio '+esc(NM)+' en '+esc(D[c.cc].n)+'</a>. Tu solicitud se enviará al técnico de '+esc(D[c.cc].n)+'.':'';
       det.innerHTML='<div class="ok-b"><b>📍 Estás en '+esc((nb?nb+', ':'')+c.city+', '+D[c.cc].n)+'</b><br><span class="mu">Técnico '+esc(NM)+' más cercano: '+esc(S.tec?S.tec.n:'servicio técnico')+(S.dkm!=null?' · a '+S.dkm+' km':'')+'</span>'+otro+'</div>';});});},
    function(e){det.innerHTML='<div class="ok-b">'+(e&&e.code===1?'No diste permiso de ubicación.':'No pudimos obtener tu ubicación.')+' Elige país y ciudad abajo.</div>';},{timeout:12000,maximumAge:600000});};
  $('#sig0').onclick=function(){var p=$('#p-pais').value,c=$('#p-ciudad').value;if(!p||!c){det.innerHTML='<div class="ok-b">Elige tu país y tu ciudad para continuar.</div>';return;}
   S.pais=p;S.ciudad=c;elegirTec(function(){paso=1;render();});};
 }
 if(paso===1)root.querySelectorAll('.opt').forEach(function(b){b.onclick=function(){if(S.equipo!==b.dataset.k)S.falla='';S.equipo=b.dataset.k;paso=2;render();};});
 if(paso===2){root.querySelectorAll('.opt').forEach(function(b){b.onclick=function(){var i=+b.dataset.f;S.falla=i<0?'Otra falla':O.equipos[S.equipo].fallas[i][0];root.querySelectorAll('.opt').forEach(function(x){x.setAttribute('aria-pressed',x===b);});$('#sig2').disabled=false;};});
  $('#sig2').onclick=function(){paso=3;render();};}
 if(paso===3){var n=$('#d-nom'),env=$('#enviar'),tb=$('#tecbox');
  tb.innerHTML=S.tec?'<b>Tu solicitud irá a:</b> '+esc(S.tec.n)+'<br><span class="mu">'+esc(S.tec.z+', '+S.tec.c)+(S.dkm!=null?' · a '+S.dkm+' km de ti':'')+'</span>':'<b>Tu solicitud irá al servicio técnico '+esc(NM)+' de '+esc((D[S.pais]||{}).n)+'.</b>';
  function v(){env.disabled=n.value.trim().length<2;}n.oninput=v;v();
  env.onclick=function(){var id='S'+new Date().toISOString().slice(2,10).replace(/-/g,'')+'-'+Math.floor(100+Math.random()*900);
   var e=O.equipos[S.equipo],ur=(e.fallas.filter(function(f){return f[0]===S.falla;})[0]||[])[2]||'';
   var L=['*Solicitud de servicio técnico '+NM+'* ('+id+')','',
    '📺 Equipo: '+cap(termino(S.equipo).replace(/s$/,''))+' '+NM,'🔧 Falla: '+S.falla+(ur?' ('+ur+')':'')];
   if($('#d-mod').value.trim())L.push('🏷️ Modelo: '+$('#d-mod').value.trim());
   L.push('📍 Ubicación: '+((S.barrio?S.barrio+', ':'')+S.ciudad+', '+D[S.pais].n));
   if($('#d-dir').value.trim())L.push('🏠 Dirección/referencia: '+$('#d-dir').value.trim());
   if(S.lat!=null)L.push('🗺️ Mapa: https://maps.google.com/?q='+S.lat.toFixed(5)+','+S.lon.toFixed(5));
   L.push('🕒 Horario: '+$('#d-hor').value,'👤 Nombre: '+n.value.trim());
   if($('#d-obs').value.trim())L.push('📝 Detalle: '+$('#d-obs').value.trim());
   var url='https://wa.me/'+numero()+'?text='+encodeURIComponent(L.join('\n'));
   try{localStorage.setItem('ord',JSON.stringify({nombre:n.value.trim(),pais:S.pais,ciudad:S.ciudad}));}catch(x){}
   window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'solicitud_whatsapp',marca:M,pais:S.pais,equipo:S.equipo,falla:S.falla});window.dataLayer.push({event:'whatsapp',marca:M,pais:S.pais});
   window.open(url,'_blank','noopener');
   $('#fin').innerHTML='<div class="ok-b"><b>✅ Solicitud '+id+' lista.</b><br>Si WhatsApp no se abrió, <a href="'+url+'" target="_blank" rel="noopener">toca aquí para enviarla</a>.</div>';};}
}
// arranque: país/equipo/falla preseleccionados por la página
if(S.equipo&&!O.equipos[S.equipo])S.equipo='';
if(S.falla&&S.equipo){var ok=O.equipos[S.equipo].fallas.some(function(f){return f[0]===S.falla;});if(!ok)S.falla='';}
render();
if(navigator.permissions&&navigator.permissions.query){navigator.permissions.query({name:'geolocation'}).then(function(s){if(s.state==='granted'&&paso===0&&$('#gps'))$('#gps').click();}).catch(function(){});}
})();
