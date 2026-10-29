# utilidades compartidas por las pruebas
HELP="""
window.__drain = () => { let n=0; while(!document.getElementById('dialog').hidden && n<80){ n++;
   if(typing){ finishType(dq.choices); continue; }
   if(dq && dq.choices){ pickChoice(0); continue; }
   advance(); } return n; };
window.__go=(x,y,m,dir)=>{S.px=x*16+8;S.py=y*16+12;S.minutes=m*60;S.dir=dir||'down';camInit=false;resetParty&&resetParty();};
0;
"""
