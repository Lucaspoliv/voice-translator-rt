# 🎙️ Tradutor de Voz em Tempo Real (Voz Clonada)

Criei este script para rodar um tradutor de voz de latência super baixa. Você fala em português, o script detecta o fim da sua fala, traduz para o inglês e fala de volta usando uma voz clonada pela API da ElevenLabs.

Foquei em deixar o código o mais limpo, portátil e rápido possível, sem precisar instalar programas pesados no computador.

---

## 🛠️ Como resolvi os problemas técnicos (A parte legal)

Durante o desenvolvimento, precisei contornar alguns problemas clássicos de integração de áudio e APIs. Aqui está como resolvi cada um deles:

* **O SDK da ElevenLabs quebrou? Fui de requisição pura:** 
  A biblioteca oficial deles estava dando erro de compatibilidade de versão (conflito do Pydantic no Python). Em vez de perder tempo brigando com versões de pacotes, decidi consumir a API fazendo requisições HTTP diretas usando `requests`. Ficou mais leve, mais rápido e blindado contra atualizações chatas da biblioteca deles.
  
* **Chega de áudio cortando no final:** 
  Tentar reproduzir arquivos MP3 por streaming direto da memória costuma cortar o final das frases. Para resolver isso de forma definitiva, passei a solicitar o áudio no formato PCM bruto (`pcm_24000`) direto para a API. 
  
* **Zero dependências externas (Nada de FFmpeg):** 
  Geralmente, projetos de áudio em Python exigem que você instale o FFmpeg no sistema operacional (o que é chato de configurar no Windows). Como mudei a saída para PCM bruto, consigo ler os dados com o `numpy` e jogar direto no `sounddevice` sem precisar de nenhum conversor externo. Funciona direto ao clonar o repositório.

* **Detecção de voz automática:** 
  Usei matemática simples com `numpy` para monitorar o volume do microfone em blocos de tempo. O script sabe exatamente quando você começa e quando para de falar, eliminando a necessidade de apertar botões para gravar.

---

## 🚀 Como testar na sua máquina

### 1. Instale as dependências:
```bash
pip install -r requirements.txt

2. Configure suas chaves:
Abra o arquivo tradutor_pt_en.py e coloque sua API Key da ElevenLabs e o ID da sua voz clonada:

Python
API_KEY_ELEVEN = "SUA_API_KEY_AQUI"
VOICE_ID_CLONADO = "SEU_VOICE_ID_AQUI"
3. Execute:
Bash
python tradutor_pt_en.py
```bash
pip install -r requirements.txt# voice-translator-rt
