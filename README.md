# SwiftDL - Download de Mídia Simples

O SwiftDL é uma aplicação desktop intuitiva e eficiente para baixar vídeos e áudios de diversas plataformas online, como YouTube, TikTok, Instagram, Facebook, Pinterest e muitas outras suportadas pela poderosa biblioteca `yt-dlp`. Com uma interface amigável, ele simplifica o processo de salvar seu conteúdo favorito diretamente no seu computador.

## Funcionalidades Principais

* **Download de Vídeos:** Baixe vídeos em formato MP4, mantendo a melhor qualidade disponível.
* **Download de Áudios:** Converta vídeos para áudio MP3 de alta qualidade.
* **Suporte a Múltiplas Plataformas:** Compatível com uma vasta gama de sites de vídeo/mídia (YouTube, TikTok, Instagram, Facebook, Pinterest, etc.).
* **Detecção Inteligente de Playlists:**
    * Identifica automaticamente se o link fornecido é de uma playlist.
    * **Pergunta ao Usuário:** Antes de iniciar o download, o aplicativo perguntará se você deseja baixar todos os itens da playlist ou apenas o vídeo/música individual.
* **Acesso a Vídeos Restritos/Privados (com cookies):** Permite o uso de um arquivo de cookies para baixar conteúdo que requer autenticação (ex: vídeos privados do YouTube para os quais sua conta tem acesso).
* **Organização de Downloads:**
    * **Seleção de Diretório:** Escolha facilmente a pasta onde deseja salvar seus arquivos.
    * **Criação de Pasta Única:** Com a opção "Criar pasta de download automaticamente" marcada, todos os itens baixados (seja um vídeo único ou uma playlist inteira) serão salvos em uma única pasta dedicada, mantendo seus downloads organizados em um só lugar. Você pode nomear esta pasta ou deixar o aplicativo gerar um nome padrão (Ex: `SwiftDL_Downloads_YYYY-MM-DD_HH-MM-SS`).
* **Barra de Progresso e Status:** Acompanhe o progresso do download em tempo real e visualize o status atual da operação.
* **Cancelamento de Download:** Interrompa qualquer download em andamento a qualquer momento, de forma responsiva.

## Como Utilizar (Passo a Passo)

1.  **Obtenha o Link:**
    * Abra o seu navegador e acesse o vídeo ou a playlist que você deseja baixar.
    * Copie a URL completa da barra de endereços do seu navegador.

2.  **Abra o SwiftDL:**
    * Execute o aplicativo SwiftDL.

3.  **Cole o Link:**
    * No campo "Link do Vídeo/Áudio:", clique no botão **"Colar"** para inserir o link copiado da sua área de transferência. Alternativamente, você pode colar o link manualmente (Ctrl+V ou Cmd+V).
    * Após colar o link, o SwiftDL iniciará uma breve análise para determinar o título do vídeo/playlist e se é uma playlist. Aguarde a mensagem "aguardando análise" ser substituída pelo título.

4.  **Decida sobre Playlists (se detectada):**
    * Se o link for de uma playlist, uma caixa de diálogo aparecerá perguntando: "Este link contém uma playlist com X itens. Deseja baixar todos?".
    * Clique em **"Sim"** para baixar todos os vídeos/músicas da playlist.
    * Clique em **"Não"** para baixar apenas o primeiro vídeo/música do link.

5.  **Selecione o Local para Salvar:**
    * No campo "Salvar em:", clique no botão **"Procurar"**.
    * Escolha a pasta no seu computador onde você deseja que os downloads sejam salvos e clique em "Selecionar Pasta".

6.  **Configure o Nome da Pasta de Saída (Opcional):**
    * Marque a caixa **"Criar pasta de download automaticamente"**.
    * **Se você quiser uma pasta com um nome específico** para agrupar seus downloads, digite o nome desejado no campo "Nome da Pasta (opcional):" (Ex: `Minhas_Musicas_Favoritas`). Todos os downloads desta sessão irão para essa única pasta.
    * **Se você deixar o campo "Nome da Pasta (opcional):" vazio**, o SwiftDL criará automaticamente uma pasta com um nome padrão (Ex: `SwiftDL_Downloads_2025-07-30_23-59-59`) dentro do diretório que você escolheu no passo 5.

7.  **Escolha o Tipo de Download:**
    * **Baixar apenas áudio (MP3):** Marque esta opção para obter somente a faixa de áudio em formato MP3.
    * **Baixar apenas vídeo (MP4):** Marque esta opção para baixar o vídeo em formato MP4 (geralmente sem áudio, dependendo da fonte).
    * **Nenhuma opção marcada:** Se nenhuma das duas opções acima for marcada, o SwiftDL baixará o vídeo completo (áudio e vídeo) no melhor formato MP4 disponível.
    * **Atenção:** Selecione apenas uma opção de download (áudio ou vídeo). Marcar ambas causará um aviso.

8.  **Forneça Cookies (Opcional - Para Vídeos Privados/Restritos):**
    * Se você estiver tentando baixar um vídeo privado ou de acesso restrito (para o qual você tem permissão via login), você pode precisar fornecer um arquivo de cookies.
    * **Como obter cookies:** Você pode usar extensões de navegador como "EditThisCookie" (para Chrome/Firefox) para exportar seus cookies em formato Netscape.
    * No campo "Arquivo de Cookies (opcional):", clique em **"Procurar"** e selecione o arquivo `.txt` de cookies exportado.

9.  **Iniciar o Download:**
    * Clique no botão **"Baixar"**.
    * A barra de progresso e o status abaixo dela indicarão o andamento do download.

10. **Cancelar o Download:**
    * A qualquer momento, você pode clicar no botão **"Cancelar"** para interromper o download em andamento.

## Requisitos Importantes

Para que o SwiftDL funcione corretamente, especialmente para download de áudio (MP3) e certas conversões de vídeo (MP4), o **FFmpeg** é essencial.

* **FFmpeg:**
    * Você precisa ter o **FFmpeg** instalado no seu sistema e configurado no `PATH` do ambiente.
    * Você pode baixar o FFmpeg na página oficial: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
    * Instruções detalhadas para adicionar o FFmpeg ao PATH podem ser encontradas em tutoriais online específicos para o seu sistema operacional (Windows, macOS, Linux).
    * Alternativamente, você pode colocar os executáveis `ffmpeg.exe` e `ffprobe.exe` (no Windows) diretamente na mesma pasta onde o executável `SwiftDL.exe` está localizado.

## Solução de Problemas Comuns

* **"Erro ao baixar: Private video" / "Private video. Sign in..."**:
    * Este erro ocorre quando o vídeo é privado ou de acesso restrito e sua conta (ou o navegador de onde você copiou o link) tem permissão para acessá-lo.
    * Solução: Exporte seus cookies de navegador e forneça o arquivo `.txt` no campo "Arquivo de Cookies (opcional)".
* **"Nenhum formato de vídeo/áudio compatível encontrado"**:
    * Pode indicar que o vídeo está restrito, foi removido, ou que o `yt-dlp` não consegue encontrar um formato para baixar (raro). Verifique se o vídeo está disponível e se o link está correto.
* **"O termo 'pyinstaller' não é reconhecido..."**:
    * Este erro ocorre se você estiver tentando executar o SwiftDL a partir do código-fonte e o PyInstaller não estiver corretamente instalado ou configurado no PATH do seu sistema/ambiente virtual. (Este erro não deve acontecer se você estiver usando o executável pronto).
* **Download travado ou muito lento**:
    * Verifique sua conexão com a internet.
    * Vídeos muito longos ou playlists grandes naturalmente levam mais tempo.
    * Se o cancelamento não responder imediatamente, aguarde alguns segundos. Em downloads muito grandes, pode levar um momento para o processo parar.

## Licença

Este projeto está licenciado sob a Licença MIT.

---