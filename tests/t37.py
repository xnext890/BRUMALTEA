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
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e.stack)[:600]));pg.on("console",lambda m:errs.append(m.text) if m.type=="warning" else None)
    await pg.goto(INDEX);await pg.wait_for_timeout(500)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    E=pg.evaluate
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:99,prog:0,done:true};S.house='raiz';S.flags.friends=true;S.flags.rival1=true;S.lvl=8;ensureX();S.inv.musgo=2;S.inv.seda=1;S.inv.baya=1")
    print("lv",await E("[amLv('iria'),sceneAvail('iria')]"))
    await E("amAdd('iria',10)");print("lv2",await E("[amLv('iria'),sceneAvail('iria'),npcMarker(NPC.iria)]"))
    await E("talkFriend(NPC.iria)");await pg.wait_for_timeout(1200);await pg.screenshot(path=SCR+"F_scene.png")
    await E("__drain()");print("seen",await E("am37().iria.seen"))
    await E("talkFriend(NPC.iria)");await pg.wait_for_timeout(300);print("dlg",await E("document.querySelector('#dialog').innerText.slice(0,120)"))
    await E("__drain()");await E("giveGift('iria','musgo')");await E("__drain()");print("gift",await E("[am37().iria.p,am37().iria.taste,S.inv.musgo]"))
    await E("faint()");await pg.wait_for_timeout(3000);print("pend",await E("am37().bastian.pend"))
    i=0
    for k in ["torre","lago","biblioteca","cocina","nieve","comedor","anden","ala","cripta","marisma","puerto","pazo","niebla"]:
      await E(f"showScene('{k}',[{{who:'player',x:150,y:150,dir:'down'}},{{who:'iria',x:110,y:152,dir:'right'}},{{who:'bastian',x:190,y:152,dir:'left',ghost:{'true' if k=='ala' else 'false'}}}],'{k}','prueba');say([['','x']])");await pg.wait_for_timeout(500)
      await pg.screenshot(path=SCR+f"S_{k}.png");await E("__drain();hideScene()")
    await E("openMenu('amigos')");await pg.wait_for_timeout(400);await pg.screenshot(path=SCR+"F_menu.png")
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
