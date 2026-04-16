import webview
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from swiftdl_core import SwiftDLCore

class Api:
    def __init__(self):
        self._window = None
        self.core = SwiftDLCore()
        self.core.set_progress_callback(self.progress_bridge)
        # Limita downloads simultâneos para não sobrecarregar a rede/CPU
        self.executor = ThreadPoolExecutor(max_workers=3)

    def set_window(self, window):
        self._window = window

    def toggle_fullscreen(self):
        """Alterna o modo de ecrã inteiro."""
        if self._window:
            self._window.toggle_fullscreen()

    def select_folder(self):
        """Abre a caixa de diálogo para escolher o diretório."""
        try:
            result = self._window.create_file_dialog(webview.FOLDER_DIALOG)
            if result and len(result) > 0:
                return result[0]
        except Exception as e:
            print(f"Erro ao selecionar pasta: {e}")
        return None

    def start_download(self, url, path, format_mode, folder_name="", create_subfolder=True, allow_playlist=False):
        """Inicia o processo de transferência numa thread de background usando o executor."""
        if not url or not path:
            return False

        audio_only = (format_mode == 'audio_only')
        video_only = (format_mode == 'video_only')

        # Submete a tarefa para a pool de threads (não bloqueia a UI e controla concorrência)
        self.executor.submit(
            self._run_download_thread,
            url, path, folder_name, create_subfolder, audio_only, video_only, allow_playlist
        )
        return True

    def cancel_download(self):
        """Cancela a transferência em curso."""
        self.core.cancel_download()

    def _run_download_thread(self, url, path, folder_name, create_subfolder, audio_only, video_only, allow_playlist):
        """Método interno executado na thread de download."""
        try:
            success = self.core.download(
                url=url, 
                base_download_path=path,
                folder_or_prefix_name=folder_name,
                create_subfolder=create_subfolder, 
                audio_only=audio_only, 
                video_only=video_only,
                allow_playlist=allow_playlist
            )
            
            if self._window:
                if success:
                    self._window.evaluate_js("onDownloadComplete(true)")
                else:
                    self._window.evaluate_js("onDownloadComplete(false)")
                
        except Exception as e:
            print(f"Erro Crítico na Thread: {e}")
            safe_error = str(e).replace("'", "").replace('"', "").replace('\n', ' ')
            if self._window:
                self._window.evaluate_js(f"onDownloadError('{safe_error}')")

    def progress_bridge(self, percent, status, speed="N/A", eta="N/A"):
        """Ponte de comunicação para enviar o estado ao Frontend."""
        msg = "A iniciar..."
        if status == 'downloading':
            msg = f"{percent:.1f}%"
        elif status == 'finished':
            msg = "A processar ficheiro (FFmpeg)..."
            percent = 100
        elif status == 'error':
            msg = "Erro na transferência"
        
        if self._window:
            # Escapa as strings para evitar erros no JS
            speed = speed.replace("'", "\\'")
            eta = eta.replace("'", "\\'")
            self._window.evaluate_js(f"updateProgress({percent}, '{msg}', '{status}', '{speed}', '{eta}')")

def get_resource_path(relative_path):
    """Garante o caminho correto do recurso quer em dev quer em compilação (PyInstaller)."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    api = Api()
    
    html_path = get_resource_path(os.path.join('web', 'index.html'))
    icon_path = get_resource_path(os.path.join('web', 'favicon.ico'))
    
    window = webview.create_window(
        'SwiftDL - Universal Downloader', 
        url=html_path,
        js_api=api,
        width=900,
        height=720,
        resizable=True,
        min_size=(700, 600),
        background_color='#121212'
    )
    
    api.set_window(window)
    # webview inicia quase instantaneamente porque yt_dlp sofreu "lazy load"
    webview.start(debug=False, icon=icon_path)