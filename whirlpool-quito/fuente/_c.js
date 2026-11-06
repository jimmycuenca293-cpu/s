const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1366,height:900}});const pg=await c.newPage();
await pg.goto('http://localhost:8797/');await pg.addStyleTag({content:'html{scroll-behavior:auto!important}'});
const y=await pg.evaluate(()=>{const h=[...document.querySelectorAll('h2')].find(x=>x.textContent.includes('Cómo trabajamos'));return h.getBoundingClientRect().top+scrollY-100});
await pg.evaluate(y=>scrollTo(0,y),y);await pg.waitForTimeout(600);await pg.screenshot({path:'c-home.png'});
await pg.goto('http://localhost:8797/como-trabajamos/');await pg.waitForTimeout(800);await pg.screenshot({path:'c-page.png',fullPage:false});
await b.close()})()
