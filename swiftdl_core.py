import os
import yt_dlp
from datetime import datetime

class SwiftDLCore:
    def __init__(self):
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
            'ignoreerrors': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        }
        self.download_canceled = False
        self.progress_callback = None

    def _progress_hook(self, d):
        if self.download_canceled:
            raise yt_dlp.utils.DownloadError("User cancelled download.")

        if d['status'] == 'downloading':
            if self.progress_callback:
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                if total_bytes > 0:
                    percent = (downloaded_bytes / total_bytes) * 100
                    self.progress_callback(percent, 'downloading')
                else:
                    self.progress_callback(0, 'starting')
        elif d['status'] == 'finished':
            if self.progress_callback:
                self.progress_callback(100, 'finished')
        elif d['status'] == 'error':
            if self.progress_callback:
                self.progress_callback(0, 'error')

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def download(self, url, base_download_path, folder_or_prefix_name="", create_subfolder=True, audio_only=False, video_only=False, cookie_file_path=None):
        self.download_canceled = False
        final_output_dir = base_download_path
        output_filename_template = "%(title)s.%(ext)s"

        # Lógica de pastas
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

        # Cria diretório se não existir
        if not os.path.exists(final_output_dir):
            try:
                os.makedirs(final_output_dir)
            except OSError as e:
                print(f"Erro ao criar diretório: {e}")
                return False

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

        # Cookies
        if cookie_file_path and os.path.exists(cookie_file_path):
            self.ydl_opts['cookiefile'] = cookie_file_path
        else:
            self.ydl_opts.pop('cookiefile', None)

        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"Erro no download: {e}")
            return False
        finally:
            self.download_canceled = False
            self.ydl_opts['outtmpl'] = ""

    def cancel_download(self):
        self.download_canceled = True