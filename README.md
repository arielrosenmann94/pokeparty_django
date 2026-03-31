# ⚔️ PokéParty Optimizer

Una aplicación web Django que permite armar y optimizar una party Pokémon con stats reales obtenidos desde la [PokéAPI](https://pokeapi.co/).

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.x-green?logo=django&logoColor=white)
![PokéAPI](https://img.shields.io/badge/PokéAPI-v2-red)

---

## 🧩 Funcionalidades

- 🎯 **Selección de tipo**: elegí entre los 18 tipos de Pokémon
- 🎲 **Captura aleatoria**: obtiene un Pokémon random del tipo elegido desde la PokeAPI
- 🎮 **Party (máx. 6)**: los primeros 6 van a la party, el resto al PC Box
- 📦 **PC Box**: reserva para Pokémon excedentes
- 📊 **Ordenación**: ordenar la party por HP, Ataque, Defensa, Atq. Esp. o Velocidad
- ✨ **Mejor equipo posible**: selecciona los 6 con mayor `totalPower` de toda la colección
- 💾 **Persistencia**: todos los datos se guardan en base de datos (SQLite por defecto)

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd pokeparty_django
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configurar base de datos

**SQLite** (por defecto, sin configuración extra):

```bash
python manage.py migrate
```

**PostgreSQL** (opcional): creá un archivo `.env` basado en `.env.example` y ajustá `DATABASES` en `settings.py`.

### 4. Ejecutar el servidor

```bash
python manage.py runserver
```

Abrí el navegador en: **http://127.0.0.1:8000/**

---

## 🗂️ Estructura del proyecto

```
pokeparty_django/
├── party/                    # App principal
│   ├── migrations/
│   ├── templatetags/         # Filtros custom (type_color)
│   ├── admin.py
│   ├── models.py             # Modelo Pokemon
│   ├── services.py           # Integración con PokéAPI + caché
│   ├── urls.py
│   └── views.py
├── pokeparty/                # Config del proyecto
│   ├── settings.py
│   └── urls.py
├── static/
│   ├── css/main.css          # Diseño dark glassmorphism, 100% responsive
│   └── js/
│       ├── main.js
│       └── party.js
├── templates/
│   ├── base.html
│   └── party/
│       ├── index.html
│       └── _pokemon_card.html
├── requirements.txt
└── manage.py
```

---

## 🧮 Lógica de optimización

```
totalPower = hp + attack + defense + special_attack + special_defense + speed
```

El botón **"Mejor equipo posible"** combina party + PC Box y coloca los 6 Pokémon con mayor `totalPower` en la party.

---

## 🔌 Variables de entorno (opcional para PostgreSQL)

Crear un archivo `.env` en la raíz:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta
DATABASE_URL=postgres://usuario:password@localhost:5432/pokeparty
```

Ver `.env.example` para referencia.

---

## 📄 Licencia

MIT — datos de Pokémon provistos por [PokéAPI](https://pokeapi.co/).
Pokémon y nombres de personajes son marcas registradas de Nintendo / Game Freak.
