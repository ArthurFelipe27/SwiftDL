import os
import re
from datetime import datetime

class SwiftDLCore:
    def __init__(self):
        # yt_dlp é pesado. Importamos dentro das funções (Lazy Load) para arranque rápido.
        self.ydl_opts = {
            'format': 'best',
            'outtmpl': '',
            'noplaylist': True,
            'progress_hooks': [self._progress_hook],
            'postprocessors': [],
            'verbose': False,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': True, # Ignora erros de vídeos individuais numa playlist
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        self.download_canceled = False
        self.progress_callback = None

    def _progress_hook(self, d):
        import yt_dlp

        if self.download_canceled:
            raise yt_dlp.utils.DownloadError("Transferência cancelada pelo utilizador.")

        if d['status'] == 'downloading':
            if self.progress_callback:
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')

                if total_bytes > 0:
                    percent = (downloaded_bytes / total_bytes) * 100
                    self.progress_callback(percent, 'downloading', speed, eta)
                else:
                    self.progress_callback(0, 'starting', speed, eta)
                    
        elif d['status'] == 'finished':
            if self.progress_callback:
                self.progress_callback(100, 'finished', '', '')
                
        elif d['status'] == 'error':
            if self.progress_callback:
                self.progress_callback(0, 'error', '', '')

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def _sanitize_folder_name(self, name):
        """Segurança: Limpa caracteres maliciosos para prevenir Path Traversal."""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    def download(self, url, base_download_path, folder_or_prefix_name="", create_subfolder=True, audio_only=False, video_only=False, allow_playlist=False, cookie_file_path=None):
        import yt_dlp # Lazy load efetuado apenas quando se clica em "Baixar"
        
        self.download_canceled = False
        final_output_dir = base_download_path
        output_filename_template = "%(title)s.%(ext)s"

        folder_or_prefix_name = self._sanitize_folder_name(folder_or_prefix_name)

        # Lógica de pastas segura
        if create_subfolder:
            if folder_or_prefix_name:
                final_output_dir = os.path.join(base_download_path, folder_or_prefix_name)
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                final_output_dir = os.path.join(base_download_path, f"SwiftDL_{timestamp}")
            
            output_filename_template = os.path.join(final_output_dir, "%(title)s.%(ext)s")
        else:
            if folder_or_prefix_name:
                output_filename_template = os.path.join(final_output_dir, f"{folder_or_prefix_name}_%(title)s.%(ext)s")
            else:
                output_filename_template = os.path.join(final_output_dir, "%(title)s.%(ext)s")

        # Se permitir playlist, inclui o número da track se for uma lista
        if allow_playlist:
            self.ydl_opts['noplaylist'] = False
            output_filename_template = os.path.join(final_output_dir, "%(playlist_index)s_%(title)s.%(ext)s")
        else:
            self.ydl_opts['noplaylist'] = True

        # Cria diretório se não existir
        if not os.path.exists(final_output_dir):
            try:
                os.makedirs(final_output_dir)
            except OSError as e:
                raise OSError(f"Falha ao criar o diretório: {e}")

        self.ydl_opts['outtmpl'] = output_filename_template
        self.ydl_opts['postprocessors'] = []

        if audio_only:
            self.ydl_opts['format'] = 'bestaudio/best'
            self.ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
        elif video_only:
            self.ydl_opts['format'] = 'bestvideo[ext=mp4]/bestvideo'
        else:
            self.ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            self.ydl_opts['postprocessors'].append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            })

        # Autenticação por Cookies
        if cookie_file_path and os.path.exists(cookie_file_path):
            self.ydl_opts['cookiefile'] = cookie_file_path
        else:
            self.ydl_opts.pop('cookiefile', None)

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            return True
        except yt_dlp.utils.DownloadError as e:
            if "cancelled" in str(e).lower() or self.download_canceled:
                print("Download cancelado.")
                return False
            print(f"Erro no yt-dlp: {e}")
            raise e
        except Exception as e:
            print(f"Erro crítico no download: {e}")
            raise e
        finally:
            self.download_canceled = False
            self.ydl_opts['outtmpl'] = ""

    def cancel_download(self):
        self.download_canceled = True