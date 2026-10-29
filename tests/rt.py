import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(500)
    r=await pg.evaluate("""(()=>{const ser=JSON.parse(serialize()).S;const miss=[];
      for(const k of Object.keys(S)){if(!(k in ser)){const v=S[k];miss.push(k+':'+(typeof v==='function'?'fn':Array.isArray(v)?'arr'+v.length:typeof v==='object'&&v?'obj':String(v)))}}
      return miss})()""")
    print(r);print(errs);await b.close()
asyncio.run(main())
