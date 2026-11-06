const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [n,o,p] of [['d',{viewport:{width:1366,height:900}},'/'],['m',devices['iPhone 13'],'/'],['f',{viewport:{width:1366,height:900}},'/refrigeradora-whirlpool-no-enfria-quito/'],['z',{viewport:{width:1366,height:900}},'/servicio-tecnico-whirlpool-en-la-carolina/']]){
const c=await b.newContext(o);const pg=await c.newPage();await pg.goto('http://localhost:8795'+p);await pg.waitForTimeout(1200);
await pg.screenshot({path:`v-${n}.png`});
if(n==='d'||n==='m'){await pg.evaluate(()=>window.scrollTo(0,900));await pg.waitForTimeout(400);await pg.screenshot({path:`v-${n}2.png`});await pg.evaluate(()=>window.scrollTo(0,2200));await pg.waitForTimeout(400);await pg.screenshot({path:`v-${n}3.png`});}
await c.close()}
await b.close()})()
