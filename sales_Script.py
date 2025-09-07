from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- Configuración del script ---
numero_telefono = "34641716268"  # Número de teléfono con código de país
mensaje_a_enviar = "Hola, esto es un mensaje de prueba. ¿Cómo estás?" 

# Crear el enlace wa.me para abrir el chat
wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}"

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

print("Por favor, escanea el código QR de WhatsApp Web. Tienes 40 segundos.")
time.sleep(40)  # Tiempo para escanear el QR

try:
    print(f"Abriendo chat con el número {numero_telefono}...")
    driver.get(wa_me_url)
    
    wait = WebDriverWait(driver, 20)
    input_box = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
    )
    
    print("Campo de texto del chat encontrado. Escribiendo mensaje...")
    
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
    
except Exception as e:
    print(f"Ocurrió un error: {e}")
    print("No se pudo enviar el mensaje. Verifica el número y que escaneaste el QR.")

print("Script finalizado. El navegador se cerrará automáticamente.")
time.sleep(3) 
driver.quit()
