const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
let p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+process.cwd()+'/_og.html');await p.waitForTimeout(1500);await p.screenshot({path:'assets/og.png'});
p=await b.newPage({viewport:{width:512,height:512}});await p.goto('file://'+process.cwd()+'/_icon.html');await p.waitForTimeout(1500);await p.screenshot({path:'assets/icon-512.png'});await b.close()})()
