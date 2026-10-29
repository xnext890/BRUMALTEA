import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"
H='''window.__drain=()=>{let n=0;while(!document.getElementById('dialog').hidden&&n<80){n++;if(typing){finishType(dq.choices);continue;}if(dq&&dq.choices){pickChoice(0);continue;}advance();}return n;};
window.__go=(x,y)=>{S.px=x*16+8;S.py=y*16+12;camInit=false;};'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
        errs=[];pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
        pg.on("console",lambda m: errs.append(m.text) if m.type=="error" and "TUNNEL" not in m.text else None)
        await pg.goto(INDEX);await pg.wait_for_timeout(400)
        await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(400)
        await pg.evaluate(H)
        await pg.evaluate("__drain();Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:7,prog:0,done:false};S.house='raiz';repaintHouseCarpet(HOUSES.raiz.col);S.spells=['chispa'];S.flags.side='island';S.flags.friends=true;S.day=2;S.minutes=8*60+30;S.look.wand='#8a5a33';S.look.gem='#3fb37a';placeAnselmo();__go(64,38);resetParty();placeStudentsNow();refreshTracker()")
        await pg.wait_for_timeout(600)
        print("class now",await pg.evaluate("JSON.stringify(classNow())"),await pg.evaluate("fmtTime()"))
        await pg.screenshot(path=SCR+"k_aula.png")
        await pg.evaluate("__go(64,38);S.dir='up';TALK.mirlo()");await pg.wait_for_timeout(200)
        await pg.evaluate("finishType(dq.choices);pickChoice(0)");await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR+"k_enc_intro.png")
        await pg.click("#cls-ctrl button");await pg.wait_for_timeout(300)
        # trace rune with mouse along checkpoints
        for r in range(3):
            cps=await pg.evaluate("CG.st.cps")
            box=await pg.evaluate("(()=>{const r=document.getElementById('cls-cv').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
            pts=[(box[0]+x/320*box[2],box[1]+y/180*box[3]) for x,y in cps]
            await pg.mouse.move(*pts[0]);await pg.mouse.down()
            for q in pts[1:]: await pg.mouse.move(*q,steps=3)
            if r==1: await pg.screenshot(path=SCR+"k_enc_play.png")
            await pg.mouse.up();await pg.wait_for_timeout(900)
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR+"k_enc_end.png")
        print("enc",await pg.evaluate("JSON.stringify([S.mastery,S.xp,S.lvl,S.classLog])"))
        await pg.click("#cls-ctrl button");await pg.wait_for_timeout(200)
        # pociones at 11
        await pg.evaluate("S.day=5;S.minutes=10*60+40;__go(46,57);S.dir='left'")
        await pg.wait_for_timeout(400);await pg.screenshot(path=SCR+"k_stairs.png")
        await pg.evaluate("OBJ_ACT.stairsDown()");await pg.wait_for_timeout(1500)
        await pg.screenshot(path=SCR+"k_bodegas.png")
        await pg.evaluate("__go(42,113);S.dir='up';TALK.grajal();finishType(dq.choices);pickChoice(0)");await pg.wait_for_timeout(200)
        await pg.click("#cls-ctrl button");await pg.wait_for_timeout(200)
        # solve recipe
        steps=await pg.evaluate("CG.st.steps")
        names={"seta":"Seta de luz","flor":"Flor de niebla","raiz":"Raíz de saúco","escama":"Escama de salamandra","polvo":"Polvo de estrella","sal":"Sal de mar"}
        for s in steps:
            if s["type"]=="ing": await pg.click(f"#cls-ctrl button:has-text('{names[s['k']]}')")
            elif s["type"]=="stir":
                for _ in range(s["n"]): await pg.click("#cls-ctrl button:has-text('%s')"%("derecha" if s["d"]=="der" else "izquierda"))
            else:
                await pg.click("#cls-ctrl button:has-text('Avivar')")
                await pg.screenshot(path=SCR+"k_poc_heat.png")
                for _ in range(200):
                    v=await pg.evaluate("CG.st.heat?CG.st.heat.v:-1")
                    if 0.68<v<0.76: break
                    await pg.wait_for_timeout(15)
                await pg.click("#cls-ctrl button:has-text('Avivar')")
            await pg.wait_for_timeout(120)
        await pg.wait_for_timeout(300);await pg.screenshot(path=SCR+"k_poc_end.png")
        await pg.click("#cls-ctrl button");await pg.wait_for_timeout(200)
        # herbologia: wednesday 11
        await pg.evaluate("S.day=6;S.minutes=10*60+50;__go(81,58);S.dir='up';TALK.tobias();finishType(dq.choices);pickChoice(0)");await pg.wait_for_timeout(200)
        await pg.click("#cls-ctrl button");await pg.wait_for_timeout(2500)
        await pg.screenshot(path=SCR+"k_her.png")
        await pg.evaluate("CG.t=999");await pg.wait_for_timeout(300);await pg.click("#cls-ctrl button")
        # astronomia: tuesday 21
        await pg.evaluate("S.day=3;S.minutes=20*60+40;__go(48,26);S.dir='up';TALK.vega();finishType(dq.choices);pickChoice(0)");await pg.wait_for_timeout(200)
        await pg.click("#cls-ctrl button");await pg.wait_for_timeout(400)
        for c in range(3):
            tg=await pg.evaluate("CG.st.target")
            box=await pg.evaluate("(()=>{const r=document.getElementById('cls-cv').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
            for x,y in tg:
                await pg.mouse.click(box[0]+x/320*box[2],box[1]+y/180*box[3]);await pg.wait_for_timeout(60)
            if c==0: await pg.screenshot(path=SCR+"k_ast.png")
            await pg.wait_for_timeout(800)
        await pg.wait_for_timeout(300);await pg.screenshot(path=SCR+"k_ast_end.png")
        await pg.click("#cls-ctrl button")
        print("after",await pg.evaluate("JSON.stringify([S.mastery,S.xp,S.lvl,S.cup.raiz,S.flags.llave,S.bancal])"))
        # chests & almacen
        await pg.evaluate("S.mastery.enc=200;applyUnlocks();__go(60,117);S.dir='right'")
        await pg.evaluate("S.py=117*16+12;S.px=60*16+8;interactables().find(i=>Math.abs(i.x-61*16-8)<2&&Math.abs(i.y-117*16-8)<2).fn();__drain()")
        await pg.wait_for_timeout(300)
        await pg.evaluate("OBJ_ACT.chest(objects.find(o=>o.cid==='almacen'));__drain()")
        print("almacen",await pg.evaluate("[get(61,117),S.flags.chest_almacen,S.lunas,S.inv.polvo]"))
        # menu progreso
        await pg.evaluate("__go(50,40)");await pg.keyboard.press("q");await pg.wait_for_timeout(200);await pg.click('[data-tab="progreso"]');await pg.wait_for_timeout(200)
        await pg.screenshot(path=SCR+"k_prog.png");await pg.keyboard.press("Escape")
        # shops interior
        for key in ["pasteleria","sastreria","libreria","varitas","madriguera","cielo"]:
            await pg.evaluate(f"(()=>{{S.flags.side='mainland';S.minutes=17*60;const B=SHOP['{key}'];__go(B.door[0],B.y1-1);S.dir='up';}})()")
            await pg.wait_for_timeout(900);await pg.screenshot(path=SCR+f"k_shop_{key}.png")
        await pg.evaluate("(()=>{const B=SHOP.herbolario;__go(B.door[0],B.y1-1);keeperTalk(npcs.find(n=>n.shop==='herbolario'));})()");await pg.wait_for_timeout(300)
        await pg.screenshot(path=SCR+"k_shopsell.png")
        print("\n".join(errs) or "no errors")
        await b.close()
asyncio.run(main())
