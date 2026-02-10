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

# MODO DEBUG: True para ver más información
DEBUG_MODE = True

contactos = [
     "34641716268", 
     "50766365572", # Agrega tus números aquí con código de país
]

# Ruta de la imagen a enviar
RUTA_IMAGEN = "/Users/josehernandez/Downloads/Proyecto Jose/1.png"  # ⚠️ CAMBIAR ESTA RUTA
# Ejemplo Mac: "/Users/josehernandez/Documents/SCRIPT DE VENTAS/1.png"
# Si la imagen está en la misma carpeta que el script, usa solo: "1.png"

# Mensaje de texto
MENSAJE_TEXTO = "¡Hola! 👋 Mira esta oferta increíble que tenemos para ti 😍"

# Configuración de encuesta
ENCUESTA = {
    "pregunta": "¿Te interesa este producto?",
    "opciones": ["Sí, quiero más info 👍", "Tal vez más adelante 🤔"]
}

# ==================== CONFIGURACIÓN DE CHROME ====================
options = webdriver.ChromeOptions()

# User agent realista de Mac
options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

# Argumentos anti-detección
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)

# Argumentos adicionales para parecer más humano
options.add_argument("--disable-web-security")
options.add_argument("--disable-features=IsolateOrigins,site-per-process")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

# IMPORTANTE: Usar perfil de usuario de Chrome (OPCIONAL pero muy efectivo)
# Descomenta la siguiente línea y ajusta la ruta si quieres usar tu perfil real de Chrome:
# options.add_argument("--user-data-dir=/Users/josehernandez/Library/Application Support/Google/Chrome")
# options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=options)

# Scripts anti-detección
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
})

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-ES', 'es', 'en-US', 'en']
        });
        window.chrome = {
            runtime: {}
        };
    '''
})

# Detectar sistema operativo para el comando de pegar
PASTE_KEY = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

# ==================== FUNCIONES AUXILIARES ====================

def validar_numero(numero):
    """Valida que el número tenga el formato correcto"""
    # Eliminar espacios, guiones, paréntesis
    numero_limpio = ''.join(filter(str.isdigit, numero))
    
    # Debe tener entre 10 y 15 dígitos
    if len(numero_limpio) < 10 or len(numero_limpio) > 15:
        return False, f"Número muy corto o muy largo: {len(numero_limpio)} dígitos"
    
    # Si empieza con +, quitarlo
    if numero.startswith('+'):
        numero_limpio = numero[1:]
    
    return True, numero_limpio

def esperar_whatsapp_cargado():
    """Espera a que WhatsApp Web esté completamente cargado después del QR"""
    try:
        # Esperar a que aparezca la caja de búsqueda (señal de que WhatsApp está listo)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
        )
        print("✅ WhatsApp Web cargado correctamente")
        time.sleep(3)
        return True
    except:
        print("❌ Timeout esperando que WhatsApp cargue")
        return False

def escribir_con_delay(elemento, texto):
    """Escribe texto carácter por carácter para simular escritura humana"""
    for caracter in texto:
        pyperclip.copy(caracter)
        elemento.send_keys(PASTE_KEY, 'v')
        time.sleep(random.uniform(0.03, 0.15))

def enviar_imagen(ruta_imagen):
    """Envía una imagen adjunta"""
    try:
        if not os.path.exists(ruta_imagen):
            print(f"❌ No se encuentra la imagen: {ruta_imagen}")
            return False
        
        print(f"📷 Enviando imagen: {os.path.basename(ruta_imagen)}")
        
        # 1. Abrir menú de adjuntos - MÚLTIPLES MÉTODOS
        attach_opened = False
        
        # Método 1: Por título
        try:
            attach_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="Adjuntar"]'))
            )
            attach_button.click()
            attach_opened = True
            print("   ✓ Menú abierto (método 1)")
        except:
            pass
        
        # Método 2: Por icono clip
        if not attach_opened:
            try:
                attach_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')
                attach_button.click()
                attach_opened = True
                print("   ✓ Menú abierto (método 2)")
            except:
                pass
        
        # Método 3: Por aria-label
        if not attach_opened:
            try:
                attach_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Adjuntar"]')
                attach_button.click()
                attach_opened = True
                print("   ✓ Menú abierto (método 3)")
            except:
                pass
        
        # Método 4: Buscar por XPath
        if not attach_opened:
            try:
                attach_button = driver.find_element(By.XPATH, '//div[@title="Adjuntar" or @aria-label="Adjuntar"]')
                attach_button.click()
                attach_opened = True
                print("   ✓ Menú abierto (método 4)")
            except:
                pass
        
        if not attach_opened:
            print("   ❌ No se pudo abrir el menú de adjuntos")
            return False
        
        time.sleep(2)
        
        # 2. Buscar input de archivo (oculto) - MÚLTIPLES SELECTORES
        file_input = None
        
        # Probar varios selectores
        selectores_input = [
            'input[type="file"][accept*="image"]',
            'input[type="file"]',
            'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
        ]
        
        for selector in selectores_input:
            try:
                file_input = driver.find_element(By.CSS_SELECTOR, selector)
                if file_input:
                    print(f"   ✓ Input encontrado: {selector[:40]}...")
                    break
            except:
                continue
        
        if not file_input:
            print("   ❌ No se encontró el input de archivo")
            return False
        
        # 3. Enviar ruta de archivo
        ruta_absoluta = os.path.abspath(ruta_imagen)
        print(f"   📂 Ruta: {ruta_absoluta}")
        file_input.send_keys(ruta_absoluta)
        time.sleep(4)  # Esperar a que cargue el preview
        
        # 4. Esperar preview de imagen y botón de envío - MÚLTIPLES SELECTORES
        send_clicked = False
        
        # Selector 1: Por data-icon
        try:
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
            )
            send_button.click()
            send_clicked = True
            print("   ✓ Enviado (método 1)")
        except:
            pass
        
        # Selector 2: Por aria-label
        if not send_clicked:
            try:
                send_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Enviar"]')
                send_button.click()
                send_clicked = True
                print("   ✓ Enviado (método 2)")
            except:
                pass
        
        # Selector 3: Buscar botón con el icono específico de envío
        if not send_clicked:
            try:
                send_button = driver.find_element(By.XPATH, '//span[@data-icon="send" or @data-icon="send-light"]')
                driver.execute_script("arguments[0].click();", send_button)
                send_clicked = True
                print("   ✓ Enviado (método 3)")
            except:
                pass
        
        if not send_clicked:
            print("   ❌ No se pudo hacer clic en enviar")
            return False
        
        print("✅ Imagen enviada")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Error enviando imagen: {e}")
        import traceback
        traceback.print_exc()
        return False

def enviar_texto(mensaje):
    """Envía un mensaje de texto"""
    try:
        print("💬 Enviando mensaje de texto...")
        
        # Encontrar caja de texto
        text_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
        )
        text_box.click()
        time.sleep(0.5)
        
        # Escribir mensaje
        escribir_con_delay(text_box, mensaje)
        
        # Enviar
        text_box.send_keys(Keys.ENTER)
        print("✅ Texto enviado")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"❌ Error enviando texto: {e}")
        return False

def enviar_encuesta(pregunta, opciones):
    """Envía una encuesta de WhatsApp"""
    try:
        print(f"📊 Creando encuesta: {pregunta}")
        
        # 1. Abrir menú de adjuntos - MÚLTIPLES MÉTODOS
        attach_opened = False
        
        # Método 1: Por título
        try:
            attach_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="Adjuntar"]'))
            )
            attach_button.click()
            attach_opened = True
            print("   ✓ Menú adjuntos abierto")
        except:
            pass
        
        # Método 2: Por icono
        if not attach_opened:
            try:
                attach_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="attach-menu-plus"]')
                attach_button.click()
                attach_opened = True
                print("   ✓ Menú adjuntos abierto (icono)")
            except:
                pass
        
        # Método 3: Por aria-label
        if not attach_opened:
            try:
                attach_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Adjuntar"]')
                attach_button.click()
                attach_opened = True
                print("   ✓ Menú adjuntos abierto (aria)")
            except:
                pass
        
        # Método 4: Buscar cualquier botón de adjuntos
        if not attach_opened:
            try:
                # Buscar todos los botones y encontrar el de adjuntar
                buttons = driver.find_elements(By.TAG_NAME, 'button')
                for btn in buttons:
                    try:
                        if 'adjunt' in btn.get_attribute('aria-label').lower():
                            btn.click()
                            attach_opened = True
                            print("   ✓ Menú adjuntos abierto (búsqueda)")
                            break
                    except:
                        continue
            except:
                pass
        
        if not attach_opened:
            print("   ❌ No se pudo abrir menú de adjuntos")
            return False
        
        time.sleep(2)
        
        # 2. Buscar opción "Encuesta" o "Poll" - MÚLTIPLES MÉTODOS
        poll_found = False
        
        # Método 1: Por texto visible
        try:
            elementos = driver.find_elements(By.XPATH, "//*[contains(text(), 'Encuesta') or contains(text(), 'Poll')]")
            for elem in elementos:
                if elem.is_displayed():
                    elem.click()
                    poll_found = True
                    print("   ✅ Opción de encuesta encontrada (texto)")
                    break
        except:
            pass
        
        # Método 2: Por aria-label
        if not poll_found:
            try:
                poll_button = driver.find_element(By.CSS_SELECTOR, '[aria-label*="Encuesta" i], [aria-label*="Poll" i]')
                poll_button.click()
                poll_found = True
                print("   ✅ Opción de encuesta encontrada (aria)")
            except:
                pass
        
        # Método 3: Por data-icon
        if not poll_found:
            try:
                poll_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="poll"]')
                poll_button.click()
                poll_found = True
                print("   ✅ Opción de encuesta encontrada (icono)")
            except:
                pass
        
        # Método 4: Buscar en todos los elementos del menú
        if not poll_found:
            try:
                # Buscar todos los spans visibles
                spans = driver.find_elements(By.TAG_NAME, 'span')
                for span in spans:
                    try:
                        texto = span.text.lower()
                        if span.is_displayed() and ('encuesta' in texto or 'poll' in texto):
                            # Hacer clic en el elemento padre clickeable
                            parent = span.find_element(By.XPATH, './ancestor::*[@role="button" or @role="menuitem"][1]')
                            parent.click()
                            poll_found = True
                            print("   ✅ Opción de encuesta encontrada (búsqueda)")
                            break
                    except:
                        continue
            except:
                pass
        
        if not poll_found:
            print("   ❌ No se encontró la opción de encuesta en el menú")
            print("   💡 Verifica que tu cuenta tenga habilitada la función de encuestas")
            return False
        
        time.sleep(3)
        
        # 3. Escribir pregunta
        campos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
        )
        
        if len(campos) < 1:
            print("   ❌ No se encontraron campos para la encuesta")
            return False
        
        # Campo de pregunta
        campos[0].click()
        time.sleep(0.5)
        escribir_con_delay(campos[0], pregunta)
        time.sleep(1)
        print("   ✓ Pregunta escrita")
        
        # 4. Primera opción
        if len(campos) > 1:
            campos[1].click()
            time.sleep(0.5)
            escribir_con_delay(campos[1], opciones[0])
            time.sleep(1)
            print("   ✓ Opción 1 escrita")
        
        # 5. Añadir segunda opción
        if len(opciones) > 1:
            try:
                # Buscar botón "Añadir opción"
                add_buttons = driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'Añadir') or contains(text(), 'Add')]")
                
                for btn in add_buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        print("   ✓ Botón añadir clickeado")
                        time.sleep(2)
                        break
                
                # Escribir en el nuevo campo
                campos = driver.find_elements(By.CSS_SELECTOR, 'div[contenteditable="true"]')
                if len(campos) > 2:
                    campos[2].click()
                    time.sleep(0.5)
                    # Limpiar texto predeterminado
                    campos[2].send_keys(PASTE_KEY, 'a')
                    campos[2].send_keys(Keys.DELETE)
                    time.sleep(0.3)
                    escribir_con_delay(campos[2], opciones[1])
                    print("   ✓ Opción 2 escrita")
                
            except Exception as e:
                print(f"   ⚠️ Error añadiendo segunda opción: {e}")
        
        time.sleep(2)
        
        # 6. Enviar encuesta - MÚLTIPLES MÉTODOS
        send_clicked = False
        
        # Método 1: Por data-icon
        try:
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="send"]'))
            )
            driver.execute_script("arguments[0].click();", send_button)
            send_clicked = True
            print("   ✓ Encuesta enviada (método 1)")
        except:
            pass
        
        # Método 2: Por aria-label
        if not send_clicked:
            try:
                send_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Enviar"]')
                send_button.click()
                send_clicked = True
                print("   ✓ Encuesta enviada (método 2)")
            except:
                pass
        
        # Método 3: Buscar por XPath
        if not send_clicked:
            try:
                send_button = driver.find_element(By.XPATH, '//div[@aria-label="Enviar"]')
                send_button.click()
                send_clicked = True
                print("   ✓ Encuesta enviada (método 3)")
            except:
                pass
        
        if not send_clicked:
            print("   ❌ No se pudo enviar la encuesta")
            return False
        
        print("✅ Encuesta enviada")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Error general en encuesta: {e}")
        import traceback
        traceback.print_exc()
        return False

# ==================== SCRIPT PRINCIPAL ====================

try:
    # Abrir WhatsApp Web
    print("🌐 Abriendo WhatsApp Web...")
    driver.get("https://web.whatsapp.com/")
    
    print("📲 Escanea el QR (60s)...")
    
    # Esperar a que WhatsApp cargue
    if not esperar_whatsapp_cargado():
        print("❌ WhatsApp no cargó correctamente")
        driver.quit()
        exit()
    
    # Validar que hay contactos
    if not contactos:
        print("⚠️  No hay contactos en la lista. Agrega números en la variable 'contactos'")
        driver.quit()
        exit()
    
    # Procesar cada contacto
    for numero in contactos:
        try:
            # Validar número
            valido, resultado = validar_numero(numero)
            if not valido:
                print(f"\n⚠️  Número inválido: {numero}")
                print(f"   Razón: {resultado}")
                continue
            
            numero_limpio = resultado
            
            print(f"\n{'='*50}")
            print(f"📱 Procesando: {numero_limpio}")
            print(f"{'='*50}")
            
            # 1. Abrir chat
            wa_url = f"https://web.whatsapp.com/send/?phone={numero_limpio}&text&type=phone_number&app_absent=0"
            driver.get(wa_url)
            print(f"   🔗 Abriendo: {wa_url}")
            time.sleep(8)  # Más tiempo para cargar
            
            # Verificar que el chat se abrió - MÉTODO MEJORADO
            chat_abierto = False
            
            # Intentar múltiples selectores
            selectores_chat = [
                'div[contenteditable="true"][data-tab="10"]',  # Selector principal
                'div[contenteditable="true"][data-lexical-editor="true"]',  # Nuevo formato
                'div[role="textbox"]',  # Genérico
                'footer div[contenteditable="true"]'  # Alternativo
            ]
            
            for selector in selectores_chat:
                try:
                    elemento = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if elemento.is_displayed():
                        print(f"✅ Chat abierto (selector: {selector[:30]}...)")
                        chat_abierto = True
                        break
                except:
                    continue
            
            if not chat_abierto:
                print("❌ No se pudo abrir el chat")
                print("   ℹ️  Posibles causas:")
                print("      - El número no existe en WhatsApp")
                print("      - El número no tiene el formato correcto")
                print("      - WhatsApp bloqueó temporalmente la acción")
                
                if DEBUG_MODE:
                    print("\n   🔍 MODO DEBUG - Información de la página:")
                    print(f"      URL actual: {driver.current_url}")
                    print(f"      Título: {driver.title}")
                    
                    # Buscar mensajes de error
                    try:
                        errores = driver.find_elements(By.XPATH, "//*[contains(text(), 'no válido') or contains(text(), 'not valid') or contains(text(), 'doesn')]")
                        if errores:
                            print(f"      ⚠️  Mensaje de error detectado: {errores[0].text}")
                    except:
                        pass
                
                # Tomar screenshot para debug
                screenshot_path = f"/tmp/whatsapp_error_{numero_limpio}.png"
                driver.save_screenshot(screenshot_path)
                print(f"   📸 Screenshot guardado en: {screenshot_path}")
                
                # Esperar antes de continuar
                time.sleep(3)
                continue
            
            # 2. Enviar imagen
            if RUTA_IMAGEN:
                enviar_imagen(RUTA_IMAGEN)
            
            # 3. Enviar texto
            if MENSAJE_TEXTO:
                enviar_texto(MENSAJE_TEXTO)
            
            # 4. Enviar encuesta
            if ENCUESTA:
                enviar_encuesta(ENCUESTA["pregunta"], ENCUESTA["opciones"])
            
            # Espera aleatoria antes del siguiente contacto
            if numero != contactos[-1]:  # Si no es el último
                wait_time = random.uniform(30, 45)
                print(f"\n⏳ Esperando {wait_time:.1f}s antes del siguiente contacto...")
                time.sleep(wait_time)
            
        except Exception as e:
            print(f"❌ Error con {numero}: {e}")
            continue
    
    print("\n" + "="*50)
    print("✅ Todos los contactos procesados")
    print("="*50)

except KeyboardInterrupt:
    print("\n⚠️ Script interrumpido por el usuario")
except Exception as e:
    print(f"\n❌ Error fatal: {e}")
finally:
    time.sleep(3)
    driver.quit()
    print("🔚 Navegador cerrado")