import customtkinter as ctk
import threading
import json
import sys
import os
from datetime import datetime
from voz import AssistenteVoz
from comandos import ComandosHandler

class AssistenteUI:
    def __init__(self):
        self.config = self.carregar_config()
        self.assistente_voz = AssistenteVoz(self.config["nome_assistente"])
        self.comandos_handler = ComandosHandler(self.assistente_voz)
        
        self.setup_interface()
    
    def carregar_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️ Config.json não encontrado, criando padrão...")
            config_padrao = {"nome_assistente": "Ashiley"}
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config_padrao, f, indent=4)
            return config_padrao
    
    def setup_interface(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.app = ctk.CTk()
        self.app.title(f"Assistente {self.config['nome_assistente']}")
        
        # Dimensões
        width, height = 500, 600
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x = screen_width - width - 20
        y = screen_height - height - 50
        
        self.app.geometry(f"{width}x{height}+{x}+{y}")
        self.app.attributes("-topmost", True)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.app)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"🤖 Assistente {self.config['nome_assistente']}", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=10)
        
        # Ícone do microfone
        self.mic_icon = ctk.CTkLabel(
            self.main_frame, 
            text="🎤", 
            font=("Arial", 100)
        )
        self.mic_icon.pack(pady=20)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="✅ Pronto para ouvir", 
            font=("Arial", 16, "bold")
        )
        self.status_label.pack(pady=5)
        
        # Botão principal
        self.btn_ouvir = ctk.CTkButton(
            self.main_frame, 
            text="🎤 CLIQUE E FALE 🎤", 
            command=self.ouvir_comando,
            height=70,
            font=("Arial", 20, "bold"),
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        )
        self.btn_ouvir.pack(pady=30, padx=20, fill="x")
        
        # Área de log
        self.log_label = ctk.CTkLabel(
            self.main_frame, 
            text="📝 Histórico", 
            font=("Arial", 14, "bold")
        )
        self.log_label.pack(pady=(20,5))
        
        self.log_frame = ctk.CTkScrollableFrame(self.main_frame, height=150)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = ctk.CTkTextbox(self.log_frame, height=140, wrap="word")
        self.log_text.pack(fill="both", expand=True)
        
        # Configurar tags
        self.log_text.tag_config("erro", foreground="#ff6b6b")
        self.log_text.tag_config("sucesso", foreground="#69db7e")
        self.log_text.tag_config("info", foreground="#ffffff")
        
        # Botão limpar
        self.btn_limpar = ctk.CTkButton(
            self.main_frame, 
            text="🗑️ Limpar Histórico", 
            command=self.limpar_historico,
            height=35,
            font=("Arial", 12),
            fg_color="#555555",
            hover_color="#333333"
        )
        self.btn_limpar.pack(pady=10)
        
        # Mensagem inicial
        self.app.after(500, self.boas_vindas)
        self.app.lift()
        self.app.focus_force()
    
    def boas_vindas(self):
        self.adicionar_log(f"Assistente {self.config['nome_assistente']} iniciado!", "sucesso")
        self.adicionar_log("Clique no botão verde e fale seu comando", "info")
        # Falar mensagem de boas-vindas
        threading.Thread(target=lambda: self.assistente_voz.falar(f"Olá, sou {self.config['nome_assistente']}. Clique no botão e fale seu comando"), daemon=True).start()
    
    def limpar_historico(self):
        self.log_text.delete("1.0", "end")
        self.adicionar_log("Histórico limpo!", "info")
    
    def adicionar_log(self, texto, tipo="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.log_text.insert("end", f"[{timestamp}] ")
        
        if tipo == "erro":
            self.log_text.insert("end", f"❌ {texto}\n", "erro")
        elif tipo == "sucesso":
            self.log_text.insert("end", f"✅ {texto}\n", "sucesso")
        else:
            self.log_text.insert("end", f"📝 {texto}\n", "info")
        
        self.log_text.see("end")
    
    def animar_microfone(self, ativo=True):
        if ativo:
            self.mic_icon.configure(text="🎤🔴", text_color="red")
            self.status_label.configure(text="🎙️ OUVINDO... Fale agora!", text_color="yellow")
            self.btn_ouvir.configure(state="disabled", fg_color="#555555")
        else:
            self.mic_icon.configure(text="🎤", text_color="white")
            self.status_label.configure(text="✅ Pronto para ouvir", text_color="white")
            self.btn_ouvir.configure(state="normal", fg_color="#2E7D32")
    
    def ouvir_comando(self):
        def processar_audio():
            try:
                self.app.after(0, lambda: self.animar_microfone(True))
                
                self.adicionar_log("🎙️ Ouvindo...", "info")
                comando = self.assistente_voz.ouvir(timeout=5, uma_vez=True)
                
                self.app.after(0, lambda: self.animar_microfone(False))
                
                if comando and len(comando) > 0:
                    self.adicionar_log(f"🎯 Comando: '{comando}'", "sucesso")
                    
                    resposta = self.comandos_handler.executar(comando)
                    
                    if resposta:
                        self.adicionar_log(f"💬 Resposta: {resposta}", "sucesso")
                        # A fala já é feita dentro do comandos_handler
                    else:
                        self.adicionar_log("❌ Comando não reconhecido", "erro")
                        self.assistente_voz.falar("Desculpe, não entendi o comando.")
                else:
                    self.adicionar_log("⏰ Nenhum comando detectado", "erro")
                    self.assistente_voz.falar("Não entendi o que você disse.")
                    
            except Exception as e:
                self.app.after(0, lambda: self.animar_microfone(False))
                self.adicionar_log(f"❌ Erro: {str(e)}", "erro")
                print(f"Erro detalhado: {e}")
        
        threading.Thread(target=processar_audio, daemon=True).start()
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = AssistenteUI()
    app.run()