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
    st=lambda: E("[qStage('c5'),Qs.c5&&Qs.c5.prog,ensureX().curso,S.spells.join(),pauseFlag,document.querySelector('#dialog').hidden]")
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};['c2','c3','c4'].forEach(q=>Qs[q]={stage:99,prog:0,done:true});S.house='raiz';S.flags.friends=true;S.flags.rival1=true;S.lvl=20;S.xp=99999;ensureX();S.x.curso=4;S.x.f.bastianTold=1;S.x.f.bastianPromesa=1;S.spells=['chispa','rafaga','pasmo','escudo','luz','paso','nana']")
    print("ready",await E("JSON.stringify(cursoState())"))
    await E("endCurso()");await E(D);await pg.wait_for_timeout(3500);await E(D);await pg.wait_for_timeout(2500);await E(D);print("c5",await st())
    await E("TALK.albarran();"+D);print("intro",await st())
    await E("TALK.socorro();"+D);print("soc",await st())
    await E(f"__go({0},{1},12)".replace("{0}","PEAK39[0]").replace("{1}","PEAK39[1]"))
    await E("__go(PEAK39[0],PEAK39[1],7)");await pg.wait_for_timeout(700);await E(D);print("peak",await st())
    await E("TALK.socorro();"+D);print("lanza",await st())
    await E("__go(VEST39[0],VEST39[1],23.5)");await pg.wait_for_timeout(700);await E(D);print("vest",await st())
    await E("__go(Math.floor(NPC.albarran.px/16),Math.floor(NPC.albarran.py/16)+1,20)");await pg.wait_for_timeout(500);await E("TALK.albarran()");await pg.wait_for_timeout(300);await E(D);await pg.wait_for_timeout(300);await E(D);print("assault",await st(),await E("foes.filter(f=>f.assault).length"))
    await pg.wait_for_timeout(800);await pg.screenshot(path=SCR+"H_assault.png")
    await E("S.spell=S.spells.indexOf('lanza');S.mp=20;S.cd=0;const e=foes.find(f=>f.assault);S.px=e.px-40;S.py=e.py;S.dir='right';cast()");await pg.wait_for_timeout(600);await pg.screenshot(path=SCR+"H_lanza.png")
    for i in range(8):
      await E("for(const f of foes.filter(f=>f.assault&&!f.dead).slice(0,1))killFoe(f)");await pg.wait_for_timeout(200)
    await pg.wait_for_timeout(400);await pg.screenshot(path=SCR+"H_ramiro.png");await E(D);print("after",await st(),await E("[S.x.f.ramiroMuerto,S.x.f.bastianIdo,NPC.guarda.name]"))
    await E("__go(PATIO39[0],PATIO39[1],12)");await pg.wait_for_timeout(700);await E(D);print("patio",await st())
    await E("TALK.albarran();"+D);print("lente",await st(),await E("S.x.f.lenteDec"))
    await E("OBJ_ACT.piano({});"+D);await pg.wait_for_timeout(300);print("end5",await st(),await E("document.querySelector('#ending h2').textContent"))
    await E("document.querySelector('#end-go').click();TALK.albarran();"+D);await pg.wait_for_timeout(3600);await E(D);await pg.wait_for_timeout(2500);await E(D);print("c6",await E("[ensureX().curso,qStage('c6'),NPC.guarda.name]"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
