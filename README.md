# 🎙️ Tradutor de Voz em Tempo Real com Voz Clonada (ElevenLabs)

Um assistente de tradução de voz de latência ultra-baixa desenvolvido em Python. O sistema captura a fala em português dinamicamente via microfone, realiza a transcrição e tradução para o inglês e reproduz a resposta de forma estável utilizando síntese de voz customizada via API da ElevenLabs.

---

## ⚡ Diferenciais Técnicos & Otimizações (Portfólio)

Este projeto foi desenhado com foco em **performance, latência e portabilidade**, aplicando conceitos avançados de engenharia de software:

* **Bypass de SDK para Estabilidade:** Em vez de depender do SDK oficial da ElevenLabs (que apresenta instabilidades frequentes de serialização de dados em versões recentes do Python/Pydantic), foi implementada uma integração direta via requisições HTTP (`requests`) para os endpoints REST da API.
* **PCM Streaming de Alta Performance:** Para evitar o overhead e a latência de decodificação de formatos comprimidos (como MP3), o áudio é solicitado diretamente do servidor no formato PCM bruto (`pcm_24000`), economizando ciclos de CPU e reduzindo o tempo de resposta geral.
* **VAD Dinâmico (Voice Activity Detection):** Utiliza análises matemáticas com `numpy` (`np.linalg.norm`) sobre buffers de áudio contínuos para detectar o início e o fim da fala automaticamente, eliminando a necessidade de cliques de botões ("push-to-talk").
* **Sem Dependências do Sistema (Zero FFmpeg):** A reprodução do áudio é feita alimentando arrays do `numpy` diretamente no buffer do `sounddevice`, tornando o software 100% portátil para Windows, Linux e macOS sem requerer instalação de players de mídia externos ou codecs como o FFmpeg.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Speech-to-Text (STT):** SpeechRecognition (Google Web Speech API)
* **Translation:** Deep Translator (Google Translate API)
* **Text-to-Speech (TTS):** ElevenLabs API (Voz Clonada)
* **Audio I/O:** SoundDevice & SoundFile
* **Processamento de Sinais:** NumPy

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado na sua máquina.

### 1. Instale as dependências:
```bash
pip install -r requirements.txt# voice-translator-rt
