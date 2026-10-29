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
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e.stack)[:600]));pg.on("console",lambda m:errs.append(m.text) if m.type in("warning","error") else None)
    await pg.goto(INDEX);await pg.wait_for_timeout(500)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    E=pg.evaluate
    async def step(js,shot=None,wait=900):
      await E(js);await pg.wait_for_timeout(wait)
      if shot:await pg.screenshot(path=SCR+shot)
    await E("Qs.m0={stage:4,prog:0,done:true};S.house='raiz';S.flags.friends=true;S.flags.rival1=true;S.lvl=8;ensureX()")
    # 1: tu tambien
    await step("Qs.m1={stage:10,prog:0,done:false};OBJ_ACT.piano({});for(let i=0;i<4;i++)advance()","G_m1.png",1500)
    await E("__drain()");await pg.wait_for_timeout(300);print("m1",await E("[qStage('m1'),S.x.f.tuTambien,document.querySelector('#end-text').textContent.slice(0,40)]"));await E("__drain();document.querySelector('#end-go').click()")
    # 2: velado
    await step("Qs.c2={stage:6,prog:0,done:false};S.x.curso=2;__go(425,25,12)",None,600)
    await E("__drain()");await pg.wait_for_timeout(600)
    for i in range(4): await E("if(typing)finishType(dq&&dq.choices);advance()")
    await pg.wait_for_timeout(1300);await pg.screenshot(path=SCR+"G_vel.png");await E("__drain()");print("vel",await E("[S.x.f.velCara,pauseFlag,!!SC37,frozen(),qStage('c2'),areaOfXY(S.px,S.py),document.querySelector('#dialog').hidden,document.querySelector('#menu').hidden]"))
    # cripta valcarcel
    await step("ARRIVE.c2_6();for(let i=0;i<5;i++){if(typing)finishType(dq.choices);advance()}","G_crip.png",1300)
    await E("while(dq&&!dq.choices){if(typing)finishType(dq.choices);advance()};if(dq&&dq.choices)pickChoice(0)");await pg.wait_for_timeout(200);await E("__drain()")
    print("valc",await E("[S.x.f.valcDecision,am37().valcarcel.p,qStage('c2')]"))
    # 3: nora
    await step("S.x.curso=3;Qs.c2={stage:99,prog:0,done:true};Qs.c3={stage:9,prog:0,done:false};foes.length=0",None,1500)
    await pg.screenshot(path=SCR+"G_nora.png");await E("__drain()");await pg.wait_for_timeout(3000);await E("__drain()");print("nora",await E("[S.x.f.noraGone,S.x.f.calvoGone,npcVisible(NPC.nora)]"))
    await E("talkFriend(NPC.bastian);if(typing)finishType(dq.choices);pickChoice(0);__drain()");print("told",await E("S.x.f.bastianTold"))
    # 4: lapida
    await step("S.x.curso=4;Qs.c4={stage:5,prog:0,done:false};OBJ_ACT.lapida();__drain()",None,800)
    await E("__drain()");print("lap",await E("[S.x.f.lapidaLeida,qStage('c4')]"))
    await E("OBJ_ACT.librogris();__drain()");print("abuela",await E("S.x.f.abuelaIria"))
    await E("talkFriend(NPC.iria);if(typing)finishType(dq.choices);pickChoice(0);__drain()");print("iria",await E("S.x.f.iriaDecision"))
    await step("TALK.rueda();advance();advance()","G_rueda.png",1200);await E("__drain()")
    await E("openMenu('amigos')");await pg.wait_for_timeout(300);await pg.screenshot(path=SCR+"G_menu.png")
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
