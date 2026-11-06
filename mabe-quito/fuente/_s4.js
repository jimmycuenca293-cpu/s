const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [nm,o] of [['pc',{viewport:{width:1366,height:850}}],['cel',{...devices['iPhone 13'],deviceScaleFactor:1}]]){const c=await b.newContext(o);const p=await c.newPage();
for(const [k,u] of [['refri','/reparacion-de-refrigeradoras-mabe-quito/'],['zona','/servicio-tecnico-mabe-en-la-carolina/'],['falla','/refrigeradora-mabe-no-enfria-quito/']]){await p.goto('http://127.0.0.1:8711'+u,{waitUntil:'networkidle'});await p.waitForTimeout(300);await p.screenshot({path:`p-${k}-${nm}.png`});}
if(nm==='cel'){await p.goto('http://127.0.0.1:8711/',{waitUntil:'networkidle'});await p.screenshot({path:'p-home-cel.png'});await p.click('.mov summary');await p.waitForTimeout(300);await p.screenshot({path:'p-menu-cel.png'});}
await c.close()}await b.close()})()
