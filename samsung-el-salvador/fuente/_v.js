const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [n,o,p] of [['d',{viewport:{width:1366,height:900}},'/'],['m',devices['iPhone 13'],'/'],['n',{viewport:{width:1366,height:900}},'/reparacion-de-neveras-samsung-quito/']]){
const c=await b.newContext(o);const pg=await c.newPage();await pg.goto('http://localhost:8932'+p);await pg.waitForTimeout(1500);
await pg.screenshot({path:`v-${n}.png`,fullPage:false});
if(n!=='n'){await pg.evaluate(()=>window.scrollTo(0,1400));await pg.waitForTimeout(500);await pg.screenshot({path:`v-${n}2.png`});}
await c.close()}
await b.close()})()
