from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()

print("WebDriver de Chrome iniciado.")

print("Abriendo WhatsApp Web...")
driver.get("https://web.whatsapp.com/")

# --- Esperar Autenticación ---
# Este tiempo es CRUCIAL para que puedas escanear el código QR con tu teléfono.
# Ajusta este tiempo si necesitas más o menos.
print("Por favor, escanea el código QR de WhatsApp Web con tu teléfono.")
print("Tienes 60 segundos para hacerlo.")
time.sleep(30) # Espera 60 segundos

print("¡WhatsApp Web debería estar abierto y conectado!")

# --- Mantener la ventana abierta por un tiempo (opcional) ---
# Puedes descomentar la siguiente línea si quieres que la ventana permanezca abierta
# después de que el script parezca haber terminado, para que puedas verla.
time.sleep(10) # Mantiene la ventana abierta 10 segundos más

# --- Cerrar el Navegador ---
# Una vez que termines de interactuar o para finalizar el script, descomenta la línea de abajo.
# driver.quit()
# print("Navegador cerrado.")

print("Script de apertura de WhatsApp Web finalizado.")