from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pyperclip
import platform  # Para detectar sistema operativo

# --- Configuración del script ---
contactos = [
    "34641716268",
    "50766365572",
    "50760312294",
    "50767494746"
]

mensajes = [
    "Hola, esto es un mensaje de prueba. ¿Cómo estás?😍",
    "¡Hola! Espero que estés teniendo un buen día 😊",
    "¡Saludos! Quería enviarte este mensaje de prueba. 🧐"
]

ruta_imagen = "/Users/josehernandez/Downloads/Diseño sin título.png"  # Ruta absoluta de la imagen

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

print("Por favor, escanea el código QR de WhatsApp Web. Tienes 40 segundos.")
time.sleep(40)

wait = WebDriverWait(driver, 20)
ultimo_mensaje = None

# Detectar tecla de pegar según sistema operativo
paste_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

for numero_telefono in contactos:
    try:
        print(f"Abriendo chat con el número {numero_telefono}...")
        wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}"
        driver.get(wa_me_url)

        # --- Pulsar botón + (clip) ---
        clip_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-icon="plus-rounded"]'))
        )
        clip_button.click()
        time.sleep(2)  # Pequeña espera para que aparezca el panel

        # --- Subir imagen ---
        file_input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file" and contains(@accept,"image")]'))
        )
        file_input.send_keys(ruta_imagen)
        time.sleep(3)  # Esperar a que cargue la vista previa

        # --- Elegir mensaje aleatorio distinto al último ---
        mensaje_a_enviar = random.choice(mensajes)
        while mensaje_a_enviar == ultimo_mensaje and len(mensajes) > 1:
            mensaje_a_enviar = random.choice(mensajes)
        ultimo_mensaje = mensaje_a_enviar

        # --- Escribir mensaje debajo de la imagen ---
        caption_box = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]'))
        )
        print(f"Escribiendo mensaje a {numero_telefono}...")
        for caracter in mensaje_a_enviar:
            pyperclip.copy(caracter)
            caption_box.send_keys(paste_key, 'v')
            time.sleep(random.uniform(0.05, 0.2))

        # --- Enviar imagen con mensaje ---
        send_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_button.click()
        print("Mensaje con imagen enviado ✅")

        # --- Espera aleatoria entre contactos ---
        wait_time = random.uniform(25, 40)
        print(f"Esperando {wait_time:.2f} segundos antes del siguiente contacto...")
        time.sleep(wait_time)

    except Exception as e:
        print(f"Ocurrió un error con el contacto {numero_telefono}: {e}")
        print("Saltando al siguiente contacto...")

print("Todos los mensajes han sido procesados.")
time.sleep(3)
driver.quit()
