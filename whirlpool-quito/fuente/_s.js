const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1366,height:900}});const pg=await c.newPage();
await pg.goto('http://localhost:8793/');await pg.waitForTimeout(1200);
const y=await pg.evaluate(()=>document.querySelector('.seo').getBoundingClientRect().top+scrollY-120);await pg.addStyleTag({content:'html{scroll-behavior:auto!important}'});await pg.evaluate(y=>scrollTo(0,y),y);await pg.waitForTimeout(500);await pg.screenshot({path:'s-seo.png'});
await pg.goto('http://localhost:8793/mapa-del-sitio/');await pg.waitForTimeout(800);await pg.screenshot({path:'s-mapa.png'});
await b.close()})()
