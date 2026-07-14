import io
import requests
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
import numpy as np
from deep_translator import GoogleTranslator

# ==========================================
# CONFIGURAÇÕES DA ELEVENLABS (Configure aqui as suas chaves)
# ==========================================
API_KEY_ELEVEN = "SUA_API_KEY_AQUI"
VOICE_ID_CLONADO = "SEU_VOICE_ID_AQUI"

# Configurações de áudio do microfone
SAMPLE_RATE = 16000
TAMANHO_BLOCO = int(SAMPLE_RATE * 0.1) 

# Inicializa as ferramentas locais
reconhecedor = sr.Recognizer()
tradutor = GoogleTranslator(source='pt', target='en')

def falar_com_voz_clonada_estavel(texto):
    """Gera o áudio em formato PCM de 24kHz (liberado em todos os planos) e reproduz sem cortes"""
    print(f"🔊 Gerando áudio via API (formato PCM compatível)...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID_CLONADO}"
    
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": API_KEY_ELEVEN
    }
    
    # Mudado para 'pcm_24000' para funcionar perfeitamente em planos sem restrição Pro
    TAXA_AMOSTRAGEM_SAIDA = 24000
    params = {
        "output_format": f"pcm_{TAXA_AMOSTRAGEM_SAIDA}"  
    }
    
    data = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    try:
        resposta = requests.post(url, json=data, headers=headers, params=params)
        
        if resposta.status_code != 200:
            print(f"❌ Erro na API ElevenLabs ({resposta.status_code}): {resposta.text}")
            return
            
        print("🗣️ Falando em Inglês com a sua voz customizada!")
        
        # Lê os dados brutos PCM recebidos (24kHz)
        dados_raw = np.frombuffer(resposta.content, dtype=np.int16)
        
        # Converte para float32 para o sounddevice reproduzir sem estalos
        dados_float = dados_raw.astype(np.float32) / 32768.0
        
        # Toca usando a frequência exata que pedimos à API (24000 Hz)
        sd.play(dados_float, TAXA_AMOSTRAGEM_SAIDA)
        sd.wait()  # Espera terminar de tocar completamente antes de liberar o microfone
            
    except Exception as e:
        print(f"❌ Erro ao falar na ElevenLabs: {e}")

def capturar_fala_inteligente():
    """Grava o áudio dinamicamente: começa quando você fala, para quando faz silêncio"""
    print("👂 Ouvindo... pode falar!")
    
    limiar_silencio = 0.005  
    silencio_maximo = 0.5   
    
    audio_acumulado = []
    falando = False
    segundos_de_silencio = 0.0
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
        while True:
            dados, _ = stream.read(TAMANHO_BLOCO)
            audio_acumulado.append(dados.copy())
            
            volume = np.linalg.norm(dados) / np.sqrt(len(dados))
            
            if volume > limiar_silencio:
                if not falando:
                    falando = True
                    print("🎤 Voz detectada... gravando...")
                segundos_de_silencio = 0.0
            elif falando:
                segundos_de_silencio += 0.1
                if segundos_de_silencio >= silencio_maximo:
                    print("⏱️ Fim de fala detectado.")
                    break
            else:
                if len(audio_acumulado) > 20:
                    audio_acumulado.pop(0)
                    
    audio_completo = np.concatenate(audio_acumulado, axis=0)
    audio_int16 = (audio_completo * 32767).astype(np.int16)
    return audio_int16

def executar_tradutor():
    print("\n🔥 TRADUTOR FUTURISTA ULTRA ESTÁVEL ATIVADO")
    print("🇧🇷 Fale em português e faça uma pausa natural.")
    print("👉 (Pressione Ctrl + C para parar)\n")
    
    while True:
        try:
            audio_bruto = capturar_fala_inteligente()
            print("🧠 Processando...")
            
            buffer_wav = io.BytesIO()
            sf.write(buffer_wav, audio_bruto, SAMPLE_RATE, format='WAV', subtype='PCM_16')
            buffer_wav.seek(0)
            
            with sr.AudioFile(buffer_wav) as fonte:
                dados_audio = reconhecedor.record(fonte)
                
                # Transcreve o áudio em português
                texto_portugues = reconhecedor.recognize_google(dados_audio, language="pt-BR")
                print(f"🇧🇷 Você: {texto_portugues}")
                
                # Traduz para o inglês
                texto_ingles = tradutor.translate(texto_portugues)
                print(f"🇺🇸 Tradução: {texto_ingles}")
                
                # Fala de forma limpa e completa
                falar_com_voz_clonada_estavel(texto_ingles)
                print("-" * 50)
                
        except sr.UnknownValueError:
            print("❓ Não entendi. Continue falando...\n")
        except sr.RequestError as e:
            print(f"❌ Erro de conexão com o reconhecimento de voz: {e}\n")
        except KeyboardInterrupt:
            print("\n🛑 Programa finalizado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Ocorreu um erro: {e}\n")

if __name__ == "__main__":
    try:
        executar_tradutor()
    except KeyboardInterrupt:
        print("\n🛑 Programa encerrado.")
