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
    D="__drain();if(SC37&&document.querySelector('#dialog').hidden)hideScene();"
    st=lambda: E("[qStage('c6'),ensureX().curso,S.spells.join(),pauseFlag,areaOfXY(S.px,S.py)]")
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};['c2','c3','c4','c5'].forEach(q=>Qs[q]={stage:99,prog:0,done:true});S.house='raiz';S.flags.friends=true;S.flags.rival1=true;S.lvl=22;ensureX();S.x.curso=6;S.x.f.lenteDec='esconder';S.x.f.valcDecision='cubrir';S.spells=['chispa','rafaga','pasmo','escudo','luz','paso','nana','lanza'];Qs.c6={stage:0,prog:0,done:false}")
    await E("TALK.albarran();"+D);print("intro",await st())
    await E("TALK.casilda();"+D);print("libro",await st())
    await E("__go(PAZO40[0],PAZO40[1],21)");await pg.wait_for_timeout(800)
    await pg.screenshot(path=SCR+"K_cena.png");await E(D);await pg.wait_for_timeout(300);await E(D);print("cena",await st(),await E("S.x.f.cenaMal"))
    await E("__go(1465,119,12);OBJ_ACT.puertaint({k:'cripta6'})");await pg.wait_for_timeout(1500);await E(D);print("in",await st())
    await pg.screenshot(path=SCR+"K_cripta.png")
    await E("OBJ_ACT.registroAnclas();"+D);await pg.wait_for_timeout(800);print("reg",await st(),await E("foes.filter(f=>f.type==='guardian').length"))
    await E("const g=foes.find(f=>f.type==='guardian');hitFoe(g,5,0,0)");print("immune",await E("foes.find(f=>f.type==='guardian').hp"))
    await E("S.spell=S.spells.indexOf('desvelo');S.mp=20;S.cd=0;const g=foes.find(f=>f.type==='guardian');S.px=g.px;S.py=g.py+40;cast()");await pg.wait_for_timeout(200)
    await E("const g=foes.find(f=>f.type==='guardian');hitFoe(g,5,0,0)");print("hit",await E("[foes.find(f=>f.type==='guardian').hp,foes.find(f=>f.type==='guardian').desv]"))
    await pg.wait_for_timeout(1500);await pg.screenshot(path=SCR+"K_boss.png")
    await E("const g=foes.find(f=>f.type==='guardian');killFoe(g)");await pg.wait_for_timeout(300);await E(D);print("killed",await st())
    await E("TALK.albarran();"+D);print("conf",await st(),await E("S.x.f.confesion"))
    await E("__go(36,37,22);OBJ_ACT.piano({});"+D);await pg.wait_for_timeout(300);print("neb",await st(),await E("[S.x.f.nebulario,document.querySelector('#ending h2').textContent]"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
