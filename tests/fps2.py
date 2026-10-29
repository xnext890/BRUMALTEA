import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"
from helpers import HELP
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    await pg.goto(INDEX);await pg.wait_for_timeout(500)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    await pg.evaluate("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:11,prog:0,done:true};S.house='raiz';ensureX();placeStudentsNow()")
    for (x,y,h) in [(1120,40,12),(1131,99,22),(1282,100,12),(1420,30,12)]:
      await pg.evaluate(f"__go({x},{y},{h})");await pg.wait_for_timeout(800)
      fps=await pg.evaluate("new Promise(r=>{let n=0;const t0=performance.now();function f(){n++;if(performance.now()-t0<2000)requestAnimationFrame(f);else r(n/2)}requestAnimationFrame(f)})")
      print(x,y,fps)
    await b.close()
asyncio.run(main())
