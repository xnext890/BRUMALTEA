# Brumaltea en línea: dictamen del Game Director

> Mientras preparaba este documento solo he leído archivos y no he modificado ninguno. Comprobé en el código las cifras sobre las que la mesa no se ponía de acuerdo:
> - `Math.random` aparece **345** veces.
> - `rect(` aparece **264** veces, contando definición y usos.
> - Hay **36** `S.lunas+=` y **10** `S.lunas-=`.
> - Hay **51** redefiniciones de `gameUpdate=function`.
> - En la copia de trabajo, `resize()` ya usa `w/640,h/360` (index.html:900) y `#cc-count` está vacío (línea 1807), aunque la etiqueta sigue ahí.
>
> Desde ahora estas cifras no se discuten de memoria. Las cifras oficiales serán las que dé el script versionado `tests/count_invariants.py`.

## Visión

Brumaltea no será un MMO masivo con mundo abierto total. Será **una academia compartida con una historia que sigue siendo tuya**, en tres capas:

1. **Mundo compartido.** Valdeniebla y los terrenos (`mundo`), la planta baja del castillo (`pb`: Patio del Reloj, Gran Comedor, Galería de las Casas, Biblioteca), `p1`, `p2`, las bandas del castillo, `bod`, `brezal` y las regiones RG. Aquí están la Copa de las Casas, el reloj del mundo, los eventos públicos (EV42), el chat, el ajedrez entre personas y, más adelante, el mercado.
2. **Instancias de grupo de 1 a 4 jugadores.** `cripta`, `cueva`, `catac`, `int_cripta6` y `cis`.
3. **Fase o instancia personal.** La historia de los 7 cursos y del espejo de plata:
   - la sala `PBR.DOR`, que se extrae como área nueva `ala` (el Ala Dormida);
   - `int_corazon`, los jefes de historia, las secciones de sigilo y los 3 finales de `ending41`;
   - los NPC de historia (Iria, Bastián, Valcárcel, Albarrán, Nora, Xana, Pimienta, Trastín), que cada cliente fasea según sus propios flags.

**Qué se conserva de la historia.** Cada jugador sigue siendo el protagonista: tiene sus amistades, su rival, sus decisiones de `DEC42` y su final. La contradicción de tener muchos elegidos se resuelve con la **Promoción de plata**: este año el espejo brilla en plata para todos los novatos, algo que no pasaba desde la niña desaparecida hace 80 años (`EXPECT.rueda`). Ese misterio pasa a ser el hilo común de la temporada. Hay que reescribir `WHISPERS` y `EXPECT` de m1 **antes** del lanzamiento, no después.

**Pilares**, en orden de prioridad:
1. Acogedor y narrativo.
2. Las casas como comunidad.
3. Poder horizontal con techo.
4. Nada competitivo se calcula en el cliente.
5. El modo un jugador sin conexión sigue existiendo y su suite de pruebas siempre en verde.

## Decisiones de la mesa

| # | Desacuerdo | Gana | Resolución y motivo |
|---|---|---|---|
| 1 | Alcance: MMO completo o híbrido | Game Designer (consenso) | Mundo compartido, historia en fase o instancia, cooperativo de 1 a 4. Es lo único viable para una persona. |
| 2 | Etapa cooperativa P2P/WebRTC | Backend y DevOps | **Descartada.** Necesita señalización y TURN de todas formas, y el anfitrión impondría su `S`. Una sala Colyseus en modo relé valida lo mismo y ese código no se tira. |
| 3 | ¿Los duelos son baratos de pasar a red? | Gameplay | No: `duelStart`/`duelPoint` son combate en tiempo real (mkFoe «duelista», 60 s). **El primer multijugador real es el ajedrez** (`chLegal`/`chMake`, 2-4 días). El duelo entre jugadores llega después del cooperativo contra criaturas. El duelo contra alumnos IA sigue en local. |
| 4 | ¿Presencia antes de extraer `sim/`? | Backend y DevOps, con la condición de QA | La presencia no espera a `sim/`, pero **sí a la línea base** (partidas doradas, conteos, hash de mapa). El protocolo lleva `seq` y tick del cliente desde el primer día (lo que pedía Gameplay). La carga útil es la posición y el servidor valida velocidad, área y colisión. |
| 5 | Validar colisión en la fase de presencia | Backend | Sí, porque `collision.bin` más un hash por área es un entregable de la fase 0 (World Builder). Si se retrasa, la fase 2 arranca validando solo velocidad y área (la objeción de DevOps), y la colisión se añade en cuanto exista el artefacto. |
| 6 | Reloj del mundo: ¿MVP o después? | NPC & AI | **Entra en la fase de presencia.** Con relojes distintos, dos jugadores ven comedores y noches diferentes. En modo en línea dormir deja de adelantar el reloj y pasa a dar una bonificación. El modo sin conexión conserva el reloj personal. |
| 7 | Criaturas con autoridad del servidor en el MVP | Backend, DevOps y NPC (revisado) | No en el MVP: las criaturas siguen siendo locales por jugador y sin botín comerciable. **El piloto es la gárgola de EV42**, que llega con la economía autoritativa porque reparte lunas y puntos de Copa. La ecología completa de `SPAWNS`, al final. |
| 8 | ¿Brezal es mazmorra? | World Builder y NPC | Es **mundo abierto compartido**: tiene 6 entradas de SPAWNS, ELITES y LOST. Solo se instancian las mazmorras, `ala` e `int_corazon`. Las misiones principales no se instancian enteras: casi todas sus etapas son conversaciones en el hub y `playScene` ya es una superposición local. |
| 9 | Capa de fase sobre los tiles | World Builder, Designer y Gameplay | **No hay fase de tiles.** Toda mutación de mapa condicionada por un flag de historia (`doorOpen` en sealedDoor2/_os18, `almacen` en la línea 3225 y las que encuentre el test de hash) se convierte en portal o en puerta-entidad por jugador. Las zonas compartidas tienen una sola rejilla de colisión. Lo que diga `tests/map_hash.py` con varios estados de flags zanja la discusión entre 135, 218 y 264. |
| 10 | Clave de sala | World Builder | El área de `AREAS`/`BAND`, **nunca `zoneAt`**, que es cosmética y cambia con los parches. |
| 11 | Un proceso por zona; mapa servido como `zones/*.json` | Backend y DevOps | Un solo proceso con salas Colyseus, y se reparte solo cuando lo pidan las métricas. El mapa lo sigue generando el cliente y el servidor carga `collision.bin` con hash. Si el hash no coincide, el servidor rechaza con «recarga». `zones/pois.json` sí se hace, para el mapa y el minimapa. |
| 12 | Interés de red (AOI) con rejilla de 32×32 | World Builder | El interés se calcula **primero por área** y, solo si una sala supera los 60 jugadores, se filtra a vista máxima + 4 tiles. |
| 13 | Tamaño de canal: 30, 40, 50 o 60 | Backend | Tope de **40 por canal**, con un canal nuevo a partir de 32. Las salas de banda del castillo, 30. |
| 14 | Orden de trabajo de Gameplay | Gameplay, para combate y economía | El orden es: inventario de parches, después módulos sin cambio de comportamiento, después `sim/` con tick fijo y RNG con semilla, y por último autoridad del servidor. Los datos puros (`ITEMS`, `QUESTS`, `HOUSES`) pueden extraerse antes. **No se extrae lógica a `shared/` antes de aplanar los parches**, porque el servidor validaría reglas que no son las que se ejecutan. Hay congelación de contenido nuevo solo durante las ~2 semanas de partición. |
| 15 | Criterio «byte a byte» | QA | Inalcanzable hoy. Nivel A: el test inyecta mulberry32 y un reloj falso, y compara **por campos** (lvl, xp, lunas, inv, Qs, flags). Byte a byte solo cuando exista `sim.step`. |
| 16 | Umbral de FPS en CI | QA | En CI la comparación es **relativa a main** (falla si la mediana de update o render empeora más de un 20 %). Los fps absolutos (60 en gráfica integrada a 1080p, 30 en Android de gama media) se miden a mano o por la noche en una máquina de referencia. |
| 17 | Carga a 1.000 conexiones | Backend y DevOps | Se prueba a **600 bots** de protocolo (el doble del objetivo de 300) más 50 clientes Playwright en una sala. |
| 18 | Zoom de cámara | UI/UX, con datos de DevOps y World Builder | No se fija un VW/VH. **Mínimo de 14 tiles en el lado corto**, `SCALE=1` permitido, y ajuste Cerca/Normal/Lejos (±1 de escala). Normal = lo que ya hay en la copia de trabajo (~40×22 en escritorio) si fps2 lo aguanta; si no, 28 de ancho. **La cámara se limita a `AREAS[área].b`** y no a toda la matriz. En interiores pequeños, zoom fijo y cámara centrada. `updateBossBar` pasa a depender de la vista y no de 360 px. La caché de tiles estáticos por chunks solo se hace si la medición lo exige. Los radios de IA (78/120 px) y de ráfaga (44 px) no cambian con el zoom. |
| 19 | `#cc-count` | Todos | Se borra el span y se añade un test que compruebe que no existe. Ningún test lo usa. |
| 20 | Invulnerabilidad durante el diálogo | UI/UX y Gameplay | No hay protección general. En SAFE, menú y diálogo a pantalla completa con estado «ocupado». Fuera de SAFE, paneles no modales y **no se puede iniciar un diálogo con aggro activo**. `frozen()`/`pauseFlag` pasan a ser estado del jugador. Las escenas solo congelan en fase personal. Los eventos sociales (coro, estrellas) son ambientales y no quitan el control. |
| 21 | Comercio en el MVP | Economy, Designer y Backend | **No hay trueque, ni Tablón, ni Copa real** hasta que el monedero, el inventario y `addPoints` sean autoritativos. Una sola moneda, las lunas, con libro mayor (ledger) de solo inserción y reclamaciones (claims) idempotentes. |
| 22 | Migración de partidas | Economy y QA, frente a Backend | Lo importado **nunca reabre una concesión**. Se importan los flags narrativos, los cosméticos y las UPGR ya hechas, que quedan ligadas al personaje. Todos los cofres y misiones se marcan como reclamados. El monedero empieza con ~50 lunas. El inventario libre no se migra. El importador usa una lista blanca validada con zod, nunca `Object.assign(S,d.S)`. Un test importa un guardado con todas las misiones completas y comprueba que el ledger no cambia. |
| 23 | ¿Los flags que habilitan pagos pueden vivir en el cliente? | Economy y QA, frente a DevOps | No. `trastoDay`, `pielesWk`, `encDay`, `sold.day` y los cofres viven en la tabla `claims` del servidor. Todo dato del cliente lleva `trust:'client'`, y un test prohíbe que el ranking, la Copa o el mercado lo lean. |
| 24 | Donar lunas a la Copa | Designer (Economy se retracta) | Rechazado: sería pagar para ganar entre casas. El bono por entrar en la casa pequeña es **cosmético ligado**, no en lunas. |
| 25 | Puntos de Copa por evento | Designer, con matiz de NPC | Puntos **fijos** por participante que supere el umbral de crédito (≥10 %), con tope diario por jugador. **La Copa semanal se mide como media por jugador activo de cada casa.** La beca semanal se queda en local mientras no haya servidor. |
| 26 | Ranuras de equipo con estadísticas e inventario con uid | Designer y Economy | Las ranuras son cosméticas o dan efectos laterales con techo (velocidad, radio de recogida, iframes), nunca daño ni vida. El inventario son **contadores** por `item_id` más un campo `bind:'cuenta'|'libre'` en ITEMS. |
| 27 | ¿Las ELITES pasan a jefes de mundo? | NPC & AI | Solo 2 o 3 pasan a jefe de mundo, con un patrón para grupo. Cada élite conserva su variante personal de encargo (`f.enc`) para el Gremio. |
| 28 | «Si nadie va a la gárgola, mañana hay dos» | Economy | Puede acumularse dificultad, pero la **recompensa por cuenta y evento es fija** y no escala con el número de participantes. La vida del jefe sí escala: `hp*(1+0,6*(n-1))`, con tope en n=10. |
| 29 | Secundarias repetibles | Economy | La primera vez es un claim único con la recompensa completa. Las repeticiones pasan a ser encargos del Gremio (`encReward`, tope `ENC_DAILY=4`). |
| 30 | Trueque dentro de `renderShop` | UI/UX | El trueque va en **ventana propia**: doble confirmación, cuenta atrás de 3 s y aviso cuando el otro cambia su oferta. El Tablón del Gremio sí es una pestaña del panel de tienda. |
| 31 | Drive como copia del personaje en línea | UI/UX | El personaje en línea solo se guarda en el servidor (más una descarga RGPD de solo lectura). Drive y `.json` quedan **solo para personajes de Historia sin conexión**. En la pantalla de título hay dos entradas separadas. |
| 32 | Invitados en instancias de historia | UI/UX | Solo elige el anfitrión. El invitado ve los diálogos en modo lectura («Historia de <nombre>») y `DEC42` nunca se aplica a su partida. |
| 33 | Postgres gestionado o local; `ws` plano o Colyseus | Backend | Postgres 16 local en el VPS y Colyseus desde el relé. DevOps endurece las copias: **WAL continuo a B2** en cuanto exista el ledger y restauración probada cada mes. |
| 34 | PvP | Designer | No hay PvP en mundo abierto, nunca. Solo duelo consentido o torneo instanciado, con marcador determinista (`duelPoint`) y sin críticos aleatorios. Los duelos y el ajedrez amistosos no dan puntos de Copa ni lunas. |
| 35 | Escalado de criaturas | Designer | En zona abierta, nivel fijo por zona y *level sync* a nivel de zona + 2. En instancia, nivel máximo de la mazmorra y vida ×0,8 por miembro. Nunca `lvlN()` del cliente. |
| 36 | Barra de acción | Designer y UI/UX | **6 ranuras: 4 hechizos y 2 consumibles**, todas con enfriamiento visible. |

## Arquitectura

**Cliente**
- Sigue siendo estático en GitHub Pages (o Cloudflare Pages) con el dominio del dueño. La URL `wss://` se inyecta por entorno, igual que hoy `GOOGLE_CLIENT_ID` en `pages.yml`.
- En la fase 1-2 la red entra como un módulo más con el patrón de parches existente (`net.js`: conexión, interpolación con búfer de 100 ms, reconexión de 20 s y `net.state` = offline/conectando/online/reconectando).
- Después, partición en módulos ES nativos sin bundler, en el mismo orden y con un registro `hook()` ordenado. esbuild solo cuando haga falta.
- `window.__test` (snapshot, teleport, setTime, drain, step, seed, input, events) se carga el último.

**Servidor**
- Node 22 + TypeScript + Colyseus (WebSocket) + Fastify (REST para auth, guardado y, más adelante, el Tablón).
- Salas:
  - `ZoneRoom`: compartida, por área y canal.
  - `StoryRoom`: personal, 1 jugador más invitados de solo lectura.
  - `DungeonRoom`: 1 a 4 jugadores.
  - `ChessRoom` y `DuelRoom`: 2 jugadores.
- `sim/` y `shared/rules` son JS plano con JSDoc, y el navegador y Node los importan tal cual.
- Sin `setTimeout` ni `Math.random` dentro de una sala.

**Protocolo** (`shared/protocol`)
- Versionado: el cliente envía `v` y el servidor rechaza con «recarga».
- Esquemas zod compartidos.
- Todo mensaje económico lleva un `event_id` de idempotencia.
- Tasas:

| Contexto | Tasa |
|---|---|
| Entrada en hubs | Posición + `seq` a 10 Hz |
| Snapshots en hubs | 10 Hz |
| Duelo y mazmorra | Simulación 20 Hz, snapshots 20 Hz, entrada 15 Hz en lotes |
| Ajedrez | Por evento |
| Reloj del mundo | Se emite cada minuto de juego |

- Chat: canales Zona, Casa, Grupo, Susurro y Sistema, sin chat global. Límite de 1 mensaje/s con ráfaga de 3 y 200 caracteres. Filtro en el servidor. En el cliente, siempre `textContent`/`esc()`.

**Base de datos** (PostgreSQL 16)
- `accounts(google_sub, email, baneado)`
- `characters(id, account_id, nombre, casa, look jsonb, nivel, xp, story jsonb, trust, schema_version)`
- `claims(character_id, kind, ref)` con clave única
- `wallet_ledger(id, character_id, delta, motivo, ref, event_id único, ts)`
- `inventory_items(character_id, item_id, qty)`
- `house_points(temporada, casa, character_id, puntos, motivo)`
- `chess_games`, `friendships` y, más adelante, `market_orders`
- El trueque es una transacción SERIALIZABLE con `SELECT … FOR UPDATE`.

**Identidad**: ID token de Google (GSI) verificado con `google-auth-library`, más sesión propia (JWT de 15 min + refresh en cookie httpOnly). El servidor nunca guarda tokens de Drive.

**Hosting**: un VPS Hetzner CPX21/CX32 con Caddy (TLS), Cloudflare delante (proxy WS y protección DDoS), Docker Compose, imagen en GHCR, `server.yml` con staging automático y producción por tag con aprobación. Monitorización: pino, Sentry (plan gratuito), Uptime Kuma, `/health`, `window.onerror` enviado en lotes y CSP en `index.html`.

**Coste mensual estimado**, siempre ligado a su fase:

| Fase | Coste | Capacidad |
|---|---|---|
| 0 (actual) | 0 € | — |
| 1-2: auth, guardado, presencia, ajedrez | 10-15 € (VPS ~8-10 €, B2 ~1-2 €, dominio ~1 €) | ~300-500 conectados |
| 3: economía y ledger con WAL | 15-25 € | Hasta ~300 conectados |
| 4-5: criaturas y mazmorras simuladas | 30-60 € | ~150-250 conectados por proceso, Redis al pasar a varios procesos |

Umbrales para escalar: lag del event loop p99 > 20 ms o CPU > 60 % sostenida, se pasa a un segundo proceso. CPU de la base > 50 % o > 20 GB, se pasa a Postgres gestionado o réplica.

## Sistemas del juego

- **Cámara y creador.** Lo que pidió el dueño, sin depender de la red:
  - mínimo de 14 tiles en el lado corto y `SCALE=1` en móvil vertical;
  - Cerca/Normal/Lejos con +/- y pellizco;
  - límite de cámara por área y zoom fijo en interiores;
  - barra de jefe según la vista;
  - se borra `#cc-count`.
- **Casas y Copa.** Se conservan `HOUSES` y `repaintHouseCarpet`. El espejo reparte de forma equilibrada: «elegir tú» solo en casas con menos población. En línea, la Copa se mide como media por jugador activo, con temporada semanal y Banquete en el Gran Comedor. Cuando la Copa la calcule el servidor desaparecen los `8+random*18` de `onNewDay`. Hasta entonces la Copa en línea solo se muestra y no reparte recompensas.
- **Historia y misiones.** Las QUESTS principales y m1 corren en el cliente en fase personal. Las recompensas en lunas o XP se reclaman al servidor una vez (fase 3). Las secundarias repetibles pasan a ser encargos del Gremio. Habrá eventos públicos nuevos (gárgola, Faro, invasión del Hondo). Las misiones que dependen de «dormir hasta la noche» se revisan para el reloj común.
- **Reloj y calendario.** En línea, un reloj del servidor (1 día de juego ≈ 2 h reales, a confirmar). Clases, exámenes, `nightNow` y `SPAWNS` nocturnos lo leen. Dormir da una bonificación.
- **NPC.** Los de mundo (Teodora, profesores, alumnos) se simulan de forma determinista en cada cliente a partir del reloj y una semilla diaria, sin CPU en el servidor: el `Math.random` de rutina pasa a ser `rng(seed)`. Los NPC de historia se fasean con `npcVisible` ampliado, **no son sólidos** en zonas compartidas (`npcBlock` los ignora) y sus escenas largas van en burbuja o sala lateral.
- **Combate.**
  - MVP: criaturas locales.
  - Fase 3b: gárgola piloto en el servidor.
  - Fase 5: `updateFoes`/`bossAI` en el servidor con tabla de amenaza, cambio de objetivo al 130 %, tope de 3 perseguidores por jugador, leash al rectángulo de SPAWNS + 6 tiles con recuperación de vida, borrado de amenaza a los 3 s en SAFE, y población `max_base + 0,5 por jugador` con tope.
  - Las hitboxes se centralizan en la tabla `HITBOX`.
- **Progresión.** Se mantienen `xpFor` y `gainXP`. El techo por curso lo marca `CURSO_REQ.lvl`, con *level sync*. Pasado el curso 7, progresión horizontal (estampas, bestiario, Gremio, cosméticos). Especializaciones por asignatura en curso 2-3: después del relé. Pasivo de casa ≤5 %.
- **Economía.**
  - Fuentes oficiales: pickups de criatura, `encReward`, trastos, pieles, beca, cofres y misiones únicas, venta a NPC y eventos y élites.
  - Sumideros: tiendas, Lucio (UPGR, wandUp, recetas repetibles con materiales de dos regiones), desmayo, barca, sopa, comisión del Tablón (6 % + 1 luna), sastrería, comidas con bonificación, renovar encargos (3 lunas) y decoración del cuarto.
  - Objetivo de 100-140 lunas al día. Tope blando de 30 lunas por hora de botín por región.
  - Jefes de historia con `luna:0`. Materiales repartidos por región.
- **Social.** Orden de llegada: ajedrez entre jugadores (MVP), luego pesca y presencia compartidas, después cooperativo en mazmorras, y el duelo entre jugadores y el torneo al final.
- **UI.** Tres capas:
  - Historia: Libreta, Vínculos (la actual pestaña Amigos), escenas.
  - Mundo: minimapa, tarjeta de evento, barra de jefe, hasta 12 placas de nombre dibujadas en el canvas.
  - Comunidad: chat, grupo, trueque.
  
  A esto se suman un `KEYMAP` con contextos (requisito para el chat), la barra de 6 ranuras y un chip de estado de red. Las acciones que dependen del servidor aparecen desactivadas con un tooltip cuando no hay conexión.
- **Guardado.** Sin conexión: igual que hoy. En línea: solo en el servidor, con `trust` por columna.

## Propiedad por rol

Regla general: **mientras `index.html` siga siendo un monolito, solo hay un PR abierto que toque `index.html` a la vez**, y el Director decide el orden. Cada rol edita solo los bloques de su sistema.

| Agente (`.claude/agents/`) | Propiedad exclusiva |
|---|---|
| `game-director.md` | `CLAUDE.md`, `.claude/rules/*` (architecture, coding-standards, multiplayer-rules), `docs/ROADMAP.md`, `docs/DECISIONS.md` (esta tabla), orden de merges en `index.html`. Hace de code-reviewer para la coherencia con el GDD. |
| `game-designer.md` | `docs/GDD.md`, `docs/GAME_SYSTEMS.md` (reglas), `shared/data/{quests,dailies,spells,houses,progression,cup}.json`, `tests/fixtures/state_taxonomy.json` (clasificación, que firma con el Director), textos de `WHISPERS`/`EXPECT`. |
| `backend-engineer.md` (incluye database-architect y la parte de servidor de security) | `server/` (salvo `server/src/economy/rules`), `shared/protocol/`, `migrations/`, `docs/DATABASE_SCHEMA.md`, `docs/GAME_ARCHITECTURE.md`, `src/net/net.js`, el flujo de auth (bloque OAuth ~8890-9010) y `serialize`/`saveGame`/`loadGame` en lo que toca a la red. |
| `gameplay-programmer.md` | `src/core/hooks.js`, `src/sim/{movement,combat,progression,inventory,interact,step}.js`, `src/client/{input,prediction}.js`, `tools/extract-modules`, `window.__test`, conversión de puertas de historia en portales o entidades. |
| `world-designer.md` | `buildWorld*`, `ZONES`/`AREAS`/`BAND`/`RG`/`AREA_EXITS`/`SAFE`, `shared/data/world/zone_kind.json`, `zones/pois.json`, `tools/export-map` (`collision.bin` + hash), ubicación y densidad en `SPAWNS`/`ENC_ZONES`/`ELITES`/`GATHER`. |
| `npc-ai-designer.md` | `src/ai/` (FOE, `bossAI`, `updateFoes`, `fshots`, `spawnTick`), rutinas NPC (`students`, `profTick`, `updateVendor`, `walkNPC`), `npcVisible`/`npcBlock` y la capa de fase, EV42/`startEvent`, el futuro director de mundo. |
| `ui-ux-designer.md` | `src/ui/`, CSS del HUD y los menús, `#hud-*`/`#tracker`/`#dialog`/`#menu` (incluido el registro de pestañas de la Libreta), `#touch`, creador `cc-*`, `resize()`/SCALE/VW/VH, `drawMap` y minimapa, `KEYMAP`, opciones, paneles de chat, grupo, trueque y barra de acción. |
| `economy-designer.md` | `shared/data/economy/*.json` (ITEMS con precio y bind, SHOP_ITEMS, SHOP_SELL, FISH_SELL, FOE.drop/luna, UPGR, wandUp, recompensas), `server/src/economy/rules` y `config/economy.json` (topes y tasas). Backend se encarga de las transacciones. |
| `qa-engineer.md` | `tests/` (run_all, fuzz, monkey, `unit/`, `multiclient/`, `protocol/`, `load/`, `fixtures/`, `count_invariants.py`, `map_hash.py`), `docs/TEST_PLAN.md`. Lee el resto en modo solo lectura y reporta los fallos al dueño de cada sistema. |
| `devops-engineer.md` | `.github/workflows/*` (QA pide cambios en los jobs de test mediante PR), `infra/` (Dockerfile, compose, Caddy, Cloudflare), secrets y environments, observabilidad, copias y WAL, `tests/fps2.py` y benchmarks, CSP y build. |
| `security-engineer.md` / `code-reviewer.md` | Por ahora no son agentes propios: la seguridad se reparte entre Backend (validación y sesión) y DevOps (infraestructura), y la revisión entre el Director y QA. |

## Hoja de ruta

Las estimaciones son para una persona con ayuda de IA y a tiempo parcial-alto. Cada fase se cierra con criterios que se pueden comprobar.

**Fase 0 — Lo que pidió el dueño y la línea base (2-3 semanas, sin red)**
- Zoom: mínimo de 14 tiles en el lado corto, Cerca/Normal/Lejos, límite de cámara por área, interiores fijos, barra de jefe según la vista; se borra `#cc-count`. Las capturas de `tests/out` se regeneran en el mismo PR.
- `fps2.py` mide update y render por separado.
- `count_invariants.py`, `state_taxonomy` (47 claves de `S.flags` y ~90 de `X.f`) y el test de claves sin clasificar.
- Partidas doradas de nivel A y test de ida y vuelta `serialize`/`loadGame`.
- `map_hash.py` con varios estados de flags, `collision.bin` y `pois.json`.
- Inventario de la cadena de parches.
- GDD v1: pilares, taxonomía, lista de mutaciones de historia, tabla de Copa, Promoción de plata.
- ✔ Criterio: `run_all.py` en verde; zoom sin bordes negros a 375×812 y a 1920×1080; mediana de render ≤ +20 % frente a main; ninguna clave sin clasificar.

**Fase 1 — Cuenta y guardado en la nube (2-3 semanas)**
- VPS, Caddy, Cloudflare, `server.yml` y staging.
- Auth con ID token y sesión propia.
- `PUT /characters/:id/save` con zod y `trust:'client'`.
- Pantalla de título Historia / Mundo.
- Importador con lista blanca (aspecto, nombre, narrativa; estipendio fijo).
- ✔ Criterio: login en staging; un guardado manipulado se rechaza o se recorta; importar un guardado con todo completado no toca el ledger; la restauración de copia funciona.

**Fase 2 — MVP en línea: presencia, chat, reloj y ajedrez (4-6 semanas)**
- `ZoneRoom` por área, 40 por canal, a 10 Hz; validación de velocidad, área y colisión; interpolación.
- Reloj del mundo y rutinas NPC deterministas con semilla diaria.
- NPC de historia fase y no sólidos.
- Chat por canales con filtro y reporte.
- `KEYMAP`, placas de nombre, minimapa.
- `ChessRoom` entre jugadores (amistoso, sin recompensas).
- RGPD: política de privacidad, borrado de cuenta.
- ✔ Criterio: `run_mc.py` con 8 clientes; el servidor rechaza teletransportes y mensajes con `seq` viejo; dos clientes ven la misma hora y a los mismos alumnos; 600 bots con tick p95 < 10 ms y < 8 KB/s por jugador; alfa cerrada con amigos.

**Fase 3 — Modularización y simulación (6-8 semanas, con congelación de contenido durante ~2 semanas)**
- Módulos ES con `hook()` ordenado.
- `sim/` separada de la presentación, tick fijo, `rng(state)`.
- `window.__test` sobre `sim.step`; partidas doradas de nivel B.
- ✔ Criterio: partida dorada idéntica campo a campo; `count_invariants` = 0 `Math.random` en `sim/`.

**Fase 4 — Economía autoritativa y Copa real (6-8 semanas)**
- Monedero, ledger, inventario por contadores, `claims`.
- Tiendas y Lucio en el servidor; reclamaciones de recompensas de historia; topes diarios con el reloj del servidor.
- `house_points` con media por jugador activo.
- Gárgola piloto (EV42) en el servidor.
- WAL a B2 y métricas del ledger.
- Después, unas semanas más tarde: trueque en ventana propia y Tablón del Gremio.
- ✔ Criterio: pruebas de doble gasto, doble reclamación y desconexión en mitad de un intercambio, en verde; saldo = suma del ledger; 0 `S.lunas+=` que el servidor acepte; la simulación económica de 30 días del perfil farmer queda por debajo del umbral.

**Fase 5 — Cooperativo y JcJ (8-10 semanas)**: `DungeonRoom` de 1 a 4 (cueva, catac, cripta) con *level sync*; luego `DuelRoom` y torneo por casas con rewind de la chispa.

**Fase 6 — Mundo vivo (largo plazo)**: criaturas compartidas en zonas abiertas, élites como jefes de mundo, regiones RG con ecología, rumores de servidor, varios procesos con Redis.

Calendario realista: **MVP en línea (fases 0-2) en ~3-4 meses. Economía y Copa reales, ~7-9 meses. Cooperativo y JcJ, ~1 año.**

## Riesgos principales

1. **La cadena de parches** (51 `gameUpdate`, más de 11 `cast`, 3 `serialize`, 5 `loadGame`): reordenarla rompe comportamientos sin avisar. Mitigación: línea base y partidas doradas antes de mover nada, y un solo PR a la vez sobre `index.html`.
2. **Autoridad del cliente**: 46 mutaciones de lunas y `Object.assign(S,d.S)`. Abrir cualquier intercambio antes de la fase 4 hunde la economía. Es una regla dura del GDD.
3. **Historia y mundo compartido**: puertas de historia que cambian tiles, escenas que congelan, NPC sólidos. Mitigación: portales, burbuja y `npcBlock` en fase.
4. **El reloj común cambia el diseño**: las misiones de «dormir hasta la noche» y los exámenes con hora se rompen. Hay que revisarlas en la fase 2.
5. **Rendimiento con la cámara alejada y 30 avatares**: render sin caché de tiles. Mitigación: medir siempre y usar la caché por chunks si hace falta.
6. **Alcance y desgaste de una sola persona**: guardias, moderación, trampas. Mitigación: Colyseus, un VPS y fases que se pueden publicar por separado.
7. **Legal**: RGPD y un público posiblemente menor de edad con chat. Política de privacidad, filtro, reporte y bloqueo antes de abrir al público.
8. **Contenido de un solo uso**: unas 30 misiones y 3 finales. Sin diarias, eventos y mazmorras repetibles, los jugadores se van en semanas.

## Preguntas abiertas para el dueño

1. ¿Cuántos jugadores simultáneos esperas en los primeros 6 meses y cuál es el presupuesto mensual máximo? ¿Basta con los ~10-25 € de las fases 1-4?
2. ¿El público incluirá menores de edad? De eso depende si el chat libre entra en el MVP o se empieza con emotes y frases predefinidas.
3. ¿El modo Historia sin conexión se mantiene para siempre como producto propio? Mi recomendación es que sí.
4. ¿Aceptas que las partidas actuales migren solo la narrativa, el aspecto y las mejoras, con un estipendio fijo de lunas y sin inventario comerciable?
5. ¿Apruebas la «Promoción de plata» y la reescritura de `WHISPERS`/`EXPECT` de m1?
6. ¿Habrá monetización? Si la hay, propongo que sea solo cosmética y ligada a la cuenta, decidida antes de la fase 4.