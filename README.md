# ⚔️ PokéParty Optimizer

---

## 📚 Sobre este proyecto

> **Este repositorio es la solución del trabajo práctico _PokéParty Optimizer_, desarrollado como ejercicio integrador para los estudiantes del curso de Python con Django en la capacitación SENCE.**
>
> El trabajo fue diseñado para la clase de **API REST Framework** del módulo de Django, con el objetivo de practicar la integración con APIs públicas externas, el uso del ORM de Django para persistencia de datos y la construcción de interfaces dinámicas con Django Templates.
>
> El proyecto sirve como referencia de implementación completa: desde la configuración del entorno, el consumo de la PokeAPI, la lógica de negocio en vistas basadas en funciones (FBV), hasta el diseño responsive y accesible del frontend con CSS puro.

---

## 🎯 ¿Qué es PokéParty Optimizer?

**PokéParty Optimizer** es una aplicación web construida con Django que te permite armar, gestionar y optimizar un equipo de hasta 6 Pokémon utilizando datos reales de stats obtenidos en tiempo real desde la [PokéAPI](https://pokeapi.co/).

La app funciona como un sistema de selección y comparación: podés capturar Pokémon de distintos tipos, ver sus stats completos, reordenar tu equipo por cualquier stat individual y, con un solo clic, el sistema elige automáticamente el equipo de 6 más poderosos de toda tu colección.

### ¿Por qué es interesante para developers?

- Demuestra integración real con una **API REST pública** usando `requests` + caché en memoria
- Implementa **persistencia completa** con el ORM de Django y SQLite/PostgreSQL
- Usa **Django Templates** con herencia, partials y custom template tags
- Frontend 100% **responsive** (mobile → tablet → desktop → TV) con CSS puro (sin frameworks)
- Arquitectura limpia: separación entre **servicio de API, modelos, vistas y templates**
- Flujo POST → redirect → GET correcto con mensajes flash (patrón PRG)

---

## ✨ Funcionalidades

| Feature | Descripción |
|---|---|
| 🎯 Selector de tipo | 18 tipos de Pokémon con emojis y colores oficiales |
| 🎲 Captura aleatoria | Obtiene un Pokémon random del tipo elegido vía PokeAPI |
| 🎮 Party (máx. 6) | Primeros 6 capturados van a la party activa |
| 📦 PC Box | Los Pokémon excedentes se guardan automáticamente en reserva |
| 📊 Ordenar por stat | Ordenar la party por HP, Ataque, Defensa, Atq. Esp. o Velocidad |
| ✨ Mejor equipo posible | Selecciona los 6 Pokémon con mayor `totalPower` de toda la colección |
| 🔁 Mover entre secciones | Mover Pokémon entre Party y PC Box manualmente |
| 🌿 Liberar Pokémon | Eliminar un Pokémon de la colección |
| 💾 Persistencia | Todos los datos se guardan en base de datos (SQLite por defecto) |

---

## 🧮 Lógica de optimización

```
totalPower = hp + attack + defense + special_attack + special_defense + speed
```

El botón **"Mejor Equipo Posible"** evalúa toda la colección (Party + PC Box) y asigna los 6 con mayor `totalPower` a la Party, enviando al resto al PC Box.

---

## 🧱 Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Django 6.x (FBV, ORM, Templates) |
| Base de datos | SQLite (default) / PostgreSQL (opcional) |
| API externa | [PokéAPI v2](https://pokeapi.co/) via `requests` |
| Caché | Django `LocMemCache` (anti-rate-limit) |
| Frontend | CSS puro custom + Google Fonts (Inter) |
| JavaScript | Vanilla JS (animaciones, loading states) |

---

## 🗂️ Estructura del proyecto

```
pokeparty_django/
├── party/                        # App principal
│   ├── migrations/               # Migraciones ORM
│   ├── templatetags/
│   │   └── pokemon_tags.py       # Filtro custom: |type_color
│   ├── admin.py                  # Admin Django registrado
│   ├── models.py                 # Modelo Pokemon (stats + location)
│   ├── services.py               # Integración PokeAPI + caché
│   ├── urls.py                   # Rutas de la app
│   └── views.py                  # Capture, sort, optimize, move, release
├── pokeparty/                    # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
├── static/
│   ├── css/main.css              # CSS responsive: mobile → TV
│   ├── js/main.js                # Auto-dismiss messages
│   ├── js/party.js               # Animaciones + loading states
│   └── img/pokeball.svg          # Fallback imagen
├── templates/
│   ├── base.html                 # Layout con header + mensajes flash
│   └── party/
│       ├── index.html            # Vista principal
│       └── _pokemon_card.html    # Card partial con stat bars
├── .env.example
├── requirements.txt
└── manage.py
```

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/pokeparty_django.git
cd pokeparty_django
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configurar base de datos

**SQLite (por defecto — sin configuración extra):**

```bash
python manage.py migrate
```

**PostgreSQL (opcional):** copiar `.env.example` a `.env` y completar las variables:

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

Luego ajustar `DATABASES` en `pokeparty/settings.py` para leer del `.env`.

### 4. Ejecutar la aplicación

```bash
python manage.py runserver
```

Abrí el navegador en: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### (Opcional) Panel de administración Django

```bash
python manage.py createsuperuser
# → http://127.0.0.1:8000/admin/
```

---

## 📸 Flujo de uso

```
1. Seleccionás "Fuego" → capturás Charizard 🔥 → entra a la Party
2. Seleccionás "Agua"  → capturás Vaporeon 💧 → entra a la Party
3. Repetís hasta tener 6 → el 7mo Pokémon va al PC Box
4. Hacés clic en "Mejor Equipo Posible" →
   el sistema evalúa toda la colección y 
   pone los 6 con mayor totalPower en la Party
```

---

## 🧩 Conceptos de Django aplicados

- **Models:** `Pokemon` con `JSONField` para tipos, `IntegerField` para stats, `CharField` con choices para `location`
- **ORM queries:** `filter()`, `order_by()`, `values_list()`, `update_fields`, `count()`
- **Views (FBV):** `@require_POST`, `get_object_or_404`, `messages`, redirect PRG pattern
- **Templates:** herencia (`extends`/`block`), `include`, `{% for %}`, `{% if %}`, `{% url %}`
- **Template tags:** custom filter `|type_color` registrado con `@register.filter`
- **Static files:** `{% static %}`, `STATICFILES_DIRS`
- **Cache:** `cache.get/set` con `LocMemCache` para no repetir llamadas a la API
- **CSRF:** protección en todos los formularios POST

---

## 🌐 Variables de entorno (`.env.example`)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

# Opcional - si usás PostgreSQL en lugar de SQLite:
# DATABASE_URL=postgres://user:password@localhost:5432/pokeparty
```

---

## 📄 Licencia

MIT — datos de Pokémon provistos por [PokéAPI](https://pokeapi.co/).  
Pokémon y todos los nombres de personajes son marcas registradas de **Nintendo / Game Freak / The Pokémon Company**.  
Este proyecto es de carácter educativo y no tiene fines comerciales.
