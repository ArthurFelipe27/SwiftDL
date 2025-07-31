# 🚀 SwiftDL – Baixe Vídeos e Músicas com Facilidade!

🎵 **SwiftDL** é um aplicativo **desktop** simples, rápido e eficiente para baixar **vídeos** e **áudios** das plataformas mais populares:  
**YouTube**, **TikTok**, **Instagram**, **Facebook**, **Pinterest** e MUITO mais – tudo com a poderosa biblioteca [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

💡 Com uma interface amigável e prática, o SwiftDL torna o processo de salvar seus conteúdos favoritos no computador **rápido e organizado**.

---

## ✨ Funcionalidades Principais

- ✅ **Baixe Vídeos (MP4)** na melhor qualidade
- ✅ **Converta para Áudio (MP3)** com alta fidelidade
- ✅ **Compatível com diversas plataformas** (YouTube, TikTok, Instagram, Facebook, Pinterest, etc.)
- ✅ **Detecção de Playlist Automática** com opção de baixar tudo ou só um item
- ✅ **Suporte a Cookies** para vídeos privados ou com autenticação
- ✅ **Organização Automática:** crie pastas personalizadas ou nomeadas automaticamente
- ✅ **Barra de Progresso em Tempo Real** e status atual do download
- ✅ **Cancelamento instantâneo** do download em andamento

---

## 🧭 Como Usar o SwiftDL (Passo a Passo)

1. 🔗 **Copie o link** do vídeo ou playlist  
2. 💻 **Abra o SwiftDL** (executável está na pasta `/dist`)  
3. 📋 **Cole o link** na interface do app  
4. 📁 **Escolha a pasta** onde salvar os arquivos  
5. 🗂️ (Opcional) Dê um nome personalizado à pasta de download  
6. 🎚️ **Escolha o tipo de download:** apenas vídeo, apenas áudio, ou completo  
7. 🔐 (Opcional) Adicione um **arquivo de cookies** se o conteúdo for privado  
8. 📥 **Clique em "Baixar"** e acompanhe o progresso na barra  
9. ❌ **Clique em "Cancelar"** se quiser interromper o download

---

## 🛠️ Requisito Essencial – ⚠️ Instale o FFmpeg

Para conversões em **MP3** e **MP4**, o SwiftDL requer o [FFmpeg](https://ffmpeg.org/download.html) instalado.

### 📌 O que fazer:

1. Baixe o FFmpeg:
   🔗 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

2. **Configure o FFmpeg no PATH do sistema**:
   - Windows: adicione o caminho da pasta `bin` do FFmpeg às **Variáveis de Ambiente**
   - Ou, simplesmente coloque `ffmpeg.exe` e `ffprobe.exe` na mesma pasta que o `SwiftDL.exe`

3. Teste no terminal/cmd:
Se retornar a versão, está tudo certo ✅

---

## 📁 Estrutura do Repositório  
SwiftDL/  
├── build/SwiftDL/ # Arquivos de build temporários  
├── dist/ # ✅ Contém o executável final do app  
│ └── SwiftDL.exe  
├── .gitignore  
├── SwiftDL.spec # Configuração do PyInstaller  
├── favicon.ico # Ícone do aplicativo  
├── swiftdl_gui.py # Interface gráfica (GUI)  
└── swiftdl_core.py # Lógica de download e funcionalidades  


---

## 🧩 Solução de Problemas Comuns

| Problema | Solução |
|---------|---------|
| 🔒 **"Private video" ou "Sign in..."** | Exporte cookies do seu navegador e adicione no app |
| ❌ **"Nenhum formato de vídeo/áudio encontrado"** | Verifique se o vídeo está disponível publicamente |
| ⚠️ **Erro 'pyinstaller' não reconhecido** | Use o executável na pasta `/dist` — não é necessário rodar o código fonte |
| 🐢 **Download lento ou travado** | Verifique sua internet ou se é uma playlist grande |

---

## 📝 Licença

Este projeto está licenciado sob a **Licença MIT**.  
Você pode usar, modificar e distribuir como quiser!

---

## 🌟 Contribua e Apoie!

Se você gostou do SwiftDL, deixe uma ⭐ aqui no GitHub!  
Sugestões, melhorias e relatos de bugs são muito bem-vindos via [Issues](https://github.com/seuusuario/seurepo/issues).

---
