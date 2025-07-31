import os
import yt_dlp
from datetime import datetime # Importar datetime para nomes de pasta padronizados

class SwiftDLCore:
    def __init__(self):
        self.ydl_opts = {
            'format': 'best', # Começa como melhor qualidade, será ajustado
            'outtmpl': '', # Será definido dinamicamente
            'noplaylist': True,
            'progress_hooks': [self._progress_hook],
            'postprocessors': [],
            'verbose': False,
            'quiet': True,
            'no_warnings': True,
        }
        self.download_canceled = False
        self.progress_callback = None

    def _progress_hook(self, d):
        """
        Callback para monitorar o progresso do download do yt-dlp.
        Lança uma exceção para cancelar o download se a flag download_canceled for True.
        """
        if self.download_canceled:
            # Esta exceção é capturada no método download para sinalizar o cancelamento.
            raise yt_dlp.utils.DownloadError("User cancelled download.")

        if d['status'] == 'downloading':
            if self.progress_callback:
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                if total_bytes > 0:
                    percent = (downloaded_bytes / total_bytes) * 100
                    self.progress_callback(percent, 'downloading')
                else:
                    # Caso o total de bytes não seja conhecido, mostra progresso 0 ou um status inicial.
                    self.progress_callback(0, 'starting')
        elif d['status'] == 'finished':
            if self.progress_callback:
                self.progress_callback(100, 'finished')
        elif d['status'] == 'error':
            if self.progress_callback:
                self.progress_callback(0, 'error')


    def set_progress_callback(self, callback):
        """Define a função de callback para atualização de progresso na GUI."""
        self.progress_callback = callback

    def download(self, url, base_download_path, folder_or_prefix_name="", create_subfolder=True, audio_only=False, cookie_file_path=None):
        """
        Inicia o processo de download usando yt-dlp.
        Gerencia caminhos de saída, formatos e opções de pós-processamento.
        """
        # Garante que a flag de cancelamento esteja limpa para um novo download
        self.download_canceled = False

        final_output_dir = base_download_path # Diretório onde os arquivos serão salvos
        output_filename_template = "%(title)s.%(ext)s" # Template padrão do nome do arquivo

        if create_subfolder:
            if folder_or_prefix_name:
                # Se o usuário especificou um nome de pasta, usa-o
                final_output_dir = os.path.join(base_download_path, folder_or_prefix_name)
                # O nome do arquivo dentro desta pasta será apenas o título.ext
                output_filename_template = os.path.join(final_output_dir, "%(title)s.%(ext)s")
            else:
                # Se o usuário marcou "criar pasta automaticamente" mas não deu um nome,
                # cria uma pasta com nome padrão baseado na data/hora
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                default_folder_name = f"SwiftDL_Downloads_{timestamp}"
                final_output_dir = os.path.join(base_download_path, default_folder_name)
                # O nome do arquivo dentro desta pasta será apenas o título.ext
                output_filename_template = os.path.join(final_output_dir, "%(title)s.%(ext)s")
        else:
            # Se não for para criar subpasta, os arquivos vão diretamente para base_download_path
            # O folder_or_prefix_name, se existir, será usado como prefixo do nome do arquivo
            if folder_or_prefix_name:
                output_filename_template = os.path.join(final_output_dir, f"{folder_or_prefix_name}_%(title)s.%(ext)s")
            else:
                output_filename_template = os.path.join(final_output_dir, "%(title)s.%(ext)s")


        # Garante que o diretório de destino final exista antes de tentar o download
        if not os.path.exists(final_output_dir):
            try:
                os.makedirs(final_output_dir)
            except OSError as e:
                print(f"Erro ao criar o diretório: {e}")
                if self.progress_callback:
                    self.progress_callback(0, 'error')
                return False

        self.ydl_opts['outtmpl'] = output_filename_template
        self.ydl_opts['postprocessors'] = [] # Reseta post-processadores para cada download

        # Configurações para download de áudio ou vídeo
        if audio_only:
            self.ydl_opts['format'] = 'bestaudio/best'
            self.ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
        else:
            # Tenta pegar melhor vídeo mp4 + melhor áudio m4a, ou melhor mp4 geral, ou melhor formato disponível
            self.ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            # Garante que o arquivo final seja mp4 através de conversão se necessário
            self.ydl_opts['postprocessors'].append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            })

        # Adiciona o arquivo de cookies às opções do yt-dlp se um caminho válido for fornecido
        if cookie_file_path and os.path.exists(cookie_file_path):
            self.ydl_opts['cookiefile'] = cookie_file_path
        else:
            # Garante que a opção 'cookiefile' não esteja presente se o caminho for inválido/vazio
            self.ydl_opts.pop('cookiefile', None)

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # A lógica de playlist é controlada pela opção 'noplaylist' do ydl_opts.
                # Se 'noplaylist' for True, yt-dlp baixa apenas o primeiro item se for uma playlist.
                # Se 'noplaylist' for False, yt-dlp baixa a playlist completa.
                ydl.download([url])
            return True # Retorna True se o download foi bem-sucedido
        except yt_dlp.utils.DownloadError as e:
            # Captura a exceção de cancelamento ou outros erros de download
            if "User cancelled" in str(e):
                print("Download cancelled by user.")
                return False
            else:
                print(f"Erro ao baixar: {e}")
                if self.progress_callback:
                    self.progress_callback(0, 'error')
                return False
        except Exception as e:
            # Captura quaisquer outros erros inesperados
            print(f"Ocorreu um erro inesperado: {e}")
            if self.progress_callback:
                self.progress_callback(0, 'error')
            return False
        finally:
            # Garante que a flag de cancelamento seja resetada e o cookiefile removido após a operação
            self.download_canceled = False
            self.ydl_opts.pop('cookiefile', None) # Limpa a opção de cookiefile
            # Reset o outtmpl para evitar comportamentos inesperados em downloads subsequentes
            self.ydl_opts['outtmpl'] = ""

    def cancel_download(self):
        """Sinaliza para o processo de download ser cancelado."""
        self.download_canceled = True
        print("Download cancellation requested.")