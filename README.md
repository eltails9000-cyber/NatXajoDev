# GloryBot

Bot avanzado de Discord construido con **discord.py 2.x** y arquitectura modular por cogs.

---

## Requisitos

- Python 3.10 o superior
- pip

---

## Instalación

```bash
cd bot
pip install -r requirements.txt
```

---

## Configuración

Crea un archivo `.env` en el directorio `bot/` con las siguientes variables:

```env
# Token de tu bot de Discord (obligatorio)
DISCORD_TOKEN=tu_token_aqui

# ID del propietario del bot (obligatorio para comandos /shutdown, /restart, /maintenance)
OWNER_ID=1042929958286266540

# URL base de tu API de Roblox (obligatorio para comandos /roblox*)
ROBLOX_API_URL=https://tu-api.ejemplo.com

# Clave de autenticación de la API de Roblox (obligatorio para comandos /roblox*)
ROBLOX_API_KEY=tu_clave_aqui

# Nombre del archivo SQLite (opcional, por defecto: database.db)
DATABASE_NAME=database.db
```

> ⚠️ **Nunca compartas ni subas el archivo `.env` a un repositorio público.**

---

## Ejecutar el bot

```bash
cd bot
python main.py
```

---

## Estructura del proyecto

```
bot/
├── main.py               # Punto de entrada y definición de GloryBot
├── config.py             # Variables de configuración (lee desde .env)
├── api.py                # Cliente async para la API de Roblox
├── database.py           # Acceso a la base de datos SQLite (tabla bans)
├── requirements.txt      # Dependencias Python
├── Procfile              # Definición de proceso para plataformas como Railway/Heroku
├── README.md             # Esta documentación
│
├── cogs/
│   ├── maintenance.py    # /maintenance on|off, /botstatus
│   ├── moderation.py     # /kick, /ban, /unban, /warn
│   ├── owner.py          # /shutdown, /restart
│   └── roblox.py         # /robloxban, /robloxcheck, /robloxunban
│
└── utils/
    ├── maintenance_state.py  # Estado global de mantenimiento
    ├── messages.py           # Embeds reutilizables (success, error, info)
    └── permissions.py        # Check owner_check() para slash commands
```

---

## Comandos disponibles

### Generales
| Comando | Descripción | Permiso |
|---|---|---|
| `/botstatus` | Muestra el estado actual del bot | Solo owner |

### Mantenimiento
| Comando | Descripción | Permiso |
|---|---|---|
| `/maintenance on` | Activa el modo de mantenimiento | Solo owner |
| `/maintenance off` | Desactiva el modo de mantenimiento | Solo owner |

### Owner
| Comando | Descripción | Permiso |
|---|---|---|
| `/shutdown` | Apaga el bot de forma segura | Solo owner |
| `/restart` | Reinicia el proceso del bot | Solo owner |

### Moderación Discord
| Comando | Descripción | Permiso Discord |
|---|---|---|
| `/kick @miembro razón` | Expulsa a un miembro del servidor | Kick Members |
| `/ban @miembro razón` | Banea a un miembro del servidor | Ban Members |
| `/unban id razón` | Desbanea a un usuario por su ID | Ban Members |
| `/warn @miembro razón` | Emite una advertencia a un miembro | Moderate Members |

### Roblox
| Comando | Descripción | Permiso Discord |
|---|---|---|
| `/robloxban userid reason` | Banea un usuario de Roblox (local + API) | Ban Members |
| `/robloxcheck userid` | Consulta si un usuario tiene ban registrado | Cualquiera |
| `/robloxunban userid` | Elimina el ban local y notifica a la API | Ban Members |

---

## Variables de entorno requeridas

| Variable | Obligatoria | Descripción |
|---|---|---|
| `DISCORD_TOKEN` | ✅ | Token del bot de Discord |
| `OWNER_ID` | ✅ | ID numérico del propietario |
| `ROBLOX_API_URL` | ⚠️ Necesaria para Roblox | URL base de la API de Roblox |
| `ROBLOX_API_KEY` | ⚠️ Necesaria para Roblox | Clave de la API de Roblox |
| `DATABASE_NAME` | ❌ Opcional | Nombre del archivo SQLite (default: `database.db`) |

---

## Notas

- Los comandos slash se sincronizan globalmente al iniciar el bot. Puede tardar hasta **1 hora** en aparecer en todos los servidores.
- La base de datos SQLite se crea automáticamente en el primer arranque.
- Si la API de Roblox no está configurada, los comandos `/roblox*` guardarán el ban localmente pero avisarán que la petición a la API falló.
