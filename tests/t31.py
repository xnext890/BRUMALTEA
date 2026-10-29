import pathlib
pathlib.Path(__file__).resolve().parent.joinpath("out").mkdir(exist_ok=True)
INDEX=pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
import asyncio
from playwright.async_api import async_playwright
from helpers import HELP
SCR=str(pathlib.Path(__file__).resolve().parent/"out")+"/"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1280,"height":800})
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e.stack)[:600]))
    await pg.goto(INDEX);await pg.wait_for_timeout(500)
    await pg.click("#btn-new");await pg.wait_for_timeout(200);await pg.click("#cc-go");await pg.wait_for_timeout(300)
    await pg.evaluate(HELP);await pg.evaluate("__drain()")
    E=pg.evaluate
    await E("Qs.m0={stage:4,prog:0,done:true};Qs.m1={stage:11,prog:0,done:true};S.house='raiz';S.flags.side='island';Object.assign(S.inv,{pocion:3,tonico:2,seta:24,flor:7,polvo:2,semilla:3,concha:5,ascua:2,baya:4,pelaje:3,libro:2,cebo:4});S.bag.bollo=2;S.flags.own_botas=true;__go(979,80,12);S.hearts=3")
    print("cap",await E("[bagUsed(),bagCap(),roomFor('seta',1),roomFor('seda',1)]"))
    await E("openMenu('mochila')");await pg.wait_for_timeout(700);await pg.screenshot(path=SCR+"MO_1.png")
    await E("document.querySelector('.slot.cons').click()");await pg.wait_for_timeout(200)
    await E("document.getElementById('mo-use')&&document.getElementById('mo-use').click()");await pg.wait_for_timeout(800)
    print("after use",await E("[S.hearts,S.inv.pocion,S.bag.bollo]"))
    await E("[...document.querySelectorAll('.slot')].find(s=>s.title==='Baya de brezo').click()");await pg.wait_for_timeout(200)
    await E("document.getElementById('mo-da').click()");await pg.wait_for_timeout(800)
    print("drop",await E("[S.inv.baya,S.x.ground.length]"))
    await E("closeMenu()");await pg.wait_for_timeout(1500);await pg.screenshot(path=SCR+"MO_ground.png")
    print("picked back",await E("[S.inv.baya,S.x.ground.length]"))
    # fill to capacity then herb pickup refused
    await E("S.inv.musgo=200");print("full",await E("[bagUsed(),bagCap(),roomFor('alga',1)]"))
    print("\n".join(errs) or "no errors");await b.close()
asyncio.run(main())
