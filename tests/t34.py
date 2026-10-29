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
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};S.house='raiz';S.flags.side='island';S.spells=['chispa','rafaga','pasmo'];S.lvl=8;S.maxHearts=8;S.hearts=8;S.lunas=100;ensureX();Qs.q_juncia={stage:99,prog:0,done:true};S.x.f.teo='va'")
    for k,(x,y) in {"taberna":(1411,24),"maran":(1175,114),"capilla":(1128,81),"choza":(1093,16),"ermita":(1280,11)}.items():
      await E(f"__go({x},{y},14,'up')");await pg.wait_for_timeout(250);await pg.keyboard.down("w");await pg.wait_for_timeout(700);await pg.keyboard.up("w");await pg.wait_for_timeout(1500);await E("__drain()");await pg.wait_for_timeout(1200)
      a=await E("areaOfXY(S.px,S.py)");await pg.screenshot(path=SCR+f"I_{k}.png")
      await pg.keyboard.down("s");await pg.wait_for_timeout(1500);await pg.keyboard.up("s");await pg.wait_for_timeout(900)
      print(k,a,"->",await E("areaOfXY(S.px,S.py)"))
    print(await E("OBJ_ACT.baulmaran();__drain();S.x.f.diarioU"))
    # quest
    print(await E("TALK.juncia();__drain();qStage('q_velados')"))
    await E("__go(1182,30,23)");await pg.wait_for_timeout(600);print("st",await E("qStage('q_velados')"))
    await E("OBJ_ACT.tiendagrande();__drain()");await pg.wait_for_timeout(500);print("boss",await E("[qStage('q_velados'),foes.filter(f=>f.type==='teniente').length,foes.filter(f=>f.type==='velado').length]"))
    await pg.screenshot(path=SCR+"I_boss.png")
    await E("for(const f of foes)if(f.type==='teniente')killFoe(f)");await pg.wait_for_timeout(900);await E("__drain()")
    print(await E("OBJ_ACT.tiendagrande();if(typing)finishType(dq.choices);while(!(dq&&dq.choices)){advance();if(typing)finishType(dq.choices);}pickChoice(0);__drain();[qStage('q_velados'),S.inv.cartasV]"))
    print(await E("TALK.albarran();__drain();[qStage('q_velados'),S.x.f.albarranQuema]"))
    for n in ["rita","ruperto","nemesio","ofelia","lucas"]: print(n,await E(f"TALK.{n}();const t=document.querySelector('#dialog').innerText.slice(0,40);__drain();t"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
