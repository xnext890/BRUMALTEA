import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=set();pg.on("pageerror",lambda e:errs.add(str(e.stack or e)[:500]))
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    r=await pg.evaluate("""(async()=>{const bad=[];const sl=ms=>new Promise(r=>setTimeout(r,ms));
      const spots={};for(let y=0;y<H;y+=3)for(let x=0;x<W;x+=3){if(!walk[y*W+x])continue;const a=areaOfXY(x*16+8,y*16+12);if(!spots[a])spots[a]=[x,y];}
      S.house='tormenta';S.spells=['chispa','rafaga','pasmo','escudo','luz','paso','nana','lanza','desvelo','llama'];S.flags.side='island';
      for(const q of Object.keys(QUESTS)){for(let st=0;st<QUESTS[q].stages.length;st++){
        Qs[q]={stage:st,prog:0,done:false};S.tracked=q;
        for(const a of Object.keys(spots)){S.px=spots[a][0]*16+8;S.py=spots[a][1]*16+12;camInit=false;
          for(const h of [3,13]){S.minutes=h*60;
            try{refreshTracker();updateHUD();}catch(e){bad.push('hud '+q+st+e.message)}
            await sl(8);}}
        if(!document.getElementById('dialog').hidden)__dr();
      }delete Qs[q];}
      return bad.slice(0,10)})()""".replace("__dr()","(()=>{let n=0;while(!document.getElementById('dialog').hidden&&n<80){n++;if(typing){finishType(dq.choices);continue;}if(dq&&dq.choices){pickChoice(dq.choices.length-1);continue;}advance();}})()"))
    print(r);print("\n".join(sorted(errs)) or "no errors");await b.close()
asyncio.run(main())
