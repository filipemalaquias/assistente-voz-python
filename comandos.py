import webbrowser
import os
import subprocess
import json
import platform
import datetime

class ComandosHandler:
    def __init__(self, assistente_voz):
        self.assistente_voz = assistente_voz
        self.carregar_comandos_personalizados()
    
    def carregar_comandos_personalizados(self):
        """Carrega comandos do arquivo instrucoes.json"""
        try:
            with open("instrucoes.json", "r", encoding="utf-8") as f:
                self.comandos_personalizados = json.load(f)
            print(f"✅ {len(self.comandos_personalizados)} comandos carregados")
        except FileNotFoundError:
            print("⚠️ instrucoes.json não encontrado")
            self.comandos_personalizados = {}
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao ler instrucoes.json: {e}")
            self.comandos_personalizados = {}
    
    def abrir_site(self, url):
        """Abre um site no navegador"""
        try:
            webbrowser.open(url)
            return f"Abrindo site"
        except Exception as e:
            print(f"Erro ao abrir site: {e}")
            return f"Erro ao abrir o site"
    
    def abrir_pasta(self, caminho):
        """Abre uma pasta no explorador do Windows"""
        try:
            sistema = platform.system()
            
            if sistema == "Windows":
                # Verificar se a pasta existe
                if os.path.exists(caminho):
                    os.startfile(caminho)
                    return f"Abrindo pasta"
                else:
                    # Tentar abrir a pasta do usuário atual
                    if "Users\\HP" in caminho:
                        # Substituir HP pelo nome do usuário atual
                        usuario_atual = os.environ.get('USERNAME', 'HP')
                        caminho_corrigido = caminho.replace("HP", usuario_atual)
                        if os.path.exists(caminho_corrigido):
                            os.startfile(caminho_corrigido)
                            return f"Abrindo pasta"
                    return f"Pasta não encontrada: {caminho}"
            elif sistema == "Darwin":  # macOS
                subprocess.run(["open", caminho])
                return f"Abrindo pasta"
            else:  # Linux
                subprocess.run(["xdg-open", caminho])
                return f"Abrindo pasta"
        except Exception as e:
            print(f"Erro ao abrir pasta: {e}")
            return f"Erro ao abrir a pasta"
    
    def abrir_programa(self, programa):
        """Abre um programa do Windows"""
        try:
            sistema = platform.system()
            
            if sistema == "Windows":
                # Para programas do sistema
                if programa.endswith('.exe'):
                    # Verificar se é caminho completo
                    if os.path.exists(programa):
                        os.startfile(programa)
                    else:
                        # Tentar executar pelo nome (procura no PATH)
                        subprocess.Popen(programa, shell=True)
                    return f"Abrindo programa"
                else:
                    # Executar comando
                    subprocess.Popen(programa, shell=True)
                    return f"Abrindo programa"
            else:
                subprocess.Popen([programa])
                return f"Abrindo programa"
        except Exception as e:
            print(f"Erro ao abrir programa: {e}")
            return f"Erro ao abrir o programa"
    
    def abrir_arquivo(self, caminho):
        """Abre um arquivo específico"""
        try:
            if os.path.exists(caminho):
                os.startfile(caminho)
                return f"Abrindo arquivo"
            else:
                return f"Arquivo não encontrado: {caminho}"
        except Exception as e:
            print(f"Erro ao abrir arquivo: {e}")
            return f"Erro ao abrir o arquivo"
    
    def mostrar_hora(self):
        """Mostra a hora atual falando"""
        agora = datetime.datetime.now()
        hora_texto = f"São {agora.hour} horas e {agora.minute} minutos"
        self.assistente_voz.falar(hora_texto)
        return hora_texto
    
    def mostrar_data(self):
        """Mostra a data atual falando"""
        agora = datetime.datetime.now()
        meses = {
            1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
            5: "maio", 6: "junho", 7: "julho", 8: "agosto",
            9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
        }
        data_texto = f"Hoje é {agora.day} de {meses[agora.month]} de {agora.year}"
        self.assistente_voz.falar(data_texto)
        return data_texto
    
    def executar(self, comando):
        """Executa o comando reconhecido"""
        comando = comando.lower().strip()
        print(f"🎯 Executando: {comando}")
        
        # Comandos nativos (sempre disponíveis)
        comandos_nativos = {
            'hora': self.mostrar_hora,
            'horas': self.mostrar_hora,
            'que horas são': self.mostrar_hora,
            'que horas': self.mostrar_hora,
            'horário': self.mostrar_hora,
            'data': self.mostrar_data,
            'que dia é hoje': self.mostrar_data,
            'dia de hoje': self.mostrar_data,
            'data de hoje': self.mostrar_data,
        }
        
        # Verificar comandos nativos
        for palavra_chave, funcao in comandos_nativos.items():
            if palavra_chave in comando:
                print(f"✅ Comando nativo: {palavra_chave}")
                return funcao()
        
        # Verificar comandos personalizados do JSON
        for comando_chave, acao in self.comandos_personalizados.items():
            if comando_chave in comando:
                print(f"✅ Comando personalizado: {comando_chave}")
                tipo_acao = acao.get("acao")
                valor = acao.get("valor")
                
                if tipo_acao == "abrir_site":
                    resultado = self.abrir_site(valor)
                    return resultado
                elif tipo_acao == "abrir_pasta":
                    resultado = self.abrir_pasta(valor)
                    return resultado
                elif tipo_acao == "abrir_programa":
                    resultado = self.abrir_programa(valor)
                    return resultado
                elif tipo_acao == "abrir_arquivo":
                    resultado = self.abrir_arquivo(valor)
                    return resultado
                else:
                    print(f"⚠️ Ação desconhecida: {tipo_acao}")
                    return None
        
        # Se nenhum comando for reconhecido
        print(f"❌ Comando não reconhecido: {comando}")
        return None