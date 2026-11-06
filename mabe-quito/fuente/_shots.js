const {chromium,devices}=require('playwright');(async()=>{const b=await chromium.launch();
for(const [nm,o] of [['pc',{viewport:{width:1366,height:850}}],['cel',{...devices['iPhone 13'],deviceScaleFactor:1}]]){const c=await b.newContext(o);const p=await c.newPage();
for(const [k,u] of [['home','/'],['refri','/reparacion-de-refrigeradoras-mabe-quito/'],['falla','/refrigeradora-mabe-no-enfria-quito/']]){await p.goto('http://127.0.0.1:8671'+u,{waitUntil:'networkidle'});await p.waitForTimeout(400);await p.screenshot({path:`q-${k}-${nm}.png`,fullPage:k!=='home'?false:false});}
await c.close()}await b.close()})()
