import os
import cv2
import json
import time
import numpy as np
from deepface import DeepFace


USERS_DIR   = "registered_users"
DB_FILE     = "users.json"
MODEL       = "Facenet"          # rápido y preciso
THRESHOLD   = 0.6                # distancia coseno máxima para verificar

os.makedirs(USERS_DIR, exist_ok=True)

#
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def capture_face(prompt: str) -> np.ndarray | None:
    """Abre la cámara, muestra un preview y captura un frame al presionar SPACE."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("  ✗ No se pudo acceder a la cámara.")
        return None

    print(f"\n  {prompt}")
    print("  Presiona ESPACIO para capturar · ESC para cancelar\n")

    frame_out = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        
        h, w = display.shape[:2]
        cx, cy, r = w // 2, h // 2, 120
        cv2.ellipse(display, (cx, cy), (r, int(r * 1.3)), 0, 0, 360, (0, 255, 100), 2)
        cv2.putText(display, prompt, (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 100), 2)
        cv2.putText(display, "ESPACIO = capturar  |  ESC = cancelar",
                    (20, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.imshow("Face Login", display)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:          
            break
        elif key == 32:        
            frame_out = frame
            break

    cap.release()
    cv2.destroyAllWindows()
    return frame_out

# ─registro de nuevo usuario, captura su rostro y lo guarda en la base de datos
def register():
    print("\n─── REGISTRO DE NUEVO USUARIO ───────────────────────────────")
    username = input("  Nombre de usuario: ").strip()
    if not username:
        print("  ✗ Nombre inválido.")
        return

    db = load_db()
    if username in db:
        print(f"  ✗ El usuario '{username}' ya existe.")
        return

    frame = capture_face("Coloca tu rostro en el óvalo")
    if frame is None:
        print("  ✗ Captura cancelada.")
        return

    # verifica que se detecte un rostro antes de guardar
    try:
        DeepFace.extract_faces(frame, detector_backend="opencv", enforce_detection=True)
    except Exception:
        print("  ✗ No se detectó ningún rostro. Inténtalo de nuevo.")
        return

    img_path = os.path.join(USERS_DIR, f"{username}.jpg")
    cv2.imwrite(img_path, frame)

    db[username] = {"image": img_path}
    save_db(db)
    print(f"\n  ✓ Usuario '{username}' registrado exitosamente.")

# login
def login():
    print("\n─── INICIO DE SESIÓN ────────────────────────────────────────")
    db = load_db()
    if not db:
        print("  ✗ No hay usuarios registrados. Registra uno primero.")
        return

    frame = capture_face("Mira a la cámara para iniciar sesión")
    if frame is None:
        print("  ✗ Captura cancelada.")
        return

    temp_path = "temp/login_attempt.jpg"
    os.makedirs("temp", exist_ok=True)
    cv2.imwrite(temp_path, frame)

    print("\n  Verificando identidad", end="", flush=True)
    matched_user = None
    best_distance = float("inf")

    for username, info in db.items():
        print(".", end="", flush=True)
        try:
            result = DeepFace.verify(
                img1_path=temp_path,
                img2_path=info["image"],
                model_name=MODEL,
                distance_metric="cosine",
                enforce_detection=False,
            )
            dist = result["distance"]
            if result["verified"] and dist < best_distance:
                best_distance = dist
                matched_user = username
        except Exception:
            continue

    print()  
    if matched_user:
        print(f"\n  ✓ ¡Bienvenido, {matched_user}! Acceso concedido.")
        print(f"    (distancia: {best_distance:.4f})")
        session(matched_user)
    else:
        print("\n  ✗ Acceso denegado. Rostro no reconocido.")

# sesion activa (simulada) para el usuario autenticado
def session(username: str):
    print(f"\n  ══ Sesión activa para: {username} ══")
    print("  • Cargando preferencias personales...")
    time.sleep(0.5)
    print("  • Sincronizando datos...")
    time.sleep(0.5)
    print("  • Panel listo.\n")
    input("  Presiona ENTER para cerrar sesión...")
    print(f"  Sesión de '{username}' cerrada.")

# lista los usuarios registrados 
def list_users():
    db = load_db()
    if not db:
        print("\n  No hay usuarios registrados.")
    else:
        print(f"\n  Usuarios registrados ({len(db)}):")
        for u in db:
            print(f"    • {u}")

# menu  
def main():
    menu = {
        "1": ("Registrar nuevo usuario", register),
        "2": ("Iniciar sesión",          login),
        "3": ("Ver usuarios registrados", list_users),
        "4": ("Salir",                   None),
    }

    print("\n╔══════════════════════════════════════╗")
    print("║   SISTEMA DE LOGIN FACIAL  v1.0      ║")
    print("║   Powered by DeepFace + OpenCV       ║")
    print("╚══════════════════════════════════════╝")

    while True:
        print("\n  Opciones:")
        for k, (label, _) in menu.items():
            print(f"    [{k}] {label}")
        choice = input("\n  Selecciona una opción: ").strip()

        if choice == "4":
            print("\n  Hasta luego.\n")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("  Opción inválida.")

if __name__ == "__main__":
    main()
