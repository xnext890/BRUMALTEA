import pathlib
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":720})
    errs=set();pg.on("pageerror",lambda e:errs.add(str(e)[:300]))
    await pg.goto(INDEX);await pg.wait_for_timeout(400)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    r=await pg.evaluate("""(()=>{const bad=[];const BADRE=/undefined|NaN|\\[object|null\\b|\\$\\{/;
      const dup=[...document.querySelectorAll('[id]')].map(e=>e.id).filter((x,i,a)=>a.indexOf(x)!==i);
      const seen=new Set();
      const grab=(tag)=>{const t=document.getElementById('dialog').innerText||'';if(BADRE.test(t)&&!seen.has(t)){seen.add(t);bad.push(tag+': '+t.replace(/\\n/g,' | ').slice(0,160));}};
      const drain=(tag)=>{let n=0;while(!document.getElementById('dialog').hidden&&n<80){n++;if(typing)finishType(dq.choices);grab(tag);if(dq&&dq.choices){pickChoice(dq.choices.length-1);continue;}advance();}};
      S.house='tormenta';S.spells=['chispa','rafaga','pasmo','escudo','luz','paso','nana','lanza','desvelo','llama'];S.flags.side='island';S.lvl=10;
      for(const mode of [0,1,2,3]){
        const states=[{},{m1:5},{m1:10,done:1},{c4:1},{c5:3},{c6:5},{c7:4}];
        for(const stt of states){
          for(const id in QUESTS)Qs[id]=Qs[id]||{stage:0,prog:0,done:false};
          for(const k in stt){if(Qs[k]&&k!=='done'){Qs[k].stage=stt[k];}}
          for(const h of [8,14,21]){S.minutes=h*60;
            for(const id in TALK){try{TALK[id]();drain('talk '+id+' s'+JSON.stringify(stt)+' h'+h);}catch(e){bad.push('THROW '+id+': '+e.message)}}
            for(const o of objects){const f=OBJ_ACT[o.kind];if(!f||/stairs|piano|bed/.test(o.kind))continue;try{f(o);drain('obj '+o.kind);}catch(e){bad.push('THROW obj '+o.kind+': '+e.message)}}
            for(const sel of ['shop','rite','cls']){const e=document.getElementById(sel);if(e&&!e.hidden){try{if(sel==='shop')closeShop();else if(sel==='cls')clsClose();else e.hidden=true}catch(_){}}}
            pauseFlag=false;}
        }break;}
      return {dup,bad:bad.slice(0,40),n:bad.length}})()""")
    print(r);print(errs);await b.close()
asyncio.run(main())
