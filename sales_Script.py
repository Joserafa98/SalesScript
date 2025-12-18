from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pyperclip
import platform

# --- Configuración del script ---
contactos = [
    
]

mensajes = [
    "Hola, esto es un mensaje de prueba. ¿Cómo estás?😍",
    "¡Hola! Espero que estés teniendo un buen día 😊",
    "¡Saludos! Quería enviarte este mensaje de prueba. 🧐"
]

# --- Configuración de encuestas (TU CONTENIDO SE MANTIENE) ---
encuestas = [
    {
        "pregunta": "¿Te gustó nuestro servicio?",
        "opciones": ["Sí, mucho 👍", "Podría mejorar 🤔"]
    },
    {
        "pregunta": "¿Recomendarías nuestros productos?",
        "opciones": ["Definitivamente sí 🎉", "Tal vez más adelante ⏳"]
    }
]

# --- Configurar opciones de Chrome ---
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# --- Abrir WhatsApp Web ---
driver.get("https://web.whatsapp.com/")
print("Por favor, escanea el código QR de WhatsApp Web. Tienes 60 segundos.")

wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
print("QR escaneado correctamente. WhatsApp Web está listo.")

ultimo_mensaje = None
paste_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

for numero_telefono in contactos:
    try:
        print(f"Abriendo chat con el número {numero_telefono}...")
        wa_me_url = f"https://web.whatsapp.com/send/?phone={numero_telefono}&text&type=phone_number&app_absent=0"
        driver.get(wa_me_url)
        time.sleep(5)

        # --- ENVIAR TEXTO ---
        try:
            if len(mensajes) > 1:
                mensaje_a_enviar = random.choice([m for m in mensajes if m != ultimo_mensaje])
            else:
                mensaje_a_enviar = mensajes[0]

            ultimo_mensaje = mensaje_a_enviar

            text_box = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
            )
            driver.execute_script("arguments[0].click();", text_box)
            time.sleep(0.5)

            print(f"Escribiendo mensaje a {numero_telefono}...")
            for caracter in mensaje_a_enviar:
                pyperclip.copy(caracter)
                text_box.send_keys(paste_key, 'v')
                time.sleep(random.uniform(0.05, 0.2))

            text_box.send_keys(Keys.ENTER)
            print("Mensaje de texto enviado ✅")
            time.sleep(2)

        except Exception as e:
            print(f"Error al enviar el texto: {e}")
            continue

        # --- ENVIAR ENCUESTA (VERSIÓN ACTUALIZADA 2025) ---
        try:
            encuesta = random.choice(encuestas)
            print(f"Preparando encuesta: {encuesta['pregunta']}")
            
            # 1. Abrir menú de adjuntos - SELECTORES ACTUALES
            try:
                # Selector 1: Por data-testid (actual)
                attach_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-testid="conversation-menu"]'))
                )
                attach_button.click()
            except:
                try:
                    # Selector 2: Por aria-label
                    attach_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Adjuntar"]')
                    attach_button.click()
                except:
                    # Selector 3: Por title
                    attach_button = driver.find_element(By.CSS_SELECTOR, 'div[title="Adjuntar"]')
                    attach_button.click()
            
            time.sleep(2)
            
            # 2. Buscar opción de encuesta
            print("Buscando opción de encuesta...")
            
            # Método A: Buscar por texto "Encuesta" o "Poll"
            try:
                elementos_texto = driver.find_elements(By.XPATH, "//*[contains(text(), 'Encuesta') or contains(text(), 'Poll')]")
                if elementos_texto:
                    # Filtrar elementos visibles
                    elementos_visibles = [e for e in elementos_texto if e.is_displayed()]
                    if elementos_visibles:
                        elementos_visibles[0].click()
                        print("✅ Encuesta encontrada por texto")
                    else:
                        raise Exception("No visible")
            except:
                # Método B: Buscar por aria-label
                try:
                    poll_option = driver.find_element(By.CSS_SELECTOR, 'div[aria-label*="Encuesta" i], div[aria-label*="Poll" i]')
                    poll_option.click()
                    print("✅ Encuesta encontrada por aria-label")
                except:
                    # Método C: Buscar en todos los divs
                    try:
                        divs = driver.find_elements(By.CSS_SELECTOR, "div")
                        for div in divs:
                            try:
                                if div.is_displayed() and ("encuesta" in div.text.lower() or "poll" in div.text.lower()):
                                    div.click()
                                    print("✅ Encuesta encontrada en div")
                                    break
                            except:
                                continue
                    except:
                        print("❌ No se encontró opción de encuesta")
                        raise Exception("Encuesta no disponible")
            
            time.sleep(3)
            
            # 3. Escribir la pregunta
            print("Escribiendo pregunta...")
            
            # Buscar todos los campos editables
            campos_editables = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
            )
            
            if len(campos_editables) > 0:
                # Primer campo es la pregunta
                campos_editables[0].click()
                time.sleep(0.5)
                
                # Escribir pregunta
                for caracter in encuesta["pregunta"]:
                    pyperclip.copy(caracter)
                    campos_editables[0].send_keys(paste_key, 'v')
                    time.sleep(random.uniform(0.03, 0.1))
                
                time.sleep(1)
                
                # 4. Escribir primera opción
                if len(campos_editables) > 1:
                    campos_editables[1].click()
                    time.sleep(0.5)
                    
                    for caracter in encuesta["opciones"][0]:
                        pyperclip.copy(caracter)
                        campos_editables[1].send_keys(paste_key, 'v')
                        time.sleep(random.uniform(0.03, 0.1))
                    
                    time.sleep(1)
                    
                    # 5. Añadir y escribir segunda opción - CORRECCIÓN
                    print("Añadiendo segunda opción...")
                    try:
                        # IMPORTANTE: Esperar a que el botón esté disponible
                        time.sleep(1)
                        
                        # Buscar botón "Añadir opción" o "Add option"
                        add_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Añadir') or contains(text(), 'Add') or contains(text(), 'añadir')]")
                        
                        if add_buttons:
                            for btn in add_buttons:
                                try:
                                    # Verificar que esté visible y sea clickeable
                                    if btn.is_displayed() and btn.is_enabled():
                                        print(f"   Botón encontrado: {btn.text}")
                                        btn.click()
                                        print("✅ Segunda opción añadida")
                                        time.sleep(2)  # Esperar a que aparezca nuevo campo
                                        break
                                except:
                                    continue
                        
                        # Si no se encuentra, intentar método alternativo
                        if not add_buttons:
                            # Buscar por tipo de botón específico
                            try:
                                add_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="añadir" i], button[aria-label*="add" i]')
                                add_btn.click()
                                print("✅ Segunda opción añadida (aria-label)")
                                time.sleep(2)
                            except:
                                # Intentar con JavaScript
                                driver.execute_script("""
                                    var buttons = document.querySelectorAll('button, div[role="button"]');
                                    for(var i=0; i<buttons.length; i++) {
                                        var text = buttons[i].textContent || buttons[i].innerText;
                                        if(text && (text.includes('Añadir') || text.includes('Add'))) {
                                            buttons[i].click();
                                            break;
                                        }
                                    }
                                """)
                                print("✅ Segunda opción añadida (JavaScript)")
                                time.sleep(2)
                                
                    except Exception as e:
                        print(f"⚠️  Error añadiendo opción: {e}")
                        # Intentar continuar de todos modos
                    
                    # 6. Escribir segunda opción - CORRECCIÓN
                    print("Escribiendo segunda opción...")
                    time.sleep(1)
                    
                    # Volver a buscar campos después de añadir
                    try:
                        campos_editables = driver.find_elements(By.CSS_SELECTOR, 'div[contenteditable="true"]')
                        print(f"   Campos disponibles: {len(campos_editables)}")
                        
                        if len(campos_editables) > 2:
                            # El tercer campo debería ser la segunda opción
                            campos_editables[2].click()
                            time.sleep(0.5)
                            
                            # Limpiar campo por si tiene texto predeterminado
                            campos_editables[2].send_keys(Keys.COMMAND + "a" if platform.system() == "Darwin" else Keys.CONTROL + "a")
                            campos_editables[2].send_keys(Keys.DELETE)
                            time.sleep(0.5)
                            
                            for caracter in encuesta["opciones"][1]:
                                pyperclip.copy(caracter)
                                campos_editables[2].send_keys(paste_key, 'v')
                                time.sleep(random.uniform(0.03, 0.1))
                            
                            print("✅ Segunda opción escrita")
                        elif len(campos_editables) == 2:
                            # Si solo hay 2 campos, usar el segundo para la segunda opción
                            campos_editables[1].click()
                            time.sleep(0.5)
                            
                            # Escribir " / " para separar opciones
                            campos_editables[1].send_keys(" / ")
                            
                            for caracter in encuesta["opciones"][1]:
                                pyperclip.copy(caracter)
                                campos_editables[1].send_keys(paste_key, 'v')
                                time.sleep(random.uniform(0.03, 0.1))
                            
                            print("✅ Opciones combinadas en un campo")
                    except Exception as e:
                        print(f"⚠️  Error escribiendo segunda opción: {e}")
                
                time.sleep(1)
                
                # 7. Enviar encuesta - CLICK DIRECTO AL BOTÓN ESPECÍFICO
                print("Enviando encuesta...")
                encuesta_enviada = False
                
                # MÉTODO PRINCIPAL: Usar el selector EXACTO del botón "Enviar"
                try:
                    # Selector 1: Botón con aria-label="Enviar" Y el icono específico dentro
                    send_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Enviar" and .//span[@data-icon="wds-ic-send-filled"]]'))
                    )
                    driver.execute_script("arguments[0].click();", send_button)  # Click con JavaScript (más confiable)
                    print("✅ ENCUESTA ENVIADA (clic en botón específico)")
                    encuesta_enviada = True
                    time.sleep(3)  # Esperar a que la UI se actualice
                    
                except Exception as e1:
                    print(f"   ❌ Intento 1 falló: {e1}")
                    
                    # MÉTODO ALTERNATIVO: Buscar solo por el icono único
                    try:
                        send_icon = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-icon="wds-ic-send-filled"]'))
                        )
                        # Subir hasta el botón padre que se puede clickear
                        send_button = driver.execute_script("""
                            var icon = arguments[0];
                            return icon.closest('div[role="button"]');
                        """, send_icon)
                        if send_button:
                            send_button.click()
                            print("✅ ENCUESTA ENVIADA (vía icono)")
                            encuesta_enviada = True
                            time.sleep(3)
                    except Exception as e2:
                        print(f"   ❌ Intento 2 falló: {e2}")
                
                if encuesta_enviada:
                    print("✅ Encuesta enviada correctamente")
                    # VERIFICACIÓN: Esperar a que desaparezca la ventana de encuesta
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.invisibility_of_element_located((By.XPATH, '//div[@aria-label="Enviar" and .//span[@data-icon="wds-ic-send-filled"]]'))
                        )
                        print("✅ Ventana de encuesta cerrada confirmada")
                    except:
                        print("⚠️  La ventana de encuesta podría no haberse cerrado")
                else:
                    print("❌ ERROR CRÍTICO: No se pudo enviar la encuesta")
                    # Opcional: Tomar captura de pantalla para debug
                    # driver.save_screenshot("error_encuesta_no_enviada.png")
            
        except Exception as e:
            print(f"No se pudo completar el proceso de encuesta: {e}")
            # Continuar aunque falle la encuesta
        # --- Espera aleatoria ---
        wait_time = random.uniform(25, 40)
        print(f"Esperando {wait_time:.2f} segundos antes del siguiente contacto...")
        time.sleep(wait_time)

    except Exception as e:
        print(f"Ocurrió un error con el contacto {numero_telefono}: {e}")
        print("Saltando al siguiente contacto...")

print("Todos los mensajes y encuestas han sido procesados.")
time.sleep(3)
driver.quit()