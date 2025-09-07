from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- Configuración del script ---
# Coloca el número de teléfono con el código de país, sin el "+"
# Ejemplo: "34641716268" para un número de España
numero_telefono = "34641716268" 

# El mensaje que quieres enviar.
mensaje_a_enviar = "Hola, esto es un mensaje de prueba. ¿Cómo estás?" 

# Crear el enlace wa.me para abrir el chat
wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}"

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

print("Por favor, escanea el código QR de WhatsApp Web. Tienes 40 segundos.")
time.sleep(40) # Tiempo para escanear el QR

try:
    print(f"Abriendo chat con el número {numero_telefono}...")
    driver.get(wa_me_url)
    
    # Espera explícita para que la URL cargue y el campo de texto sea visible
    wait = WebDriverWait(driver, 15)
    
    # Intenta encontrar el campo de texto del chat usando el selector de contenteditable
    input_box = wait.until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
)

    
    print("Campo de texto del chat encontrado. Escribiendo...")
    
    # Escribir el mensaje caracter por caracter para un comportamiento más humano
    for caracter in mensaje_a_enviar:
        input_box.send_keys(caracter)
        # Pausa aleatoria entre 0.05 y 0.2 segundos para simular una escritura humana
        time.sleep(random.uniform(0.05, 0.2))

    # Presionar Enter para enviar el mensaje
    input_box.send_keys(Keys.ENTER)
    
    print("Mensaje enviado con éxito.")
    
except Exception as e:
    print(f"Ocurrió un error: {e}")
    print("No se pudo encontrar el campo de texto o el chat. Asegúrate de que el número es válido y que has escaneado el QR.")

# El script terminará una vez que el mensaje sea enviado.
print("Script finalizado. El navegador se cerrará automáticamente.")

driver.quit()