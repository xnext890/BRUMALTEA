import pathlib,tempfile
TMP=tempfile.gettempdir()+"/"
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio,json
from playwright.async_api import async_playwright
MOCK='''(()=>{
window.__drive={file:null,calls:[]};
window.google={accounts:{oauth2:{initTokenClient:(c)=>({requestAccessToken:()=>setTimeout(()=>c.callback({access_token:"tok",expires_in:3600}),20)}),revoke:(t,cb)=>cb&&cb()}}};
const _f=window.fetch;
window.fetch=async(u,o)=>{u=String(u);o=o||{};const D=window.__drive;D.calls.push((o.method||"GET")+" "+u.split("?")[0].replace("https://www.googleapis.com",""));
 const J=(x,s)=>new Response(JSON.stringify(x),{status:s||200});
 if(u.includes("userinfo"))return J({email:"yo@test.com"});
 if(u.includes("alt=media"))return J(D.file);
 if(u.includes("/upload/")){const b=o.body;const m=b.indexOf("\\r\\n\\r\\n",b.indexOf("Content-Type: application/json\\r\\n\\r\\n")+10);
   D.file=JSON.parse(o.method==="PATCH"?b:b.slice(b.lastIndexOf("application/json\\r\\n\\r\\n")+"application/json\\r\\n\\r\\n".length,b.lastIndexOf("\\r\\n--b43")));return J({id:"f1"});}
 if(u.includes("drive/v3/files?"))return J({files:D.file?[{id:"f1"}]:[]});
 return _f(u,o);};})()
'''
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.evaluate(MOCK)
    # sin cid: abre panel
    await pg.click("#c43-in");print("panel visible",await pg.evaluate("!document.getElementById('cfg43').hidden"))
    await pg.fill("#cfg43-id","malo");await pg.click("#cfg43-ok");print("rechaza",await pg.inner_text("#c43-st"))
    await pg.fill("#cfg43-id","123-abc.apps.googleusercontent.com");await pg.click("#cfg43-ok");await pg.wait_for_timeout(300)
    print("login",await pg.inner_text("#c43-in"),"|",await pg.inner_text("#c43-st"))
    # empezar partida, guardar y subir
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(400)
    await pg.evaluate("saveGame()");await pg.evaluate("window.__tk=1");
    await pg.evaluate("clearTimeout(CLOUD43.timer);cloudSync43()");await pg.wait_for_timeout(300)
    d=await pg.evaluate("window.__drive.file");print("subida",bool(d and d['data']),pg and await pg.evaluate("window.__drive.calls"))
    # nuevo dispositivo: borra local, login -> trae nube
    await pg.evaluate("localStorage.clear()");await pg.reload();await pg.wait_for_timeout(400)
    cloud=d
    await pg.evaluate(MOCK);await pg.evaluate("window.__drive.file=%s"%json.dumps(cloud))
    await pg.evaluate("localStorage.setItem('brumaltea-cid','123-abc.apps.googleusercontent.com')")
    await pg.click("#c43-in");await pg.wait_for_timeout(300)
    print("continuar visible",await pg.evaluate("!document.getElementById('btn-continue').hidden"),await pg.inner_text("#c43-st"))
    await pg.click("#btn-continue");await pg.wait_for_timeout(400);print("started",await pg.evaluate("S.started"))
    # export/import
    await pg.evaluate("localStorage.removeItem('brumaltea-partida-v1')")
    imp=json.dumps({"game":"brumaltea","ts":5,"data":cloud['data']})
    open(TMP+"imp.json","w").write(imp)
    await pg.reload();await pg.wait_for_timeout(300)
    await pg.set_input_files("#c43-file",TMP+"imp.json");await pg.wait_for_timeout(200)
    print("import",await pg.inner_text("#c43-st"),await pg.evaluate("!document.getElementById('btn-continue').hidden"))
    open(TMP+"bad.json","w").write("{}");await pg.set_input_files("#c43-file",TMP+"bad.json");await pg.wait_for_timeout(200)
    print("bad",await pg.inner_text("#c43-st"))
    print("ERRS",errs)
    await b.close()
asyncio.run(main())
