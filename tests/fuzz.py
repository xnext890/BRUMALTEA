import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
H='''window.__drain=()=>{let n=0;while(!document.getElementById('dialog').hidden&&n<80){n++;if(typing){finishType(dq.choices);continue;}if(dq&&dq.choices){pickChoice(dq.choices.length-1);continue;}advance();}return n;};'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
        errs=[];pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
        pg.on("console",lambda m: errs.append(m.text) if m.type=="error" and "TUNNEL" not in m.text else None)
        await pg.goto(INDEX);await pg.wait_for_timeout(400)
        await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(400)
        await pg.evaluate(H)
        m0=await pg.evaluate("__drain();const a=S.minutes;a")
        await pg.wait_for_timeout(2000)
        print("frozen prologue", m0, await pg.evaluate("S.minutes"))
        # every NPC talk, every object, at several hours and stages
        for stage in [0,3,7,10]:
            for hour in [8,12,19,23]:
                r=await pg.evaluate(f"""(()=>{{Qs.m0={{stage:4,prog:0,done:true}};Qs.m1={{stage:{stage},prog:0,done:false}};S.house='tormenta';S.spells=['chispa','rafaga'];S.flags.side='island';S.minutes={hour}*60;let n=0,bad=[];
                  for(const id in TALK){{try{{const npc=npcs.find(x=>x.id===id)||NPC[id];if(npc){{S.px=npc.px;S.py=npc.py+14;}}TALK[id]();__drain();n++;}}catch(e){{bad.push(id+':'+e.message)}}}}
                  for(const o of objects){{const f=OBJ_ACT[o.kind];if(!f||o.kind==='stairsDown'||o.kind==='stairsUp'||o.kind==='piano'||o.kind==='bed')continue;try{{f(o);__drain();n++;}}catch(e){{bad.push(o.kind+':'+e.message)}}}}
                  closeShop&&!document.getElementById('shop').hidden&&closeShop();if(!document.getElementById('cls').hidden)clsClose();if(!document.getElementById('rite').hidden){{document.getElementById('rite').hidden=true;pauseFlag=false;}}
                  return [n,bad]}})()""")
                await pg.evaluate("document.getElementById('shop').hidden||closeShop();document.getElementById('creator').hidden||(document.getElementById('creator').hidden=true);pauseFlag=false")
                if r[1]: print(stage,hour,r)
        # menus
        for t in ["misiones","progreso","mochila","grimorio","coleccion","copa","mapa"]:
            await pg.evaluate(f"openMenu('{t}')");await pg.wait_for_timeout(50)
        await pg.evaluate("closeMenu()")
        # simulate 2 game days at high speed in different places
        for (x,y) in [(50,40),(126,30),(40,115),(88,20)]:
            await pg.evaluate(f"S.px={x}*16+8;S.py={y}*16+12;camInit=false;S.flags.side={'\"mainland\"' if x>100 else '\"island\"'}")
            for k in range(60):
                await pg.evaluate("S.minutes+=48;if(S.minutes>=1440){S.minutes-=1440;S.day++;onNewDay();}__drain();pauseFlag=false")
                await pg.wait_for_timeout(25)
        # sleep
        await pg.evaluate("S.flags.side='island';S.house='raiz';S.minutes=22*60;const sb=myBedSpot();S.px=sb[0]*16+8;S.py=sb[1]*16+12;OBJ_ACT.bed(objects.find(o=>o.house==='raiz'&&o.first));finishType(dq.choices);pickChoice(0)")
        await pg.wait_for_timeout(3000)
        print("after sleep",await pg.evaluate("[S.day,fmtTime(),S.hearts]"))
        print("\n".join(sorted(set(errs))) or "no errors")
        await b.close()
asyncio.run(main())
