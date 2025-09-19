from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import pyperclip
import platform
import os

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

ruta_imagen = "/Users/josehernandez/Downloads/Diseño sin título.png"
if not os.path.exists(ruta_imagen):
    print(f"Error: La imagen no existe en la ruta: {ruta_imagen}")
    exit()

# Configurar opciones de Chrome
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Abrir WhatsApp Web
driver.get("https://web.whatsapp.com/")

print("Por favor, escanea el código QR de WhatsApp Web. Tienes 60 segundos.")
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
    )
    print("QR escaneado correctamente. WhatsApp Web está listo.")
except TimeoutException:
    print("Tiempo de espera agotado para escanear el QR.")
    driver.quit()
    exit()

wait = WebDriverWait(driver, 20)
ultimo_mensaje = None

# Detectar tecla de pegar según sistema operativo
paste_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

for numero_telefono in contactos:
    try:
        print(f"Abriendo chat con el número {numero_telefono}...")
        wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}&text&type=phone_number&app_absent=0"
        driver.get(wa_me_url)
        
        # Esperar a que el chat cargue completamente
        try:
            chat_loaded = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            time.sleep(2)
        except TimeoutException:
            print(f"No se pudo cargar el chat para {numero_telefono}. Saltando...")
            continue

        # --- PRIMERO: Enviar la imagen ---
        try:
            # Pulsar botón adjuntar
            clip_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@title="Adjuntar" or @aria-label="Adjuntar"]'))
            )
            clip_button.click()
            time.sleep(1)
            
            # Subir imagen
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type="file" and @accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
            )
            file_input.send_keys(os.path.abspath(ruta_imagen))
            
            # Esperar a que cargue la vista previa
            time.sleep(3)
            
            # Enviar imagen sin texto
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            print("Imagen enviada ✅")
            time.sleep(2)  # Esperar a que se envíe la imagen
            
        except Exception as e:
            print(f"Error al enviar la imagen: {e}")
            # Intentar cerrar cualquier panel abierto
            try:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(1)
            except:
                pass
            continue

        # --- Cerrar cualquier panel abierto ---
        try:
            # Intentar cerrar el panel de adjuntar presionando ESC
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)
            
            # Hacer clic en un área neutral para asegurar que el panel se cierra
            header = driver.find_element(By.XPATH, '//header')
            header.click()
            time.sleep(1)
        except:
            pass

        # --- SEGUNDO: Enviar el texto como mensaje separado ---
        try:
            # Elegir mensaje aleatorio
            if len(mensajes) > 1:
                mensaje_a_enviar = random.choice([m for m in mensajes if m != ultimo_mensaje])
            else:
                mensaje_a_enviar = mensajes[0]
            ultimo_mensaje = mensaje_a_enviar

            # Localizar el cuadro de texto normal del chat
            text_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Usar JavaScript para hacer clic si es necesario
            driver.execute_script("arguments[0].click();", text_box)
            time.sleep(0.5)
            
            # Escribir carácter por carácter con efecto de typeo
            print(f"Escribiendo mensaje a {numero_telefono}...")
            for caracter in mensaje_a_enviar:
                pyperclip.copy(caracter)
                text_box.send_keys(paste_key, 'v')
                time.sleep(random.uniform(0.05, 0.2))
                
            # Enviar mensaje de texto
            text_box.send_keys(Keys.ENTER)
            print("Mensaje de texto enviado ✅")
            
        except Exception as e:
            print(f"Error al enviar el texto: {e}")
            continue

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