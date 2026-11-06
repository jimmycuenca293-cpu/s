const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [nm,o] of [['pc',{viewport:{width:1366,height:850}}],['cel',{...devices['iPhone 13'],deviceScaleFactor:1}]]){const c=await b.newContext(o);const p=await c.newPage();
for(const [k,u] of [['campana','/reparacion-de-campanas-extractoras-mabe-quito/'],['home','/']]){await p.goto('http://127.0.0.1:8671'+u,{waitUntil:'networkidle'});if(k==='home')await p.evaluate(()=>document.querySelector('#electrodomesticos').scrollIntoView());await p.waitForTimeout(400);await p.screenshot({path:`n-${k}-${nm}.png`});}
await c.close()}await b.close()})()
