"""Ejecuta todas las pruebas y falla si alguna lanza error de página o excepción.
Uso:  python3 tests/run_all.py [nombre ...]      (requiere: pip install playwright && playwright install chromium)"""
import subprocess,sys,pathlib,re
d=pathlib.Path(__file__).resolve().parent
ALL=["fuzz","play","city","cls","t12","t26","t31","t34","t36","t37","t38","t39","t40","t41","t42","t43","qt","qt2","ex","txt","rt","sweep","fps2"]
names=sys.argv[1:] or ALL
bad=[]
for n in names:
    r=subprocess.run([sys.executable,str(d/(n+".py"))],capture_output=True,text=True,timeout=900,cwd=str(d))
    out=r.stdout+r.stderr
    fail=r.returncode!=0 or "Traceback" in out or re.search(r"^(PE |pageerror|ERR )",out,re.M)
    if n=="qt2" and "\n0\n" not in "\n"+out.split("\n",1)[0]+"\n":fail=True
    if n=="qt" and "'nbad': 0" not in out:fail=True
    print(("FALLA " if fail else "ok    ")+n)
    if fail:bad.append(n);print("\n".join(out.splitlines()[-8:]))
sys.exit(1 if bad else 0)
