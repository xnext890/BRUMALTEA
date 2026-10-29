# Brumaltea

RPG de mundo abierto en píxel-art, en español, ambientado en una academia de magia. Un solo archivo HTML, sin dependencias ni servidor: `index.html`.

- 7 cursos de historia principal, 3 finales, ~30 misiones, duelos, ajedrez, amistades, exámenes y un castillo con vida propia.
- Se juega en el navegador (teclado o táctil).

## Jugar en local

Abre `index.html` en el navegador. O sirve la carpeta: `python3 -m http.server` y visita `http://localhost:8000`.

## Publicar con GitHub Pages

1. Sube el repo a GitHub.
2. *Settings → Pages → Source: GitHub Actions*.
3. Cada `push` a `main` publica el juego (`.github/workflows/pages.yml`).

## Guardado de la partida

| Método | Cómo funciona |
|---|---|
| Automático | Se guarda en el navegador (`localStorage`) mientras juegas. |
| Archivo | En el título: **Exportar partida** / **Importar partida** (`.json`). Funciona siempre. |
| Cuenta de Google | **Iniciar sesión con Google** guarda la partida en tu Google Drive, en una carpeta oculta de la app (`drive.appdata`). Nadie más la ve, ni tú en tu Drive. |

Si una partida no se puede cargar, se conserva una copia en `brumaltea-partida-v1-copia` antes de empezar otra.

### Activar el inicio de sesión de Google

Hace falta un ID de cliente OAuth propio (gratuito). Una sola vez:

1. [Google Cloud Console](https://console.cloud.google.com/) → crea un proyecto.
2. *APIs y servicios → Biblioteca* → activa **Google Drive API**.
3. *Pantalla de consentimiento de OAuth* → tipo Externo; añade el ámbito `.../auth/drive.appdata` y tu correo como usuario de prueba.
4. *Credenciales → Crear credenciales → ID de cliente de OAuth → Aplicación web*. En **Orígenes autorizados de JavaScript** pon la URL donde alojas el juego (por ejemplo `https://TU_USUARIO.github.io`) y `http://localhost:8000` para pruebas.
5. Dale el ID al juego de **una** de estas formas:
   - En GitHub: *Settings → Secrets and variables → Actions → Variables → New* → `GOOGLE_CLIENT_ID`. El workflow lo inyecta al publicar.
   - Editando `index.html`: `<meta name="brumaltea-google-client-id" content="TU_ID.apps.googleusercontent.com">`.
   - Sin tocar nada: al pulsar el botón por primera vez el juego te pide pegarlo (se guarda solo en tu navegador).

El ID de cliente es público por diseño; no es un secreto. No hay servidor propio: el navegador habla directamente con Google.

Limitación: el permiso de Google dura una hora. Si caduca, el juego lo renueva con tu siguiente pulsación o con **Sincronizar ahora**. Al salir se intenta guardar una última vez.

## Pruebas

```bash
pip install playwright && playwright install chromium
python3 tests/run_all.py            # todas
python3 tests/run_all.py t43 txt    # solo algunas
```

Incluye partidas simuladas de principio a fin (los tres finales), un test de «mono» con acciones aleatorias (`monkey.py <semilla>`), barridos de todas las misiones y zonas, y medición de fps.

## Estructura

```
index.html          el juego completo
tests/              pruebas con Playwright
.github/workflows/  publicación en Pages y CI
```

## Licencia

Aún sin elegir. Añade un archivo `LICENSE` antes de abrir el repositorio al público. Todos los nombres y textos son originales.
