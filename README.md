# 🚀 SwiftDL - Downloader de Mídia Moderno

O SwiftDL é uma aplicação desktop com **interface moderna e intuitiva** para baixar vídeos e áudios de diversas plataformas, como **YouTube, TikTok, Instagram** e muitas outras.

Construído com uma arquitetura híbrida poderosa: Python no backend (para performance e downloads robustos com yt-dlp e ffmpeg) e Web Technologies (HTML5/CSS3/JS) no frontend (via pywebview) para uma experiência de usuário fluida e elegante.

🎨 Com um **design dark com detalhes em roxo** e ícones vetoriais, o SwiftDL torna o processo de salvar seu conteúdo favorito **rápido, prático e organizado**.

---

## ✨ Funcionalidades

- 🎭 Interface Moderna & Responsiva: Interface web nativa com Dark Mode, ícones SVG e animações suaves.
- 📺 Múltiplos Formatos:
  - Vídeo Completo (MP4): Melhor qualidade de vídeo e áudio combinados.
  - Apenas Áudio (MP3): Extração de áudio e conversão automática.
  - Apenas Vídeo (MP4): Stream de vídeo sem áudio (útil para editores).
- 🌐 Suporte Multiplataforma: Compatível com centenas de sites suportados pelo yt-dlp.
- 📁 Organização Automática: Criação automática de subpastas com data/hora ou nomes personalizados.
- 🚀 Performance: Downloads executados em threads separadas para não travar a interface.
- 🔒 Cookies: Suporte a arquivos de cookies para conteúdos restritos.

## 🛠️ Tecnologias Utilizadas

- Linguagem: Python 3.12+
- Core de Download: yt-dlp
- Processamento de Mídia: FFmpeg
- Interface (GUI): PyWebview (Ponte Python ↔ Navegador)
- Frontend: HTML5, CSS3, JavaScript (Vanilla)
  
---

## 🚀 Como Usar

1. Cole o Link: Copie o link do vídeo/música e cole no campo principal (ou use o botão de colar).

2. Escolha o Destino: Selecione a pasta onde o arquivo será salvo.

3. Configure (Opcional):
  - Defina um nome para a subpasta.
  - Escolha se quer criar uma subpasta automaticamente.

4. Selecione o Formato: Vídeo (MP4), Áudio (MP3) ou Só Vídeo.
5. Baixar: Clique no botão "Baixar Agora" e acompanhe o progresso na barra animada.

## 📸 Imagens
<img width="1909" height="829" alt="Captura de tela 2025-12-20 144824" src="https://github.com/user-attachments/assets/8717cafa-f13d-4e05-af07-384f2121bbcc" />

## ⚙️ Instalação e Execução (Desenvolvimento)

Para rodar o projeto diretamente do código-fonte:

1. Pré-requisitos
- Python 3.10 ou superior instalado.
- FFmpeg (veja abaixo).

2. Configurar o FFmpeg
O SwiftDL precisa do FFmpeg para converter arquivos.
    1. Baixe a versão essentials ou full do site oficial do FFmpeg ou Gyan.dev.
    2. Extraia o arquivo e encontre ffmpeg.exe e ffprobe.exe na pasta bin.
    3. Coloque esses dois arquivos (.exe) na raiz do projeto (mesma pasta do main.pyw).

3. Instalar Dependências
Abra o terminal na pasta do projeto e execute:  
````pip install -r requirements.txt````


4. Executar  
````python main.pyw````  


*(Usar a extensão ``.pyw`` executa sem abrir a janela preta do terminal)*  

## 📦 Como Criar um Executável (.exe)

Para distribuir o SwiftDL como um aplicativo standalone para Windows:  
1. Instale o ``auto-py-to-exe``:  
````pip install auto-py-to-exe````


2. Abra a ferramenta:  
````auto-py-to-exe````  


3. Configurações:
- Script Location: main.pyw
- One Directory (Recomendado para performance)
- Window Based (Hide Console)
- Icon: Selecione web/favicon.ico
- Additional Files (Add Folder): Pasta web ➔ Destino web
- Additional Files (Add Files): ffmpeg.exe e ffprobe.exe ➔ Destino . (raiz)

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
1. Faça um Fork do projeto
2. Crie sua Feature Branch (``git checkout -b feature/MinhaFeature``)
3. Commit suas mudanças (``git commit -m 'Adiciona MinhaFeature'``)
4. Push para a Branch (``git push origin feature/MinhaFeature``)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.  
Desenvolvido com 💜 por **Arthur Felipe**  
