const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
let p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/_og.html');await p.waitForTimeout(1200);await p.screenshot({path:'assets/og.png'});
p=await b.newPage({viewport:{width:660,height:128},deviceScaleFactor:2});await p.goto('file://'+process.cwd()+'/_logo.html');await p.waitForTimeout(800);await p.screenshot({path:'assets/logo.png',omitBackground:true});
p=await b.newPage({viewport:{width:180,height:180}});await p.setContent('<body style="margin:0;background:#0c2740;display:grid;place-items:center;width:180px;height:180px"><div style="width:130px">'+require('fs').readFileSync('assets/favicon.svg','utf8').replace('<svg ','<svg width=130 height=114 ')+'</div></body>');await p.screenshot({path:'assets/apple-touch-icon.png'});
await b.close()})()
