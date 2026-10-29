import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio,sys,os
from playwright.async_api import async_playwright
from helpers import HELP
SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"
END=os.environ.get("END","tercera")
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e.stack)[:600]))
    await pg.goto(INDEX);await pg.wait_for_timeout(500)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    E=pg.evaluate
    D="__drain();if(SC37&&document.querySelector('#dialog').hidden)hideScene();"
    st=lambda: E("[qStage('c7'),Qs.c7&&Qs.c7.prog,S.spells.slice(-2).join(),pauseFlag,areaOfXY(S.px,S.py),Math.round(S.px/16),Math.round(S.py/16)]")
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};['c2','c3','c4','c5','c6','q_mirador'].forEach(q=>Qs[q]={stage:99,prog:0,done:true});S.house='raiz';S.flags.friends=true;S.flags.rival1=true;S.lvl=26;ensureX();S.x.curso=7;S.x.f.nebulario='escuchar';S.x.f.bastianTold=1;S.x.f.bastianPromesa=2;S.x.f.bastianIdo=1;S.x.f.bastianDuda=1;S.x.f.iriaDecision=1;S.x.f.valcDecision='cubrir';S.spells=['chispa','rafaga','pasmo','escudo','luz','paso','nana','lanza','desvelo'];Qs.c7={stage:0,prog:0,done:false};S.x.notas=[0,1,2,3,4,5,6,7,8,9,10,11,12,13];for(const k of AM_ID)am37()[k].p=80")
    await E("TALK.albarran();"+D);print("intro",await st())
    await E("S.px=NPC.trastin.px+10;S.py=NPC.trastin.py");await pg.wait_for_timeout(500);await E(D);print("tras",await st(),await E("S.x.f.trastinBien"))
    await E("talkFriend(NPC.iria);"+D);print("iria",await st())
    await E("TALK.valcarcel();"+D);print("valc",await st())
    await E("__go(LAGO41[0],LAGO41[1],22)");await pg.wait_for_timeout(800);await pg.screenshot(path=SCR+"L_lago.png");await E(D);await pg.wait_for_timeout(1500);await E(D);print("lago",await st(),await E("S.x.f.bastianVuelve"))
    await pg.screenshot(path=SCR+"L_entry.png")
    await E("S.spell=S.spells.indexOf('llama');S.mp=30;S.cd=0;__go(1664,98,22,'up')");await pg.wait_for_timeout(300);await E("cast()");await pg.wait_for_timeout(300)
    print("burn",await E("objects.filter(o=>o.kind==='nieblaDensa').map(o=>!!o.gone)"))
    await E("__go(1664,90,22)");await pg.wait_for_timeout(700);await E(D);print("past",await st())
    await E("__go(1664,70,22)");await pg.wait_for_timeout(300);await pg.screenshot(path=SCR+"L_ecos.png")
    for (x,y) in [(1641,62),(1689,62),(1646,77)]:
      await E(f"__go({x},{y},22);S.spell=S.spells.indexOf('desvelo');S.mp=30;S.cd=0;cast()");await pg.wait_for_timeout(200)
      await E("for(const o of objects)if(o.kind==='recuerdo'&&!o.hidden&&!o.got)OBJ_ACT.recuerdo(o);"+D)
    print("recuerdos",await st())
    await E("__go(1664,30,22,'up')");await pg.wait_for_timeout(800);await E(D);await pg.wait_for_timeout(800);print("neb",await st(),await E("foes.filter(f=>f.type==='nebulario').length"))
    await pg.wait_for_timeout(1200);await pg.screenshot(path=SCR+"L_boss.png")
    await E("const n=foes.find(f=>f.type==='nebulario');hitFoe(n,5,0,0)");print("velo",await E("foes.find(f=>f.type==='nebulario').hp"))
    await E("const n=foes.find(f=>f.type==='nebulario');S.px=n.px;S.py=n.py+30;S.spell=S.spells.indexOf('llama');S.mp=30;S.cd=0;cast()");print("burned",await E("foes.find(f=>f.type==='nebulario').velo"))
    await E("const n=foes.find(f=>f.type==='nebulario');n.ph1=1;n.ph2=1;hitFoe(n,9999,0,0);"+D);await pg.wait_for_timeout(500);await E(D);print("down",await st())
    await E(f"__go(1664,9,22,'up');OBJ_ACT.sello();");await pg.wait_for_timeout(300);print("opts",await E("dq&&dq.lines.length"),await E("(()=>{while(dq&&!dq.choices){if(typing)finishType(dq.choices);advance()}return dq&&dq.choices.map(c=>c[0])})()"))
    idx={"ancla":0,"rotura":1,"tercera":2}[END]
    await E(f"pickChoice({idx})");
    for i in range(6):
      await pg.wait_for_timeout(700);await E("__drain()")
    await pg.wait_for_timeout(1500);await pg.screenshot(path=SCR+f"L_cred_{END}.png");print("final",await E("[S.x.f.final,!document.querySelector('#creditos').hidden]"))
    await E("document.querySelector('#cred-go').click()");await pg.wait_for_timeout(1500);print("post",await st(),await E("[Qs.c7.done]"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
