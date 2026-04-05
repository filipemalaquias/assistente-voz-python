# voz.py (versão alternativa com pyttsx3)
import queue
import sounddevice as sd
import json
import pyttsx3
import time
from vosk import Model, KaldiRecognizer
import os

class AssistenteVoz:
    def __init__(self, nome_assistente):
        self.nome_assistente = nome_assistente
        self.microfone_ok = True
        
        # Configurar engine de fala com driver específico
        try:
            # Tentar com driver SAPI5 no Windows
            self.engine = pyttsx3.init(driverName='sapi5')
            print("✅ pyttsx3 inicializado com SAPI5")
        except:
            try:
                # Fallback para driver padrão
                self.engine = pyttsx3.init()
                print("✅ pyttsx3 inicializado com driver padrão")
            except Exception as e:
                print(f"❌ Erro ao inicializar pyttsx3: {e}")
                self.engine = None
        
        if self.engine:
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 1.0)
            
            # Selecionar voz em português
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower() or 'maria' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    print(f"✅ Voz selecionada: {voice.name}")
                    break
        
        # Carregar modelo Vosk
        model_path = "model/vosk-model-small-pt-0.3"
        if not os.path.exists(model_path):
            print(f"⚠️ Modelo não encontrado em {model_path}")
            self.model = None
        else:
            self.model = Model(model_path)
            print("✅ Modelo de voz carregado")
        
        self.recognizer = None
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.verificar_microfone()
    
    def verificar_microfone(self):
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            if not input_devices:
                print("❌ Nenhum microfone encontrado!")
                self.microfone_ok = False
                return False
            print(f"✅ Microfone encontrado: {input_devices[0]['name']}")
            self.microfone_ok = True
            return True
        except Exception as e:
            print(f"❌ Erro ao verificar microfone: {e}")
            self.microfone_ok = False
            return False
    
    def falar(self, texto):
        print(f"🤖 {self.nome_assistente} FALANDO: {texto}")
        if self.engine:
            try:
                self.engine.say(texto)
                self.engine.runAndWait()
                print("✅ Fala concluída")
                return True
            except Exception as e:
                print(f"❌ Erro ao falar: {e}")
                return False
        else:
            print("⚠️ Engine de voz não disponível")
            return False
    
    def audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(bytes(indata))
    
    def ouvir(self, timeout=5, uma_vez=True):
        if not self.model:
            return None
        
        try:
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                except queue.Empty:
                    break
            
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=8000,
                device=None,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                start_time = time.time()
                textos_reconhecidos = []
                
                print("🎤 Escutando...")
                
                while (time.time() - start_time) < timeout:
                    try:
                        data = self.audio_queue.get(timeout=0.5)
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            texto = result.get("text", "")
                            if texto:
                                if uma_vez:
                                    return texto.lower()
                                textos_reconhecidos.append(texto)
                    except queue.Empty:
                        continue
                
                if textos_reconhecidos:
                    return textos_reconhecidos[-1].lower()
                return None
        except Exception as e:
            print(f"❌ Erro ao ouvir: {e}")
            return None
    
    def fechar(self):
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass