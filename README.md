# 🚀 SwiftDL - Downloader de Mídia Moderno e Eficiente  

O **SwiftDL** é uma aplicação desktop com **interface moderna, intuitiva e tema escuro elegante** para baixar vídeos e áudios de diversas plataformas online, como **YouTube, TikTok, Instagram** e muitas outras suportadas pela poderosa biblioteca [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).  

🎨 Com um **design dark com detalhes em roxo** e ícones informativos, o SwiftDL torna o processo de salvar seu conteúdo favorito **rápido, prático e organizado**.  

---

## ✨ Funcionalidades  

- 🎭 **Interface Moderna**: Tema escuro com detalhes roxos, visualmente agradável e funcional.  
- 📺 **Múltiplos Formatos de Download**:  
  - **Vídeo Completo (MP4):** melhor qualidade com áudio incluso.  
  - **Apenas Áudio (MP3):** extração e conversão direta.  
  - **Apenas Vídeo (MP4):** ideal para edições.  
- 🌐 **Suporte a Múltiplas Plataformas**: compatível com uma vasta lista de sites de mídia.  
- 📑 **Detecção Inteligente de Playlists**:  
  - Reconhecimento automático de links de playlists.  
  - Opção de baixar a lista inteira ou apenas um item.  
- 🔒 **Acesso a Conteúdo Restrito**: suporte a **cookies** para vídeos privados (desde que sua conta tenha acesso).  
- 📂 **Organização Flexível de Arquivos**:  
  - **Criação de pastas automáticas** ou personalizadas.  
  - **Prefixo no nome do arquivo** para evitar duplicação.  
- 📊 **Feedback em Tempo Real**: barra de progresso detalhada e opção de cancelar downloads.  
- 🛠 **Verificação Automática de Dependências**: alerta caso o **FFmpeg** não esteja instalado.  

---

## 🖥 Como Utilizar  

1. **Cole o Link** → copie a URL e clique em **"Colar"**. O título do vídeo/playlist será exibido.  
2. **Playlist?** → se detectada, escolha baixar tudo ou apenas o vídeo atual.  
3. **Escolha o Local** → clique em **"Procurar"** e selecione a pasta de destino.  
4. **Configuração de Saída (opcional)**:  
   - **Criar Pasta:** nome automático ou personalizado (`SwiftDL_Downloads_DATA_HORA`).  
   - **Prefixo no Nome:** use texto como prefixo no arquivo final.  
5. **Selecione o Formato** → `MP4 (vídeo)`, `MP3 (áudio)` ou `MP4 (somente vídeo)`.  
6. **Cookies (opcional)** → adicione arquivo `.txt` para conteúdos restritos.  
7. **Baixar** → clique no botão roxo **"Baixar"** e aguarde o download.  

---

## ⚙️ Requisitos  

### 📌 FFmpeg  
O **FFmpeg** é necessário para conversão de áudio e vídeo.  

- ✅ **Detecção Automática** → o SwiftDL avisa se não encontrar.  
- 🔽 **Instalação Rápida (Windows)**:  
  - Baixe em [ffmpeg.org/download](https://ffmpeg.org/download.html)  
  - Coloque `ffmpeg.exe` e `ffprobe.exe` na mesma pasta do `SwiftDL.exe`.  
- ⚡ **Instalação Avançada**: adicione a pasta `bin` do FFmpeg ao **PATH do sistema**.  

### 📌 Dependências (para rodar via código-fonte)  
Se for executar direto em Python:  
```bash
pip install -r requirements.txt  
````

### 📦 Compilando o Executável

Para gerar o SwiftDL.exe com PyInstaller:

# Ative seu ambiente virtual (.venv) antes
````
pyinstaller --windowed --onefile --icon="favicon/favicon.ico" --add-data "favicon;favicon" --hidden-import="PIL" swiftdlo_gui.py
````
### 📜 Licença

Este projeto está licenciado sob a MIT License.

✨ Feito com dedicação para tornar seus downloads mais simples, rápidos e organizados!


