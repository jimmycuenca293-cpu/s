const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const c=await b.newContext({viewport:{width:1366,height:900}});const pg=await c.newPage();
for(const [n,p] of [['contacto','/contacto/'],['guia','/como-limpiar-ducto-secadora-whirlpool-quito/'],['zxa','/reparacion-de-lavadoras-whirlpool-en-la-carolina/']]){
await pg.goto('http://localhost:8830'+p);await pg.addStyleTag({content:'html{scroll-behavior:auto!important}'});await pg.waitForTimeout(500);await pg.screenshot({path:`p-${n}.png`,fullPage:true});}
await b.close()})()
