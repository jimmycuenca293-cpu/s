const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();
const c=await b.newContext({viewport:{width:1366,height:900}});const pg=await c.newPage();
await pg.goto('http://localhost:8797/');await pg.addStyleTag({content:'html{scroll-behavior:auto!important}'});
const H=await pg.evaluate(()=>document.documentElement.scrollHeight);console.log('H',H);
let i=0;for(let y=900;y<H;y+=1500){await pg.evaluate(y=>scrollTo(0,y),y);await pg.waitForTimeout(300);await pg.screenshot({path:`w-${i++}.png`});}
// otras páginas
for(const [n,p] of [['hub','/electrodomesticos/'],['cocina','/reparacion-de-cocinas-whirlpool-quito/'],['contacto','/contacto/'],['faq','/preguntas-frecuentes/'],['cob','/zonas-de-servicio-quito/']]){await pg.goto('http://localhost:8797'+p);await pg.waitForTimeout(500);await pg.screenshot({path:`w-${n}.png`});}
await b.close()})()
