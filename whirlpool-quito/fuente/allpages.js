const {chromium,devices}=require('playwright');const fs=require('fs');
const urls=[...fs.readFileSync('site/sitemap.xml','utf8').matchAll(/<loc>https:\/\/whirlpoolquito.click(\/[^<]*)<\/loc>/g)].map(m=>m[1]);
(async()=>{const b=await chromium.launch();let bad=[];
for(const [nm,o] of [['cel',{...devices['iPhone 13']}],['pc',{viewport:{width:1366,height:850}}]]){
 const c=await b.newContext(o);const p=await c.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 for(const u of urls){errs.length=0;await p.goto('http://127.0.0.1:8841'+u,{waitUntil:'load'});
  const r=await p.evaluate(()=>({ov:document.documentElement.scrollWidth-document.documentElement.clientWidth,imgs:[...document.images].filter(i=>i.complete&&!i.naturalWidth).length,h1:document.querySelectorAll('h1').length}));
  if(r.ov>1||r.imgs||r.h1!==1||errs.length)bad.push([nm,u,r,errs[0]])}
 await c.close()}
await b.close();console.log('páginas x2 anchos:',urls.length*2,'| con problemas:',bad.length);bad.slice(0,8).forEach(x=>console.log(JSON.stringify(x)))})()
