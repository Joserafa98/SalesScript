from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuración ---
# Coloca el número de teléfono con el código de país, sin el "+"
# Ejemplo: "573001234567" para un número de Colombia
numero_telefono = "34641716268" 

# Mensaje que se enviará (opcional, se puede dejar vacío)
mensaje_a_enviar = "Si lees este mensaje, significa que funciona el script" 

# Crear el enlace wa.me con el número de teléfono y el mensaje
wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}&text={mensaje_a_enviar}"

driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")

print("Por favor, escanea el código QR de WhatsApp Web. Tienes 40 segundos.")
time.sleep(40) # Dale tiempo para escanear

# Navegar a la URL wa.me para abrir el chat
print(f"Abriendo chat con el número {numero_telefono}...")
driver.get(wa_me_url)

try:
    # Espera explícita para que el campo de texto del chat sea visible
    wait = WebDriverWait(driver, 10)
    # Busca el campo de texto. El 'data-testid' puede cambiar con las actualizaciones.
    # El selector 'p[class="selectable-text"]' es una alternativa si el anterior falla.
    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="attached-text-input-container"] p[class*="selectable-text"]'))
    )
    
    print("Campo de texto del chat encontrado. Listo para escribir.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
    print("No se pudo encontrar el campo de texto. Es posible que el número no sea válido o que el selector haya cambiado.")
    # El script termina aquí si hay un error

print("Script finalizado. Manteniendo el navegador abierto. Presiona Ctrl+C en la terminal para cerrar.")
while True:
    time.sleep(1)