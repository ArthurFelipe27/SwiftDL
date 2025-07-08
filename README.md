# SwiftDL

SwiftDL é um downloader de playlists do YouTube com interface gráfica simples e rápida, que permite baixar áudio (MP3), vídeo (MP4) ou ambos juntos.

---

## Funcionalidades

- Baixa playlists completas do YouTube.
- Permite escolher entre baixar só áudio em alta qualidade (320 kbps MP3), só vídeo (720p MP4) ou vídeo completo com áudio (MP4).
- Barra de progresso e status para acompanhar os downloads.
- Configuração opcional do caminho do FFmpeg para processamento.

---

## Requisitos

- Python 3.11+
- FFmpeg instalado (opcional, mas recomendado para melhor desempenho)
- Bibliotecas Python:
  - `yt-dlp`
  - `tkinter` (geralmente já vem com Python)
  - `ttkbootstrap` (opcional, para tema estilizado)

---

## Como usar

1. Execute o arquivo `SwiftDL.exe` (se estiver usando a versão empacotada).

2. Insira o link da playlist do YouTube no campo **Link da Playlist**.

3. Selecione a pasta de destino onde os arquivos serão salvos.

4. (Opcional) Informe o caminho para a pasta do FFmpeg, caso instalado.

5. Escolha o formato desejado: áudio (MP3), vídeo (MP4) ou completo.

6. Clique em **Baixar Playlist** para iniciar o download.

---

## Instruções para desenvolvedores

Caso queira rodar o projeto via código-fonte:

1. Instale as dependências:

```bash
pip install yt-dlp ttkbootstrap

Observações

    O FFmpeg é utilizado para converter e mesclar áudio e vídeo.

    Caso o FFmpeg não esteja configurado, o programa ainda funciona, mas pode perder algumas funcionalidades.

    A velocidade e sucesso do download dependem da qualidade da internet e das políticas do YouTube.

Licença

MIT License — sinta-se à vontade para usar e modificar.
Contato

Arthur Matos — [arthurfelipedasilvamatosdev@gmail.com]