const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [nm,o] of [['pc',{viewport:{width:1366,height:850}}],['cel',{...devices['iPhone 13'],deviceScaleFactor:1}]]){const c=await b.newContext(o);const p=await c.newPage();
for(const [k,u] of [['home','/'],['refri','/reparacion-de-refrigeradoras-mabe-quito/'],['zonas','/zonas-de-servicio-quito/'],['elec','/electrodomesticos/']]){await p.goto('http://127.0.0.1:8711'+u,{waitUntil:'networkidle'});await p.waitForTimeout(300);await p.screenshot({path:`o-${k}-${nm}.png`,fullPage:true});}
if(nm==='pc'){await p.goto('http://127.0.0.1:8711/',{waitUntil:'networkidle'});await p.hover('.dd >> nth=0');await p.waitForTimeout(300);await p.screenshot({path:'o-menu.png',clip:{x:0,y:0,width:1366,height:520}});}
await c.close()}await b.close()})()
