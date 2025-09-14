from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- Configuración del script ---
contactos = [
    "34641716268",
    "50766365572",
    "50760312294",
    "50767494746"
]  # Lista de contactos con código de país

mensajes = [
    "Hola, esto es un mensaje de prueba. ¿Cómo estás?😍",
    "¡Hola! Espero que estés teniendo un buen día 😊",
    "¡Saludos! Quería enviarte este mensaje de prueba. 🧐"
]  # Varias opciones de mensajes para variar

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

print("Por favor, escanea el código QR de WhatsApp Web. Tienes 40 segundos.")
time.sleep(40)  # Tiempo para escanear el QR

wait = WebDriverWait(driver, 20)

ultimo_mensaje = None  # Guardará el último mensaje enviado

for numero_telefono in contactos:
    try:
        print(f"Abriendo chat con el número {numero_telefono}...")
        wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}"
        driver.get(wa_me_url)

        input_box = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )

        # --- Elegir mensaje aleatorio distinto al último ---
        mensaje_a_enviar = random.choice(mensajes)
        while mensaje_a_enviar == ultimo_mensaje and len(mensajes) > 1:
            mensaje_a_enviar = random.choice(mensajes)

        ultimo_mensaje = mensaje_a_enviar

        print(f"Escribiendo mensaje a {numero_telefono}...")
        for caracter in mensaje_a_enviar:
            input_box.send_keys(caracter)
            time.sleep(random.uniform(0.05, 0.2))  # Simula escritura humana

        # --- Enviar mensaje ---
        enviar_con_boton = random.choice([True, False])  # 50/50: botón o ENTER

        if enviar_con_boton:
            try:
                print("Intentando enviar con botón de enviar...")
                send_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]'))
                )
                send_button.click()
                print("Mensaje enviado con botón de enviar ✅")
            except Exception as e:
                print(f"Error con botón: {e}")
                print("Usando ENTER como respaldo...")
                input_box.send_keys(Keys.ENTER)
                print("Mensaje enviado con ENTER ✅")
        else:
            print("Enviando con ENTER directamente...")
            input_box.send_keys(Keys.ENTER)
            print("Mensaje enviado con ENTER ✅")

        # --- Espera aleatoria entre contactos ---
        wait_time = random.uniform(25, 40)  # Entre 2 y 5 segundos
        print(f"Esperando {wait_time:.2f} segundos antes del siguiente contacto...")
        time.sleep(wait_time)

    except Exception as e:
        print(f"Ocurrió un error con el contacto {numero_telefono}: {e}")
        print("Saltando al siguiente contacto...")

print("Todos los mensajes han sido procesados.")
time.sleep(3)
driver.quit()
