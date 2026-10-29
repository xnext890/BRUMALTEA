import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    r=await pg.evaluate("""(()=>{const out={};const ids=Object.keys(QUESTS);const areas={};
      for(let y=0;y<H;y+=2)for(let x=0;x<W;x+=2){if(!walk[y*W+x])continue;const a=areaOfXY(x*16+8,y*16+12);areas[a]=areas[a]||[x,y];}
      const bad=[];
      for(const a in areas){S.px=areas[a][0]*16+8;S.py=areas[a][1]*16+12;
        for(const q of ids){Qs[q]=Qs[q]||{stage:0,prog:0,done:false};for(let st=0;st<QUESTS[q].stages.length;st++){Qs[q].stage=st;try{questTarget(q)}catch(e){bad.push(a+'/'+q+'#'+st+': '+e.message)}}}}
      return {areas:Object.keys(areas),links:typeof LINKS!=='undefined'?Object.keys(LINKS):null,bad:bad.slice(0,15),nbad:bad.length}})()""")
    print(r);await b.close()
asyncio.run(main())
