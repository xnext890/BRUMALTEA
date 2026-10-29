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
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};S.house='raiz';S.flags.friends=true;S.flags.rival1=true;S.lvl=8;ensureX();S.x.f.valcDecision='cubrir';S.x.f.noraGone=1;S.flags.side='island'")
    # events for several days
    for d in range(6):
      await E(f"S.day={10+d};X42().ev42.day=-1;__go(980,30,9)");await pg.wait_for_timeout(400);await E(D)
      print("day",10+d,await E("[X42().ev42.k,document.querySelector('#tracker').innerText.includes('Evento')]"))
    # cartas event
    await E("S.day=40;X42().ev42.day=-1;");await pg.wait_for_timeout(300)
    k=await E("X42().ev42.k");print("ev40",k)
    # force cartas
    await E("const E=X42().ev42;E.k='cartas';E.done=false;E.got=0;EV42.cartas.start()");
    await E("for(const p of pickups.filter(p=>p.kind==='carta42'&&pickVisible(p)))collect(p)");await pg.wait_for_timeout(300)
    await E("TALK.fidel();"+D);print("cartas",await E("[X42().ev42.done,S.lunas]"))
    # letter sunday
    await E("S.day=6;__go(980,30,9)");await pg.wait_for_timeout(500);await E(D);print("carta",await E("X42().diario.filter(e=>e.k==='carta').length"))
    # rumors
    await E("window._mr=Math.random;Math.random=()=>0.1");r=await E("talkStudent(students[3]);const t=document.querySelector('#dialog').innerText;__drain();t");print("rumor",r[:120])
    await E("Math.random=window._mr")
    # curfew
    await E("__go(PBR.COR[0]+20,PBR.COR[1]+2,23.5);foes.length=0");await pg.wait_for_timeout(600);print("vig",await E("[vigOn42(),VIG42.map(v=>Math.round(v.sus*100))]"))
    await E("const v=VIG42[0];S.px=v.x+(DIRV[v.dir][0]*30);S.py=v.y+(DIRV[v.dir][1]*30)");await pg.wait_for_timeout(1500);await pg.screenshot(path=SCR+"M_vig.png");await E(D);await pg.wait_for_timeout(1500);print("caught",await E("[X42().f.pillado,areaOfXY(S.px,S.py)]"))
    # exam
    await E("Qs.m1={stage:99,prog:0,done:true};S.x.curso=1;S.lvl=10;endCurso()");await pg.wait_for_timeout(500);await pg.screenshot(path=SCR+"M_exam.png")
    await E(D);await pg.wait_for_timeout(4000);await E(D);await pg.wait_for_timeout(3000);await E(D);print("exam",await E("[JSON.stringify(X42().exam),ensureX().curso]"))
    await E("openMenu('diario')");await pg.wait_for_timeout(400);await pg.screenshot(path=SCR+"M_diario.png")
    print("his",await E("(()=>{S.x.curso=5;return hisBank().length})()"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
