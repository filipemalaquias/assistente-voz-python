# 🎤 Assistente de Voz em Python (ASHILEY)

🚀 Sobre o Projeto
Este é um assistente de voz offline que permite controlar seu computador através de comandos de voz. Com uma interface gráfica moderna e intuitiva, o assistente pode abrir sites, programas, pastas, arquivos e informar hora e data - tudo sem depender de serviços cloud.

Diferenciais
🔒 100% Offline - Não envia dados para a internet

🎯 Comandos Personalizáveis - Adicione novos comandos via JSON

🎨 Interface Moderna - Design escuro com CustomTkinter

🔊 Voz Natural - Reconhecimento de fala em português

⚡ Rápido e Leve - Baixo consumo de recursos


## 🚀 Funcionalidades
- Escuta contínua
- Interface gráfica com Tkinter
- Reconhecimento de voz em português

## Comandos Suportados
🌐 Abrir Sites (Google, YouTube, GitHub, etc.)

📁 Abrir Pastas (Downloads, Documentos, etc.)

🖥️ Abrir Programas (Bloco de Notas, Calculadora, Paint, etc.)

📄 Abrir Arquivos (qualquer arquivo no sistema)

⏰ Informar Hora e Data

🎯 Comandos Personalizados (adicione quantos quiser)


## Tecnologias Utilizadas
- Tecnologia	Versão	Finalidade
- Python	3.8+	Linguagem principal
- CustomTkinter	5.2.0	Interface gráfica moderna
- Vosk	0.3.45	Reconhecimento de voz offline
- SoundDevice	0.4.6	Captura de áudio do microfone
- pyttsx3	2.90	Síntese de voz (fallback)
- pywin32	306	API de voz do Windows


## 📦 Pré-requisitos
Python 3.8 ou superior

Microfone funcionando

Conexão com internet apenas para baixar o modelo de voz (uma vez)

Windows 10/11 (recomendado) ou Linux/macOS

## ▶️ Como executar

## 🔧 Instalação

## 1. Clone o repositório

git clone https://github.com/filipemalaquias/assistente-voz-python
cd assistente-voz-python

## 2. Crie um ambiente virtual (recomendado)
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

## 3. Instale as dependências
pip install customtkinter vosk sounddevice pyttsx3 pywin32

## 4. Baixe o modelo de voz Vosk
Faça o download do modelo para português brasileiro:

bash
# Windows (PowerShell)
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip" -OutFile "vosk-model-small-pt-0.3.zip"
Expand-Archive vosk-model-small-pt-0.3.zip -DestinationPath "model"
del vosk-model-small-pt-0.3.zip

# Linux/macOS
wget https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip vosk-model-small-pt-0.3.zip -d model
rm vosk-model-small-pt-0.3.zip

## ⚙️ Configuração
Arquivo config.json
Configure o nome do seu assistente:

json
{
    "nome_assistente": "Ashiley"
}


## Arquivo instrucoes.json

# Adicione seus comandos personalizados:

json
{
    "abrir google": {
        "acao": "abrir_site",
        "valor": "https://www.google.com"
    },
    "abrir downloads": {
        "acao": "abrir_pasta",
        "valor": "C:\\Users\\SeuUsuario\\Downloads"
    }
}


## 🤝 Contribuição
Contribuições são sempre bem-vindas!

Faça um Fork do projeto

Crie sua Feature Branch (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a Branch (git push origin feature/AmazingFeature)

Abra um Pull Request


## 📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## 📧 Contato
Dev Malaquias - @devmalaquias - filipemalaquias199@proton.me

