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
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};S.house='raiz';S.spells=['chispa','rafaga','pasmo','nana'];S.lvl=8;S.maxHearts=8;S.hearts=8;S.mp=2;ensureX()")
    await E("__go(340,30,12)");await pg.wait_for_timeout(500);await E("__drain();foes.length=0")
    # roll + perfect dodge
    r=await E("(()=>{const x0=S.px;onKey('c');const a=[!!ROLL36,rollI36>0];hurtPlayer(S.px+5,S.py);return [a,S.hearts,S.mp,S.x.f.perfects]})()")
    await pg.wait_for_timeout(500);print("roll",r,"moved",await E("Math.round(S.px)"))
    # lobo telegraph
    await E("__drain();foes.length=0;const e=mkFoe('lobo',S.px+50,S.py,{keep:true});e.cd=0;window._L=e")
    await pg.wait_for_timeout(250);print("wind",await E("[_L.wind>0,_L.lunge]"));await pg.screenshot(path=SCR+"C_lobo.png")
    await pg.wait_for_timeout(500);print("lunged",await E("[_L.wind,_L.lunge>0||_L.cd>1]"))
    # yelmo
    await E("foes.length=0;S.hearts=8;window._Y=mkFoe('yelmo',S.px+40,S.py,{keep:true})")
    hp=await E("_Y.hp");await E("hitFoe(_Y,3,0,0)");print("yelmo block",hp,await E("_Y.hp"))
    await E("_Y.stun=2;hitFoe(_Y,foeDmg(2,_Y),0,0)");print("yelmo stunned",await E("_Y.hp"))
    await E("_Y.stun=0;_Y.slamCd=0;_Y.px=S.px+20");await pg.wait_for_timeout(300);await pg.screenshot(path=SCR+"C_yelmo.png");print("swing",await E("_Y.swing"))
    # swarm
    await E("foes.length=0;__go(1120,30,23)");await pg.wait_for_timeout(400);await E("__drain();foes.length=0;swarmT36=0;spawnTick()")
    print("swarm",await E("foes.filter(e=>e.type==='polilla').length"));await pg.wait_for_timeout(600);await pg.screenshot(path=SCR+"C_swarm.png")
    await E("S.mp=10;S.cd=0;S.spell=S.spells.indexOf('nana');for(const e of foes)e.px=S.px+20,e.py=S.py;cast()");print("slept",await E("foes.filter(e=>e.stun>0).length"))
    # fatuo telegraph
    await E("foes.length=0;window._F=mkFoe('fatuo',S.px+60,S.py-10,{keep:true});_F.cd=.3");await pg.wait_for_timeout(120);await pg.screenshot(path=SCR+"C_fatuo.png")
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
