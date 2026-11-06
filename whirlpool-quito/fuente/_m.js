const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();
const c=await b.newContext({...devices['iPhone 13']});const pg=await c.newPage();
await pg.goto('http://localhost:8797/');await pg.addStyleTag({content:'html{scroll-behavior:auto!important}'});
const H=await pg.evaluate(()=>document.documentElement.scrollHeight);console.log('H',H);
let i=0;for(const y of [1600,3400,5200,7000,9200]){await pg.evaluate(y=>scrollTo(0,y),y);await pg.waitForTimeout(300);await pg.screenshot({path:`m-${i++}.png`});}
await pg.goto('http://localhost:8797/como-trabajamos/');await pg.evaluate(()=>scrollTo(0,700));await pg.waitForTimeout(400);await pg.screenshot({path:'m-pasos.png'});
await pg.goto('http://localhost:8797/refrigeradora-whirlpool-no-enfria-quito/');await pg.evaluate(()=>scrollTo(0,900));await pg.waitForTimeout(400);await pg.screenshot({path:'m-falla.png'});
await b.close()})()
