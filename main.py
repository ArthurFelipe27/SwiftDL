import webview
import threading
import os
import sys
from swiftdl_core import SwiftDLCore

class Api:
    def __init__(self):
        self._window = None
        self.core = SwiftDLCore()
        self.core.set_progress_callback(self.progress_bridge)

    def set_window(self, window):
        self._window = window

    def toggle_fullscreen(self):
        """Alterna o modo de tela cheia."""
        self._window.toggle_fullscreen()

    def select_folder(self):
        try:
            result = self._window.create_file_dialog(webview.FOLDER_DIALOG)
            if result and len(result) > 0:
                return result[0]
        except Exception as e:
            print(f"Erro ao selecionar pasta: {e}")
        return None

    def start_download(self, url, path, format_mode, folder_name="", create_subfolder=True):
        if not url or not path:
            return False

        audio_only = (format_mode == 'audio_only')
        video_only = (format_mode == 'video_only')

        thread = threading.Thread(
            target=self._run_download_thread,
            args=(url, path, folder_name, create_subfolder, audio_only, video_only)
        )
        thread.daemon = True 
        thread.start()
        return True

    def cancel_download(self):
        self.core.cancel_download()

    def _run_download_thread(self, url, path, folder_name, create_subfolder, audio_only, video_only):
        try:
            success = self.core.download(
                url=url, 
                base_download_path=path,
                folder_or_prefix_name=folder_name,
                create_subfolder=create_subfolder, 
                audio_only=audio_only, 
                video_only=video_only
            )
            
            if success:
                self._window.evaluate_js("onDownloadComplete(true)")
            else:
                self._window.evaluate_js("onDownloadComplete(false)")
                
        except Exception as e:
            print(f"Erro Crítico na Thread: {e}")
            safe_error = str(e).replace("'", "").replace('"', "") 
            self._window.evaluate_js(f"onDownloadError('{safe_error}')")

    def progress_bridge(self, percent, status):
        msg = "Iniciando..."
        if status == 'downloading':
            msg = f"{percent:.1f}%"
        elif status == 'finished':
            msg = "Processando arquivo..."
            percent = 100
        elif status == 'error':
            msg = "Erro"
        
        if self._window:
            self._window.evaluate_js(f"updateProgress({percent}, '{msg}', '{status}')")

def get_resource_path(relative_path):
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
        'SwiftDL', 
        url=html_path,
        js_api=api,
        width=850,
        height=680,
        resizable=True,
        min_size=(600, 500),
        background_color='#121212'
    )
    
    api.set_window(window)
    webview.start(debug=False, icon=icon_path)