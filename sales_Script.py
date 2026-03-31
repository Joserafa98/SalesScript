from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pyperclip
import platform
import os

# ==================== CONFIGURACIÓN ====================

DEBUG_MODE = True

contactos = [
    "34641716268", 
    "50766365572",
]

# Ruta de la imagen a enviar
RUTA_IMAGEN = "/Users/josehernandez/Downloads/Proyecto Jose.png"
IMAGEN_CAPTION = " "  # Déjalo en "" si no quieres texto

# Mensaje de texto
MENSAJE_TEXTO = "¡Hola! 👋 Mira esta oferta increíble que tenemos para ti 😍"

# Configuración de encuesta
ENCUESTA = {
    "pregunta": "¿Te interesa este producto?",
    "opciones": ["Sí, quiero más info 👍", "Tal vez más adelante 🤔"]
}

# ==================== CHROME ====================
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

PASTE_KEY = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

# ==================== FUNCIONES ====================

def validar_numero(numero):
    numero_limpio = ''.join(filter(str.isdigit, numero))
    if len(numero_limpio) < 10 or len(numero_limpio) > 15:
        return False, f"Número inválido"
    return True, numero_limpio

def esperar_whatsapp():
    try:
        # Aquí es donde cambiamos el selector para que lo detecte al instante
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Lista de chats"], div[role="grid"]'))
        )
        print("✅ WhatsApp listo")
        time.sleep(3)
        return True
    except:
        print("❌ Timeout")
        return False

def escribir(elemento, texto):
    for char in texto:
        pyperclip.copy(char)
        elemento.send_keys(PASTE_KEY, 'v')
        time.sleep(random.uniform(0.03, 0.15))

def enviar_imagen(ruta, caption=""):
    try:
        if not os.path.exists(ruta):
            print(f"❌ No existe: {ruta}")
            return False

        print(f"📷 Enviando: {os.path.basename(ruta)}")

        # 1. Abrir menú adjuntos
        menu_abierto = False
        
        # Método 1: Por aria-label en button
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Adjuntar"]'))
            )
            btn.click()
            menu_abierto = True
            print("   ✓ Menú abierto")
        except:
            pass
        
        # Método 2: Por data-icon del SVG
        if not menu_abierto:
            try:
                icon = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="plus-rounded"]')
                # Subir hasta el botón
                btn = icon.find_element(By.XPATH, './ancestor::button[1]')
                btn.click()
                menu_abierto = True
                print("   ✓ Menú abierto (icono)")
            except:
                pass
        
        # Método 3: Por data-tab
        if not menu_abierto:
            try:
                btn = driver.find_element(By.CSS_SELECTOR, 'button[data-tab="10"][aria-label="Adjuntar"]')
                btn.click()
                menu_abierto = True
                print("   ✓ Menú abierto (data-tab)")
            except:
                pass
        
        if not menu_abierto:
            print("   ❌ No se abrió menú")
            return False
        
        time.sleep(2)

        # 2. Clic en "Fotos y videos"
        try:
            # Método 1: Por texto
            xpath = "//span[contains(text(), 'Fotos y videos')]"
            elem = driver.find_element(By.XPATH, xpath)
            parent = elem.find_element(By.XPATH, './ancestor::div[@role="menuitem"][1]')
            parent.click()
            print("   ✓ 'Fotos y videos' clickeado")
        except:
            try:
                # Método 2: Por aria-label
                btn = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Fotos y videos"]')
                btn.click()
                print("   ✓ 'Fotos y videos' clickeado")
            except:
                print("   ❌ No se encontró 'Fotos y videos'")
                return False
        
        time.sleep(2)

        # 3. Subir archivo
        inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
        print(f"   🔍 DEBUG: Se encontraron {len(inputs)} inputs")
        
        for i, inp in enumerate(inputs):
            accept = inp.get_attribute('accept') or 'sin accept'
            multiple = inp.get_attribute('multiple') or 'no'
            print(f"      Input {i+1}: accept='{accept[:50]}', multiple='{multiple}'")
        
        if not inputs:
            print("   ❌ No hay input")
            return False
        
        # CORRECCIÓN: Usar el input con multiple="true" (ese es el de FOTOS)
        file_input = None
        for inp in inputs:
            accept = inp.get_attribute('accept') or ''
            multiple = inp.get_attribute('multiple')
            
            # El input de FOTOS tiene: multiple=true Y acepta videos
            if multiple and 'video' in accept:
                file_input = inp
                print(f"   ✅ Input CORRECTO (Fotos con video): {accept[:50]}")
                break
        
        # Si no se encuentra, intentar el que tenga multiple
        if not file_input:
            for inp in inputs:
                if inp.get_attribute('multiple'):
                    file_input = inp
                    print(f"   ✓ Input con multiple seleccionado")
                    break
        
        # Último recurso: usar el segundo input (suele ser el de fotos)
        if not file_input and len(inputs) >= 2:
            file_input = inputs[1]  # Input 2 en lugar del 1
            print(f"   ✓ Usando Input 2 (fotos)")
        elif not file_input:
            file_input = inputs[0]
            print(f"   ⚠️  Usando primer input")
        
        ruta_abs = os.path.abspath(ruta)
        file_input.send_keys(ruta_abs)
        print(f"   ✓ Archivo enviado al input")
        time.sleep(4)

        # 4. Caption (opcional)
        if caption:
            try:
                box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][aria-label="Escribe un mensaje"]'))
                )
                box.click()
                time.sleep(0.3)
                escribir(box, caption)
                print("   ✓ Caption añadido")
            except:
                print("   ⚠️ Sin caption")

        # 5. Enviar
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Enviar"]'))
            )
            btn.click()
            print("✅ Imagen enviada")
            time.sleep(3)
            return True
        except:
            try:
                btn = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="send"]')
                parent = btn.find_element(By.XPATH, './ancestor::div[@role="button"][1]')
                parent.click()
                print("✅ Imagen enviada")
                time.sleep(3)
                return True
            except:
                print("❌ No se envió")
                return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def enviar_texto(msg):
    try:
        print("💬 Enviando texto...")
        box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
        )
        box.click()
        time.sleep(0.5)
        escribir(box, msg)
        box.send_keys(Keys.ENTER)
        print("✅ Texto enviado")
        time.sleep(2)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def enviar_encuesta(pregunta, opciones):
    try:
        print(f"📊 Encuesta: {pregunta}")

        # Abrir menú
        menu_abierto = False
        
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Adjuntar"]'))
            )
            btn.click()
            menu_abierto = True
        except:
            pass
        
        if not menu_abierto:
            try:
                icon = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="plus-rounded"]')
                btn = icon.find_element(By.XPATH, './ancestor::button[1]')
                btn.click()
                menu_abierto = True
            except:
                pass
        
        if not menu_abierto:
            print("   ❌ No se abrió menú")
            return False
        
        time.sleep(2)

        # Buscar "Encuesta"
        try:
            elems = driver.find_elements(By.XPATH, "//*[contains(text(), 'Encuesta')]")
            for e in elems:
                if e.is_displayed():
                    e.click()
                    print("   ✓ Opción encuesta")
                    break
        except:
            print("   ❌ No hay encuesta")
            return False
        
        time.sleep(3)

        # Escribir campos
        campos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
        )
        
        if len(campos) < 1:
            print("   ❌ No hay campos")
            return False

        # Pregunta
        campos[0].click()
        time.sleep(0.5)
        escribir(campos[0], pregunta)
        print("   ✓ Pregunta")

        # Opción 1
        if len(campos) > 1:
            campos[1].click()
            time.sleep(0.5)
            escribir(campos[1], opciones[0])
            print("   ✓ Opción 1")

        # Añadir opción 2
        if len(opciones) > 1:
            try:
                btns = driver.find_elements(By.XPATH, "//*[contains(text(), 'Añadir')]")
                for btn in btns:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(2)
                        break
                
                campos = driver.find_elements(By.CSS_SELECTOR, 'div[contenteditable="true"]')
                if len(campos) > 2:
                    campos[2].click()
                    time.sleep(0.5)
                    campos[2].send_keys(PASTE_KEY, 'a')
                    campos[2].send_keys(Keys.DELETE)
                    time.sleep(0.3)
                    escribir(campos[2], opciones[1])
                    print("   ✓ Opción 2")
            except:
                print("   ⚠️ Solo 1 opción")

        time.sleep(2)

        # Enviar
        try:
            btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Enviar"]'))
            )
            btn.click()
            print("✅ Encuesta enviada")
            time.sleep(3)
            return True
        except:
            btn = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="send"]')
            parent = btn.find_element(By.XPATH, './ancestor::div[@role="button"][1]')
            parent.click()
            print("✅ Encuesta enviada")
            time.sleep(3)
            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ==================== MAIN ====================

try:
    driver.get("https://web.whatsapp.com/")
    print("📲 Escanea QR (60s)...")
    
    if not esperar_whatsapp():
        driver.quit()
        exit()

    if not contactos:
        print("⚠️ No hay contactos")
        driver.quit()
        exit()

    for numero in contactos:
        valido, limpio = validar_numero(numero)
        if not valido:
            print(f"\n⚠️ Número inválido: {numero}")
            continue

        print(f"\n{'='*50}")
        print(f"📱 {limpio}")
        print(f"{'='*50}")

        # Abrir chat
        url = f"https://web.whatsapp.com/send/?phone={limpio}&text&type=phone_number&app_absent=0"
        driver.get(url)
        time.sleep(8)

        # Verificar chat abierto
        chat_ok = False
        selectores = [
            'div[contenteditable="true"][data-tab="10"]',
            'div[role="textbox"]'
        ]
        for sel in selectores:
            try:
                elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                if elem.is_displayed():
                    print("✅ Chat abierto")
                    chat_ok = True
                    break
            except:
                continue

        if not chat_ok:
            print("❌ No se abrió chat")
            continue

        # Enviar
        if RUTA_IMAGEN:
            enviar_imagen(RUTA_IMAGEN, IMAGEN_CAPTION)
        
        if MENSAJE_TEXTO:
            enviar_texto(MENSAJE_TEXTO)
        
        if ENCUESTA:
            enviar_encuesta(ENCUESTA["pregunta"], ENCUESTA["opciones"])

        # Espera entre contactos
        if numero != contactos[-1]:
            wait = random.uniform(30, 45)
            print(f"\n⏳ {wait:.1f}s...")
            time.sleep(wait)

    print("\n" + "="*50)
    print("✅ Finalizado")
    print("="*50)

except KeyboardInterrupt:
    print("\n⚠️ Interrumpido")
except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    time.sleep(3)
    driver.quit()
    print("🔚 Cerrado")
