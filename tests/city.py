import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"
H='''window.__drain=()=>{let n=0;while(!document.getElementById('dialog').hidden&&n<80){n++;if(typing){finishType(dq.choices);continue;}if(dq&&dq.choices){pickChoice(0);continue;}advance();}return n;};
window.__st=()=>JSON.stringify(Object.fromEntries(Object.entries(Qs).map(([k,v])=>[k,v.done?'done':v.stage+'/'+v.prog])));
window.__go=(x,y)=>{S.px=x*16+8;S.py=y*16+12;camInit=false;};'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
        errs=[];pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
        pg.on("console",lambda m: errs.append(m.text) if m.type=="error" and "TUNNEL" not in m.text else None)
        await pg.goto(INDEX);await pg.wait_for_timeout(400)
        await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.fill("#cc-name","Lucía");await pg.click("#cc-go");await pg.wait_for_timeout(500)
        await pg.evaluate(H)
        await pg.screenshot(path=SCR+"c_port.png")
        await pg.evaluate("__drain()")
        await pg.evaluate("__go(114,67);S.dir='up';TALK.anselmo;talkFriend(friends[0]);__drain()")
        print("met",await pg.evaluate("__st()"))
        await pg.evaluate("__go(125,57);S.dir='left';OBJ_ACT.farola();__drain()")
        print("alley",await pg.evaluate("__st()"))
        await pg.evaluate("__go(126,48);S.minutes=17*60")
        await pg.wait_for_timeout(700);await pg.screenshot(path=SCR+"c_streetC.png")
        # visit shops
        for key in ["sastreria","libreria","caldereria","cielo","herbolario"]:
            await pg.evaluate(f"(()=>{{const B=SHOP['{key}'];__go(B.door[0],B.y1-1);S.dir='up';keeperTalk(npcs.find(n=>n.shop==='{key}'));}})()")
            await pg.wait_for_timeout(250)
            if key=="caldereria": await pg.screenshot(path=SCR+"c_shop.png")
            await pg.evaluate("document.querySelectorAll('#shop .sitems button').forEach(b=>{if(!b.disabled&&/Recoger/.test(b.textContent))b.click()})")
            await pg.evaluate("closeShop()")
        await pg.wait_for_timeout(300);await pg.screenshot(path=SCR+"c_inshop.png")
        print("list",await pg.evaluate("__st()"),await pg.evaluate("listCount()"))
        # madriguera adopt
        await pg.evaluate("(()=>{const B=SHOP.madriguera;__go(B.door[0],B.y1-1);keeperTalk(npcs.find(n=>n.shop==='madriguera'));})()")
        await pg.wait_for_timeout(200)
        await pg.click("#shop .sitems button");await pg.wait_for_timeout(200)
        await pg.screenshot(path=SCR+"c_pets.png")
        await pg.evaluate("document.querySelectorAll('.petcard .pick')[1].click()")
        await pg.evaluate("[...document.querySelectorAll('#shop button')].find(b=>b.textContent==='Adoptar').click()")
        await pg.evaluate("closeShop()")
        # wand
        await pg.evaluate("__go(126,12);S.dir='up';keeperTalk(npcs.find(n=>n.shop==='varitas'));__drain()")
        await pg.wait_for_timeout(300)
        for i in range(6):
            await pg.click("#rite-opts button:nth-child(%d)"%(1+(i*2)%6));await pg.wait_for_timeout(120)
        await pg.screenshot(path=SCR+"c_rite_wood.png")
        await pg.click("#rite-opts button");await pg.wait_for_timeout(2800)
        await pg.screenshot(path=SCR+"c_rite_gem.png")
        await pg.wait_for_timeout(3600)
        await pg.screenshot(path=SCR+"c_rite_wand.png")
        await pg.click("#rite-opts button");await pg.wait_for_timeout(300)
        await pg.evaluate("__drain()")
        print("wand",await pg.evaluate("__st()"),await pg.evaluate("JSON.stringify([S.look.wand,S.look.gem,S.look.wandNote,S.look.wandMark])"))
        await pg.evaluate("__go(126,22);S.minutes=21*60");await pg.wait_for_timeout(800);await pg.screenshot(path=SCR+"c_plaza_night.png")
        await pg.evaluate("__go(121,73);S.dir='right';TALK.anselmo();__drain()");await pg.wait_for_timeout(4200);await pg.screenshot(path=SCR+"c_train.png");await pg.click("#train-skip");await pg.wait_for_timeout(500)
        await pg.evaluate("__drain()")
        print("island",await pg.evaluate("__st()"),await pg.evaluate("[S.flags.side,Math.round(S.px/16),Math.round(S.py/16),S.lunas]"))
        await pg.screenshot(path=SCR+"c_island.png")
        await pg.evaluate("TALK.anselmo();__drain()")
        print("m1",await pg.evaluate("__st()"))
        await pg.keyboard.press("q");await pg.wait_for_timeout(200);await pg.click('[data-tab="mochila"]');await pg.wait_for_timeout(200);await pg.screenshot(path=SCR+"c_mochila.png")
        print("\n".join(errs) or "no errors")
        await b.close()
asyncio.run(main())
