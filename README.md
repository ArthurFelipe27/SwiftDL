# SwiftDL - Download de Mídia Simples

O SwiftDL é uma aplicação desktop intuitiva e eficiente para baixar vídeos e áudios de diversas plataformas online, como YouTube, TikTok, Instagram, Facebook, Pinterest e muitas outras suportadas pela poderosa biblioteca `yt-dlp`. Com uma interface amigável, ele simplifica o processo de salvar seu conteúdo favorito diretamente no seu computador.

## Funcionalidades Principais

* **Download de Vídeos:** Baixe vídeos em formato MP4, mantendo a melhor qualidade disponível.
* **Extração de Áudio:** Converta vídeos para áudio MP3 de alta qualidade.
* **Download Apenas de Vídeo:** Baixe o stream de vídeo em MP4 (sem áudio), ideal para projetos de edição.
* **Suporte a Múltiplas Plataformas:** Compatível com uma vasta gama de sites de vídeo/mídia.
* **Detecção Inteligente de Playlists:**
    * Identifica automaticamente se o link fornecido é de uma playlist.
    * **Pergunta ao Usuário:** Antes de iniciar o download, o aplicativo perguntará se você deseja baixar todos os itens da playlist ou apenas o vídeo/música individual.
* **Acesso a Conteúdo Restrito (com cookies):** Permite o uso de um arquivo de cookies para baixar conteúdo que requer autenticação.
* **Organização de Downloads:**
    * **Seleção de Diretório:** Escolha facilmente a pasta onde deseja salvar seus arquivos.
    * **Criação de Pasta Única:** Salve todos os itens de um download (seja um vídeo único ou uma playlist) em uma pasta dedicada e organizada.
    * **Nomenclatura Flexível:** Nomeie a pasta de download ou deixe que o app gere um nome padrão com data e hora. Se a criação de pasta for desmarcada, o nome fornecido servirá como um **prefixo** para o nome do arquivo.
* **Interface Clara:** Acompanhe o progresso em tempo real e cancele downloads a qualquer momento.

## Como Utilizar (Passo a Passo)

1.  **Obtenha o Link:** Copie a URL do vídeo ou playlist que deseja baixar.

2.  **Abra o SwiftDL:** Execute o aplicativo.

3.  **Cole o Link:** Clique em **"Colar"**. O SwiftDL analisará o link para obter o título.

4.  **Decida sobre Playlists (se detectada):** Uma caixa de diálogo perguntará se você deseja baixar a playlist inteira.
    * Clique em **"Sim"** para todos os itens.
    * Clique em **"Não"** para baixar apenas o primeiro.

5.  **Selecione o Local para Salvar:** Clique em **"Procurar"** e escolha uma pasta.

6.  **Configure a Saída (Opcional):**
    * **Para agrupar em uma pasta:** Deixe a caixa **"Criar pasta de download automaticamente"** marcada. Você pode digitar um nome no campo "Nome da Pasta (opcional)" ou deixar em branco para um nome padrão (Ex: `SwiftDL_Downloads_2025-10-02...`).
    * **Para salvar com um prefixo:** Desmarque a caixa e digite um nome no campo "Nome da Pasta (opcional)". O texto será adicionado ao início do nome do arquivo (Ex: `MeuPrefixo_NomeDoVideo.mp4`).

7.  **Escolha o Formato de Download:** Selecione uma das três opções:
    * **Vídeo Completo (MP4):** (Padrão) Baixa o vídeo com áudio na melhor qualidade MP4.
    * **Apenas Áudio (MP3):** Extrai e salva apenas o áudio em formato MP3.
    * **Apenas Vídeo (MP4):** Baixa o vídeo sem a faixa de áudio.

8.  **Forneça Cookies (Opcional):** Para vídeos privados ou que exigem login, use o botão "Procurar" para selecionar seu arquivo de cookies (`.txt`).

9.  **Iniciar o Download:** Clique em **"Baixar"**.

10. **Cancelar:** A qualquer momento, clique em **"Cancelar"** para interromper o processo.

## Requisitos Importantes

Para que o SwiftDL funcione corretamente, o **FFmpeg** é essencial.

* **Verificação Automática:** O SwiftDL verificará se o FFmpeg está instalado ao ser iniciado. Se não o encontrar, exibirá um aviso e não será aberto.
* **Instalação:**
    * Você precisa ter o **FFmpeg** instalado no seu sistema e configurado no `PATH` do ambiente. Baixe-o em [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
    * **Alternativa Simples:** Coloque os executáveis `ffmpeg.exe` e `ffprobe.exe` (no Windows) diretamente na mesma pasta onde o executável `SwiftDL.exe` está localizado.

## Solução de Problemas Comuns

* **"Erro ao baixar: Private video"**: O vídeo é privado. Use a opção de arquivo de cookies se sua conta tiver acesso.
* **"Nenhum formato de vídeo/áudio compatível encontrado"**: O vídeo pode ter sido removido ou estar restrito. Verifique o link.
* **Download travado ou lento**: Verifique sua conexão com a internet. Vídeos muito longos ou playlists grandes levam mais tempo.

## Licença

Este projeto está licenciado sob a Licença MIT.