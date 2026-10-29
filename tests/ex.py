import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    r=await pg.evaluate("""(()=>{const bad=[];for(const a in AREA_EXITS)for(const b in AREA_EXITS[a]){const [x,y]=AREA_EXITS[a][b];
      const ar=areaOfXY(x*16+8,y*16+8);const w=walk[y*W+x];const near=walkableNear(x,y);
      if(!w&&!near)bad.push(a+'->'+b+' '+x+','+y+' no walk');
      else if(ar!==a)bad.push(a+'->'+b+' coord in '+ar);}
      // all objects/npcs on walkable or reachable tile
      const stuck=[];for(const n of npcs){const tx=Math.floor(n.px/16),ty=Math.floor(n.py/16);if(!walk[ty*W+tx])stuck.push(n.id+'@'+tx+','+ty)}
      return {bad,stuck:stuck.slice(0,20),ns:stuck.length}})()""")
    print(r);await b.close()
asyncio.run(main())
