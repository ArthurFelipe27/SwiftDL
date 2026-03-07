# 🚀 SwiftDL – Downloader de Mídia Moderno

![GitHub repo size](https://img.shields.io/github/repo-size/ArthurFelipe27/swiftdl?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/ArthurFelipe27/swiftdl?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/ArthurFelipe27/swiftdl?style=for-the-badge)
![License](https://img.shields.io/github/license/ArthurFelipe27/swiftdl?style=for-the-badge)

> **SwiftDL** é uma aplicação desktop moderna para **download de vídeos e áudios** de diversas plataformas como **YouTube, TikTok, Instagram** e muitas outras. Construída com **Python no backend** e **tecnologias web no frontend**, oferece desempenho, organização e uma experiência visual elegante.

---

## ✨ Funcionalidades Principais

* 🎭 **Interface Moderna e Responsiva**  
  Interface web nativa com **Dark Mode**, ícones SVG e animações suaves.

* 📺 **Múltiplos Formatos de Download**
  * 🎬 Vídeo Completo (MP4) — Melhor qualidade de vídeo e áudio combinados
  * 🎵 Apenas Áudio (MP3) — Extração e conversão automática
  * 🎞️ Apenas Vídeo (MP4) — Stream de vídeo sem áudio

* 🌐 **Suporte Multiplataforma**  
  Compatível com centenas de sites suportados pelo **yt-dlp**.

* 📁 **Organização Automática**  
  Criação automática de subpastas por data/hora ou nomes personalizados.

* 🚀 **Alta Performance**  
  Downloads executados em **threads separadas**, mantendo a interface fluida.

* 🔒 **Suporte a Cookies**  
  Permite baixar conteúdos restritos utilizando arquivos de cookies.

---

## 💻 Pré-requisitos

Antes de iniciar, certifique-se de ter:

* 🐍 **Python 3.10 ou superior**
* 🎞️ **FFmpeg** instalado
* 💻 Sistema operacional **Windows, Linux ou macOS**

---

## 🚀 Tecnologias Utilizadas

### 🧩 Backend

* 🐍 **Python 3.12+**
* ⬇️ **yt-dlp** — Core de download
* 🎞️ **FFmpeg** — Processamento e conversão de mídia
* 🪟 **PyWebView** — Interface desktop e ponte Python ↔ JavaScript

### 🎨 Frontend

* 🧱 **HTML5**
* 💅 **CSS3**
* ⚡ **JavaScript (Vanilla)**

---

## ⚙️ Como Usar

1️⃣ **Cole o Link**  
Copie o link do vídeo ou música e cole no campo principal.

2️⃣ **Escolha o Destino**  
Selecione a pasta onde o arquivo será salvo.

3️⃣ **Configurações Opcionais**
* Defina um nome para a subpasta
* Ative a criação automática de pastas

4️⃣ **Selecione o Formato**  
Vídeo (MP4), Áudio (MP3) ou Apenas Vídeo.

5️⃣ **Baixar**  
Clique em **“Baixar Agora”** e acompanhe o progresso em tempo real.

---

## 🚀 Como Executar (Versão Desktop)

1. Faça o download da [Release mais recente](https://github.com/ArthurFelipe27/SwiftDL/releases/tag/v1.0.0).
2. Extraia o conteúdo para uma pasta.
3. Execute o arquivo `SwiftDL.exe`.
   * *O sistema já inclui o FFmpeg e as dependências necessárias para rodar no Windows.*
   * 
---

## ⚙️ Instalação e Execução (Desenvolvimento)

### 1️⃣ Pré-requisitos

* Python 3.10+
* FFmpeg

---

### 2️⃣ Configuração do FFmpeg

1. Baixe o FFmpeg (Essentials ou Full)
2. Extraia os arquivos
3. Copie `ffmpeg.exe` e `ffprobe.exe` da pasta `bin`
4. Cole ambos na raiz do projeto (mesma pasta do `main.pyw`)

---

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Execute a aplicação

```bash
python main.pyw
```

> ℹ️ O uso da extensão `.pyw` evita a abertura do terminal no Windows.

---

## 📦 Criando um Executável (.exe)

Para gerar um executável standalone no Windows:

### 1️⃣ Instale o auto-py-to-exe

```bash
pip install auto-py-to-exe
```

---

### 2️⃣ Abra a ferramenta

```bash
auto-py-to-exe
```

---

### 3️⃣ Configurações Recomendadas

* Script Location: `main.pyw`
* One Directory (recomendado)
* Window Based (Hide Console)
* Icon: `web/favicon.ico`
* Additional Files:
  * Pasta `web` ➜ destino `web`
  * Arquivos `ffmpeg.exe` e `ffprobe.exe` ➜ destino raiz (`.`)

---

## 📸 Demonstração

### Interface Principal
<img width="1909" height="829" alt="Interface Principal" src="https://github.com/user-attachments/assets/8717cafa-f13d-4e05-af07-384f2121bbcc" />

---

## 🤝 Contribuição

Contribuições são bem-vindas!

1. Faça um **Fork** do projeto  
2. Crie uma branch para sua feature  
   ```bash
   git checkout -b feature/MinhaFeature
   ```
3. Faça o commit  
   ```bash
   git commit -m "Adiciona MinhaFeature"
   ```
4. Faça o push  
   ```bash
   git push origin feature/MinhaFeature
   ```
5. Abra um **Pull Request**

---

## 🧑‍💻 Autor

**Arthur Felipe**  
🌐 GitHub: https://github.com/ArthurFelipe27  

---

## 📝 Licença

Este projeto está licenciado sob a **Licença MIT**.

---

💜 *Projeto desenvolvido para oferecer uma forma rápida, organizada e elegante de salvar conteúdos multimídia utilizando Python e tecnologias web.*
