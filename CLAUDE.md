# Brumaltea

RPG de academia de magia en píxel-art, en español. Hoy es un juego para un jugador en un solo archivo (`index.html`, ~1,1 MB, JavaScript vanilla sobre canvas, sin build). El objetivo es convertirlo en un MMORPG siguiendo [docs/PLAN_MMORPG.md](docs/PLAN_MMORPG.md); el debate de la mesa de agentes está en [docs/MESA_AGENTES.md](docs/MESA_AGENTES.md).

## Cómo trabajar aquí
- Jugar en local: `py -m http.server 8000` en la raíz y abrir `http://localhost:8000` (no `127.0.0.1`: el inicio de sesión con Google solo acepta `localhost`).
- Pruebas: `py tests/run_all.py` (todas) o `py tests/run_all.py t43 play` (algunas). Requieren `pip install playwright` y `playwright install chromium`.
- `index.html` es enorme: busca con Grep y lee por rangos, no entero.
- El código se organiza en módulos sucesivos que parchean funciones globales (`const _x=fn;fn=function(){_x();...}`). Al envolver, conserva y llama a la versión anterior.
- Los ids de personaje (`addNPC({id})`, `KEEPERS`) deben ser únicos: un id repetido sustituye el `TALK` del otro personaje.
- El ID de cliente de Google en la `<meta name="brumaltea-google-client-id">` es público por diseño; nunca subas el secreto del cliente.

## Agentes
Hay un agente por rol en `.claude/agents/` (game-director, game-designer, backend-engineer, gameplay-programmer, world-designer, npc-ai-designer, ui-ux-designer, economy-designer, qa-engineer, devops-engineer). Cada uno solo edita su área de propiedad, definida en la sección «Propiedad por rol» del plan. Mientras `index.html` sea un monolito, solo un cambio sobre él a la vez.
