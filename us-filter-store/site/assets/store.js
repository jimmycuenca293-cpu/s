
(function(){
var S=window.STORE||{};window.dataLayer=window.dataLayer||[];
document.addEventListener('click',function(ev){var a=ev.target.closest('a[href*="wa.me/"]');if(a){dataLayer.push({event:'whatsapp',button:(a.textContent||'').trim().slice(0,60),page:location.pathname})}},true);
function money(n){return '$'+n.toFixed(2)}
/* precios: el HTML ya trae el precio; /assets/prices.json lo puede cambiar sin volver a generar el sitio */
function boot(prices){
 document.querySelectorAll('.buy').forEach(function(box){
  var sku=box.dataset.sku,pr=(prices&&prices[sku])||{},price=pr.price!=null?pr.price:parseFloat(box.dataset.price||'0')||0,pack=pr.pack!=null?pr.pack:parseFloat(box.dataset.pack||'0')||0,ship=parseFloat(S.shipping||0)||0;
  var name=box.dataset.name,sel=box.querySelector('select.q'),out=box.querySelector('.price'),pp=box.querySelector('.pp'),pay=box.querySelector('.paywrap');
  if(!price){if(pay)pay.hidden=true;return}
  function qtyInfo(){var v=sel?sel.value:'1',n=parseInt(v,10)||1,unit=price;if(v==='pack'){n=2;unit=pack/2}return {n:n,unit:unit,total:(v==='pack')?pack:price*n}}
  function paint(){var q=qtyInfo();if(out)out.innerHTML=money(q.total)+' <small>USD'+(ship?' + '+money(ship)+' shipping':'')+'</small>'}
  paint();if(sel)sel.addEventListener('change',function(){paint();render()});
  var rendered=false;function render(){
   if(!S.paypalClientId||!window.paypal){return}
   pp.innerHTML='';var q=qtyInfo();var items=(q.total).toFixed(2);
   paypal.Buttons({style:{layout:'vertical',shape:'pill',label:'paypal'},
    createOrder:function(d,a){var q=qtyInfo(),it=q.total.toFixed(2);return a.order.create({purchase_units:[{description:name+' x'+q.n,custom_id:sku+'|'+q.n,amount:{currency_code:'USD',value:(q.total+ship).toFixed(2),breakdown:{item_total:{currency_code:'USD',value:it},shipping:{currency_code:'USD',value:ship.toFixed(2)}}},items:[{name:name,sku:sku,unit_amount:{currency_code:'USD',value:q.unit.toFixed(2)},quantity:String(q.n)}]}],application_context:{shipping_preference:'GET_FROM_FILE'}})},
    onApprove:function(d,a){return a.order.capture().then(function(){dataLayer.push({event:'purchase_paypal',sku:sku});location.href='/thank-you/'})}}).render(pp)}
  if(S.paypalClientId){var s=document.createElement('script');s.src='https://www.paypal.com/sdk/js?client-id='+encodeURIComponent(S.paypalClientId)+'&currency=USD&components=buttons&enable-funding=card';s.onload=render;document.head.appendChild(s)}
  else if(!box.dataset.link){pp.innerHTML='<p class="note">Online checkout with PayPal is coming soon. To order now, message us on WhatsApp.</p>'}
 });
}
fetch('/assets/prices.json').then(function(r){return r.ok?r.json():{}}).catch(function(){return {}}).then(boot);
/* buscador de filtros */
var box=document.getElementById('finder-q'),res=document.getElementById('finder-res');
if(box&&res){fetch('/assets/search.json').then(function(r){return r.json()}).then(function(ix){
 function norm(s){return s.toLowerCase().replace(/[^a-z0-9]+/g,'')}
 function run(){var q=norm(box.value);res.innerHTML='';if(q.length<2)return;var n=0;
  ix.forEach(function(it){if(n>=40)return;if(norm(it[0]+' '+it[2]).indexOf(q)>-1){n++;res.insertAdjacentHTML('beforeend','<a href="'+it[1]+'">'+it[0]+'<small>'+it[3]+'</small></a>')}});
  if(!n)res.innerHTML='<p>No match yet. Send us your refrigerator model number or a photo of the old filter on <a href="'+S.waLink+'">WhatsApp</a>.</p>'}
 box.addEventListener('input',run);var u=new URLSearchParams(location.search).get('q');if(u){box.value=u;run()}})}
})();
