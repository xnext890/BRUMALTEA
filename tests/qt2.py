import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    r=await pg.evaluate("""(()=>{const bad=[];S.house='tormenta';S.flags.side='island';S.px=50*16;S.py=40*16;
      for(const q of Object.keys(QUESTS)){const Q=QUESTS[q];for(let st=0;st<Q.stages.length;st++){Qs[q]={stage:st,prog:0,done:false};const s=Q.stages[st];
        let t=null;try{t=questTarget(q)}catch(e){t='ERR '+e.message}
        if(!t||typeof t==='string'||isNaN(t.x)||isNaN(t.y))bad.push(q+'#'+st+' to='+s.to+' -> '+JSON.stringify(t));
        }
        delete Qs[q];}
      return bad})()""")
    print(len(r));print("\n".join(r[:60]));await b.close()
asyncio.run(main())
