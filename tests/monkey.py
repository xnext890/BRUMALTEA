import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio,random,sys
from playwright.async_api import async_playwright
HELP='''window.__drain=()=>{let n=0;while(!document.getElementById('dialog').hidden&&n<80){n++;if(typing){finishType(dq.choices);continue;}if(dq&&dq.choices){pickChoice(dq.choices.length-1);continue;}advance();}return n;};'''
SEED=int(sys.argv[1]) if len(sys.argv)>1 else 1
async def main():
  random.seed(SEED)
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=set();pg.on("pageerror",lambda e:errs.add("PE "+str(e.stack or e)[:1100]))
    pg.on("console",lambda m:errs.add("CE "+m.text[:300]) if m.type=="error" and "TUNNEL" not in m.text and "googleapis" not in m.text and "ERR_" not in m.text else None)
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    E=pg.evaluate
    await E("S.house='tormenta';S.lvl=14;S.hearts=S.maxHearts=12;S.spells=['chispa','rafaga','pasmo','escudo','luz','paso','nana','lanza','desvelo','llama'];Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:0,prog:0,done:true};S.flags.side='island'")
    keys=["w","a","s","d","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," ","e","q","m","Escape","g","1","2","3","4","Enter"]
    pts=await E("(()=>{const o=[];for(let i=0;i<4000;i++){const x=(Math.random()*W)|0,y=(Math.random()*H)|0;if(walk[y*W+x])o.push([x,y]);}return o})()")
    stuck=0;last=None
    for step in range(900):
      r=random.random()
      if r<.55:
        k=random.choice(keys);await pg.keyboard.down(k);await pg.wait_for_timeout(random.randint(30,260));await pg.keyboard.up(k)
      elif r<.75:
        x,y=random.choice(pts);await E(f"S.px={x}*16+8;S.py={y}*16+12;camInit=false")
      elif r<.85:
        await E("S.minutes+=Math.floor(Math.random()*400);if(S.minutes>=1440){S.minutes-=1440;S.day++;onNewDay();}")
      elif r<.9:
        await E("__drain()")
      elif r<.94:
        await E("(()=>{const s=serialize();if(!loadGame(s))throw new Error('load failed');})()")
      elif r<.97:
        await E("(()=>{for(const t of ['misiones','progreso','mochila','grimorio','coleccion','copa','mapa'])try{openMenu(t)}catch(e){throw e}closeMenu();})()")
      else:
        await E("(()=>{const l=enemies.slice(0,3);for(const e of l)e.hp=0;S.hearts=Math.max(S.hearts,3)})()")
      if step%50==0:
        st=await E("[document.getElementById('dialog').hidden,document.getElementById('menu').hidden,S.hearts,S.day]")
        await E("pauseFlag=false;if(!document.getElementById('menu').hidden)closeMenu();__drain()")
      if errs and step%100==99:break
    print("seed",SEED,"steps done",step);print("\n".join(sorted(errs)) or "no errors");await b.close()
asyncio.run(main())
