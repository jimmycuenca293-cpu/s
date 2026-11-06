const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1366,height:900}});const pg=await c.newPage();
for(const [n,p] of [['e','/'],['c','/cocina-whirlpool-huele-a-gas-quito/']]){await pg.goto('http://localhost:8795'+p);await pg.addStyleTag({content:'html{scroll-behavior:auto!important}'});
if(n==='e'){const y=await pg.evaluate(()=>document.querySelector('#electrodomesticos').getBoundingClientRect().top+scrollY-90);await pg.evaluate(y=>scrollTo(0,y+420),y);}
await pg.waitForTimeout(600);await pg.screenshot({path:`e-${n}.png`});}
await b.close()})()
