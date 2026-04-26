Sistema de Login Facial
Sistema de inicio de sesión seguro con verificación facial usando DeepFace y OpenCV.
Requisitos
Python 3.10+
Cámara web
Instalación
```bash
# 1. Clonar o descargar el proyecto
cd face_login

# 2. Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```
> La primera ejecución descargará automáticamente los pesos del modelo Facenet (~90 MB).
Uso
```bash
python app.py
```
Menú principal
```
╔══════════════════════════════════════╗
║   SISTEMA DE LOGIN FACIAL  v1.0      ║
║   Powered by DeepFace + OpenCV       ║
╚══════════════════════════════════════╝

  [1] Registrar nuevo usuario
  [2] Iniciar sesión
  [3] Ver usuarios registrados
  [4] Salir
```
Flujo de uso
Registrar → Elige `[1]`, escribe tu nombre y presiona `ESPACIO` cuando tu rostro esté centrado en el óvalo.
Iniciar sesión → Elige `[2]`, mira a la cámara y presiona `ESPACIO`. El sistema comparará tu rostro contra todos los usuarios registrados.
Si el rostro coincide → acceso concedido y sesión iniciada.
Si no coincide → acceso denegado.
Estructura del proyecto
```
face_login/
├── app.py                  # Aplicación principal
├── requirements.txt        # Dependencias
├── README.md               # Este archivo
├── users.json              # Base de datos de usuarios (se crea automáticamente)
└── registered_users/       # Fotos de registro (se crea automáticamente)
```
Modelo utilizado
Parámetro	Valor
Modelo	Facenet
Métrica	Coseno
Backend detector	OpenCV
Notas
Los datos (fotos y `users.json`) se almacenan localmente, nunca se envían a ningún servidor.
Puedes registrar múltiples usuarios; el sistema verificará contra todos al hacer login.