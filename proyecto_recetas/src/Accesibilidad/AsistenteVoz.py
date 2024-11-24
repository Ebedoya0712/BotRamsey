from gtts import gTTS
import os
import pygame

def reproducir_audio(texto):
    archivo_audio = generar_mp3(texto)
    
    # Inicializar pygame para reproducir el audio
    pygame.mixer.init()
    pygame.mixer.music.load(archivo_audio)
    pygame.mixer.music.play()

    # Esperar a que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Cerrar pygame antes de eliminar el archivo
    pygame.mixer.quit()

    # Eliminar el archivo de audio
    if os.path.exists(archivo_audio):
        os.remove(archivo_audio)

def generar_mp3(texto):
    archivo_audio = "voz.mp3"
    
    # Generar archivo de audio usando gTTS
    tts = gTTS(text=texto, lang="es")
    tts.save(archivo_audio)
    return archivo_audio

