# **Bienvenido a tu gestor de resultados de LaLiga de futbol profesional**

## INTRODUCCIÓN

Como amante del fútbol, siempre me ha fascinado cómo funcionan las aplicaciones de gestión de resultados. Por eso he decidido crear mi propia versión, aunque sea en una fase inicial y con fines educativos.

Con esta aplicación podrás:
- Crear competiciones, temporadas y partidos de forma manual.
- Crear jugadores y asignarlos a cada equipo y temporada.
- Registrar resultados para que la clasificación se actualice automáticamente.

Los criterios de desempate en la clasificación siguen el sistema de LaLiga española. Aunque es posible crear competiciones de otros países, la clasificación siempre usará estos criterios.

## INSTALACIÓN

Para empezar a usar esta aplicación, necesitarás:

- MySQL como gestor de datos
- Python 3.10+ y pip
- Node.js y npm (para el frontend con Vue.js)

---

### 1. Clonar el repositorio

Clonar el repositorio via IDE, o via terminal:
```
git clone https://github.com/.../...(url del repositorio)
cd repo
```

### 2. Instalación de dependencias del Backend

```
cd backend
python -m venv venv
# Activar entorno
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```
**Instalar las dependencias**

```
pip install -r requirements.txt
```
**Configurar la conexión a MySQL**

Crea un archivo .env en la raíz del backend

```
MYSQL_HOST=localhost	
MYSQL_USER=your_user	
MYSQL_PASSWORD=your_password
MYSQL_DB=futbol_gestor
MYSQL_PORT=3306	
MYSQL_DB_TEST=futbol_gestor_test
```

### 3. Creación de la base de datos mediante Alembic

Ejecutar en terminal:

```
alembic upgrade head
```
Una vez se ha creado la base de datos
