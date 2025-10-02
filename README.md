# SwiftDL - Downloader de Mídia Moderno e Eficiente

![Screenshot do SwiftDL](https://i.imgur.com/8fL7oYj.png)

O SwiftDL é uma aplicação desktop com interface moderna e intuitiva para baixar vídeos e áudios de diversas plataformas online, como YouTube, TikTok, Instagram e muitas outras suportadas pela poderosa biblioteca `yt-dlp`. Com um tema escuro agradável e ícones informativos, ele simplifica o processo de salvar seu conteúdo favorito diretamente no seu computador.

## Funcionalidades Principais

* **Interface Moderna:** Tema escuro com detalhes em roxo, desenhado para ser visualmente agradável e funcional.
* **Múltiplos Formatos de Download:**
    * **Vídeo Completo (MP4):** Baixe vídeos com áudio na melhor qualidade disponível.
    * **Apenas Áudio (MP3):** Extraia e converta o áudio de vídeos diretamente para o formato MP3.
    * **Apenas Vídeo (MP4):** Baixe o stream de vídeo sem áudio, ideal para edições.
* **Suporte a Múltiplas Plataformas:** Compatível com uma vasta gama de sites de vídeo/mídia.
* **Detecção Inteligente de Playlists:**
    * Identifica automaticamente se o link é de uma playlist.
    * Permite que o usuário escolha entre baixar a playlist inteira ou apenas o item individual.
* **Acesso a Conteúdo Restrito:** Use um arquivo de cookies para baixar vídeos privados ou que exigem login (desde que sua conta tenha acesso).
* **Organização Flexível de Arquivos:**
    * **Criação de Pastas:** Agrupe os downloads de uma sessão em uma pasta dedicada com nome personalizado ou gerado automaticamente.
    * **Prefixo de Arquivo:** Se preferir não criar uma pasta, o nome fornecido será usado como um prefixo no nome do arquivo salvo.
* **Feedback em Tempo Real:** Acompanhe o progresso com uma barra de status detalhada e cancele downloads a qualquer momento.
* **Verificação Automática de Dependências:** O aplicativo verifica se o `FFmpeg` está instalado antes de iniciar, informando o usuário caso a dependência esteja ausente.

## Como Utilizar

1.  **Cole o Link:** Copie a URL do vídeo/playlist e clique no botão **"Colar"**. O SwiftDL analisará o link e exibirá o título.

2.  **Decida sobre a Playlist:** Se uma playlist for detectada, o programa perguntará se você deseja baixar todos os itens. Escolha "Sim" ou "Não".

3.  **Escolha o Local:** Clique em **"Procurar"** para selecionar a pasta onde seus arquivos serão salvos.

4.  **Configure a Saída (Opcional):**
    * **Para agrupar em uma pasta:** Deixe a caixa **"Criar pasta de download automaticamente"** marcada. Digite um nome no campo "Nome da Pasta" ou deixe-o vazio para um nome padrão (`SwiftDL_Downloads_DATA_HORA`).
    * **Para salvar com um prefixo:** Desmarque a caixa e digite o texto desejado no campo "Nome da Pasta". O texto será adicionado ao início do nome do arquivo (ex: `MeuPrefixo_NomeDoVideo.mp4`).

5.  **Selecione o Formato:** Escolha uma das três opções de download:
    * `Vídeo Completo (MP4)`
    * `Apenas Áudio (MP3)`
    * `Apenas Vídeo (MP4)`

6.  **Use Cookies (se necessário):** Para conteúdo restrito, clique em "Procurar" e selecione seu arquivo de cookies `.txt`.

7.  **Baixar:** Clique no botão roxo **"Baixar"** para iniciar o processo.

## Requisitos Importantes

### FFmpeg
Para conversão de áudio (MP3) e vídeo (MP4), o **FFmpeg** é essencial.
* **Verificação Automática:** O SwiftDL irá notificá-lo ao iniciar se não conseguir encontrar o FFmpeg.
* **Instalação:**
    * Baixe o FFmpeg em: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
    * **Solução Simples:** Coloque os executáveis `ffmpeg.exe` e `ffprobe.exe` (no Windows) na mesma pasta do `SwiftDL.exe`.
    * **Solução Avançada:** Instale o FFmpeg e adicione sua pasta `bin` ao PATH do sistema.

### Dependências (para rodar do código-fonte)
Se você deseja executar o projeto a partir dos arquivos Python, instale as dependências com:
```bash
pip install -r requirements.txt

Compilando o Executável (.exe)
Para gerar o arquivo SwiftDL.exe a partir do código-fonte, use o PyInstaller com o seguinte comando. Ele garante que todos os ícones e dependências ocultas sejam incluídos corretamente:

# Certifique-se de que seu ambiente virtual (.venv) esteja ativo
pyinstaller --windowed --onefile --icon="favicon/favicon.ico" --add-data "favicon;favicon" --hidden-import="PIL" swiftdlo_gui.py

Licença
Este projeto está licenciado sob a Licença MIT.

