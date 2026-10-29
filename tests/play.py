import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright

SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"

HELP = """
window.__drain = () => { let n=0; while(!document.getElementById('dialog').hidden && n<60){ n++;
   if(typing){ finishType(dq.choices); continue; }
   if(dq && dq.choices){ pickChoice(0); continue; }
   advance(); } return n; };
window.__talk = (id) => { const n=NPC[id]; S.px=n.px; S.py=n.py+14; S.dir='up'; TALK[id](); return __drain(); };
window.__st = () => JSON.stringify(Object.fromEntries(Object.entries(Qs).map(([k,v])=>[k, v.done?'done':v.stage+'/'+v.prog])));
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 720})
        errs = []
        pg.on("pageerror", lambda e: errs.append(f"pageerror: {e}"))
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type == "error" and "TUNNEL" not in m.text else None)
        await pg.goto(INDEX)
        await pg.wait_for_timeout(500)
        await pg.click("#btn-new")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR + "p_creator.png")
        await pg.click("#cc-go")
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=SCR + "p_intro.png")
        await pg.evaluate(HELP)
        await pg.evaluate("(()=>{const _d=window.__drain;window.__drain=()=>{let n=0,k=0;do{k=_d();n+=k;const c=document.getElementById('casas');if(c&&!c.hidden){document.getElementById('casas-go').click();k=1;}}while(k>0&&n<400);return n;};})()")
        await pg.evaluate("__drain()")
        await pg.evaluate("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:0,prog:0,done:false};S.tracked='m1';S.flags.side='island';S.flags.friends=true;S.px=50*16+8;S.py=88*16+4;camInit=false;placeAnselmo();resetParty();refreshTracker()")
        await pg.evaluate("S.px=50*16+8;S.py=87*16+12;S.dir='up';resetParty()")
        await pg.screenshot(path=SCR + "p_dock.png")
        await pg.keyboard.press("e"); await pg.wait_for_timeout(600)
        await pg.screenshot(path=SCR + "p_dialog.png")
        await pg.evaluate("__drain()")
        print("after anselmo", await pg.evaluate("__st()"))
        await pg.evaluate("__talk('anselmo')")  # side quest
        await pg.evaluate("__talk('albarran')")
        # mirror
        await pg.evaluate("S.px=24*16+8;S.py=44*16+12;S.dir='left'; OBJ_ACT.mirror()")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR + "p_quiz.png")
        await pg.evaluate("__drain()")
        print("after mirror", await pg.evaluate("__st()"), await pg.evaluate("S.house"))
        await pg.evaluate("__talk('albarran')")
        await pg.evaluate("__talk('mirlo')")
        print("after mirlo", await pg.evaluate("__st()"), await pg.evaluate("S.spells"))
        # shoot dummies: stand below each and cast up
        for i in range(3):
            await pg.evaluate(f"(()=>{{const o=objects.filter(o=>o.kind==='dummy'&&[905,918,931].includes(o.x)&&o.y<30)[{i}];S.px=o.x*16+8;S.py=(o.y+2)*16+12;S.dir='up';S.cd=0;S.mp=10;cast();}})()")
            await pg.wait_for_timeout(450)
        await pg.screenshot(path=SCR + "p_aula.png")
        print("after dummies", await pg.evaluate("__st()"))
        await pg.evaluate("__talk('mirlo')")
        await pg.evaluate("__talk('ines')")
        print("after ines", await pg.evaluate("__st()"))
        # side quests
        for npc in ("lia", "tobias", "bruno", "ines"):
            await pg.evaluate(f"__talk('{npc}')")
        print("sides", await pg.evaluate("__st()"))
        # forest + boss
        await pg.evaluate("S.px=87*16;S.py=28*16;S.minutes=23*60")
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=SCR + "p_forest.png")
        await pg.evaluate("for(const e of enemies){hitEnemy(e,20,0,0)}")
        await pg.wait_for_timeout(300)
        # collect fragments by teleport
        await pg.evaluate("for(const p of pickups){ if(p.kind==='frag'&&pickVisible(p)){ collect(p);} }")
        print("frags", await pg.evaluate("__st()"), await pg.evaluate("S.flags.bossDead"))
        await pg.evaluate("S.px=1045*16+8;S.py=29*16+4;S.dir='up';S.minutes=12*60")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR + "p_door.png")
        await pg.keyboard.press("e"); await pg.wait_for_timeout(200)
        await pg.evaluate("__drain()")
        print("door", await pg.evaluate("__st()"))
        await pg.evaluate("S.px=1045*16;S.py=13*16+12;S.dir='up'; OBJ_ACT.piano()")
        await pg.evaluate("__drain()")
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=SCR + "p_end.png")
        await pg.click("#end-go")
        await pg.keyboard.press("q"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR + "p_menu.png")
        await pg.click("[data-tab=coleccion]"); await pg.wait_for_timeout(200)
        await pg.screenshot(path=SCR + "p_menu2.png")
        await pg.click("[data-tab=mapa]"); await pg.wait_for_timeout(200)
        await pg.screenshot(path=SCR + "p_map.png")
        print("final", await pg.evaluate("__st()"), await pg.evaluate("S.estampas.length"))
        # reload -> continue
        await pg.reload(); await pg.wait_for_timeout(500)
        vis = await pg.evaluate("!document.getElementById('btn-continue').hidden")
        print("continue visible", vis)
        await pg.click("#btn-continue"); await pg.wait_for_timeout(300)
        print("after load", await pg.evaluate("__st ? 1 : 0") if False else await pg.evaluate("JSON.stringify(Object.keys(Qs))"), await pg.evaluate("S.house"))
        print("\n".join(errs) if errs else "no errors")
        await b.close()

asyncio.run(main())
