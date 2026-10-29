import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
from helpers import HELP
SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e.stack)[:600]))
    await pg.goto(INDEX);await pg.wait_for_timeout(500)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    E=pg.evaluate
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:11,prog:0,done:true};S.house='raiz';S.flags.side='island';S.spells=['chispa','rafaga','pasmo'];S.lvl=5;ensureX();S.day=5;")
    print("wday",await E("[wday(S.day),DAYN[wday(S.day)]]"))
    await E("while(wday(S.day)!==5)S.day++;__go(1006,122,17.5)");await pg.wait_for_timeout(800)
    print("open",await E("[tourneyOpen(),duelOK()]"))
    await E("TALK.candela()");await pg.wait_for_timeout(300)
    print(await E("document.querySelector('#dialog').innerText.slice(0,200)"))
    await E("if(typing)finishType(dq.choices);pickChoice(0)");await pg.wait_for_timeout(500)
    print("cuadro",await E("!document.getElementById('cuadro').hidden"));await pg.screenshot(path=SCR+"D_cuadro.png")
    for rnd in range(4):
      await E("document.getElementById('cu-go').click()");await pg.wait_for_timeout(1500)
      if rnd==0: await pg.screenshot(path=SCR+"D_duel.png")
      await E("if(duelRun){duelRun.cd=0;for(let k=0;k<3;k++){duelRun&&(duelRun.e.inv=0,duelRun.e.shield=0,duelPoint('me'));}}");await pg.wait_for_timeout(1200)
      print("round",rnd,await E("!document.getElementById('cuadro').hidden"),await E("document.getElementById('cu-t').textContent+' | '+document.getElementById('cu-s').innerText"))
      if rnd==3: await pg.screenshot(path=SCR+"D_final.png")
    await E("__drain()")
    print("D",await E("JSON.stringify(ens26())"),"insignia",await E("S.flags.insignia"),"pts",await E("JSON.stringify(S.cup)"),"lunas",await E("S.lunas"))
    print("again",await E("TALK.candela();const t=document.querySelector('#dialog').innerText;__drain();t.slice(0,150)"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
