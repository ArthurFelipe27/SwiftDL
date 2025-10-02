import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import subprocess
import sys
from PIL import Image, ImageTk
import sv_ttk 
import yt_dlp
from swiftdl_core import SwiftDLCore

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_ffmpeg():
    """Verifica se o FFmpeg está acessível no PATH do sistema."""
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(
            ['ffmpeg', '-version'], 
            capture_output=True, 
            check=True, 
            startupinfo=startupinfo
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

class SwiftDLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SwiftDL - Download de Mídia")
        self.root.geometry("750x660")
        self.root.resizable(False, False)

        # --- APLICAÇÃO DO TEMA E CORES ---
        # Usamos o sv_ttk para dar uma base moderna e depois personalizamos com nossas cores
        sv_ttk.set_theme("dark")
        self.setup_styles()

        self.swiftdl_core = SwiftDLCore()
        self.swiftdl_core.set_progress_callback(self.update_progress)

        self.download_playlist = False
        self.video_title = ""
        self.download_thread = None

        self.load_icons()
        self.create_widgets()

    def setup_styles(self):
        """Configura o estilo personalizado para os widgets."""
        # --- NOSSA PALETA DE CORES ---
        self.COLOR_PRIMARY = "#5e17eb"  # O roxo principal que você pediu
        self.COLOR_LIGHT_ACCENT = "#8c52ff" # Cor clara dos ícones, para destaques
        self.COLOR_BACKGROUND = "#212121" # Fundo escuro para contraste
        self.COLOR_WIDGET_BACKGROUND = "#2c2c2c" # Fundo de caixas de texto e frames
        self.COLOR_TEXT = "#ffffff"       # Texto branco
        self.COLOR_TEXT_DISABLED = "#6e6e6e" # Texto para itens desabilitados

        style = ttk.Style()
        
        # Configuração global
        style.configure('.', 
            background=self.COLOR_BACKGROUND,
            foreground=self.COLOR_TEXT,
            font=('Arial', 10)
        )

        # Frames e Janela
        style.configure('TFrame', background=self.COLOR_BACKGROUND)
        self.root.configure(background=self.COLOR_BACKGROUND)

        # Labels e Labelframes
        style.configure('TLabel', background=self.COLOR_BACKGROUND, foreground=self.COLOR_TEXT)
        style.configure('TLabelframe', background=self.COLOR_BACKGROUND, bordercolor=self.COLOR_WIDGET_BACKGROUND)
        style.configure('TLabelframe.Label', background=self.COLOR_BACKGROUND, foreground=self.COLOR_LIGHT_ACCENT, font=('Arial', 10, 'bold'))
        
        # Botões
        style.configure('TButton', 
            background=self.COLOR_WIDGET_BACKGROUND, 
            foreground=self.COLOR_TEXT,
            bordercolor=self.COLOR_WIDGET_BACKGROUND,
            lightcolor=self.COLOR_WIDGET_BACKGROUND,
            darkcolor=self.COLOR_WIDGET_BACKGROUND,
            font=('Arial', 10, 'bold')
        )
        style.map('TButton',
            background=[('active', self.COLOR_LIGHT_ACCENT), ('disabled', self.COLOR_WIDGET_BACKGROUND)],
            foreground=[('disabled', self.COLOR_TEXT_DISABLED)]
        )
        # Botão de Destaque (Baixar)
        style.configure('Accent.TButton', 
            background=self.COLOR_PRIMARY, 
            foreground=self.COLOR_TEXT
        )
        style.map('Accent.TButton',
            background=[('active', self.COLOR_LIGHT_ACCENT)]
        )

        # Caixa de Texto (Entry)
        style.configure('TEntry', 
            fieldbackground=self.COLOR_WIDGET_BACKGROUND,
            foreground=self.COLOR_TEXT,
            bordercolor=self.COLOR_WIDGET_BACKGROUND,
            insertcolor=self.COLOR_TEXT # Cor do cursor de texto
        )
        
        # Barra de Progresso
        style.configure('Horizontal.TProgressbar', 
            troughcolor=self.COLOR_WIDGET_BACKGROUND, 
            background=self.COLOR_PRIMARY,
            bordercolor=self.COLOR_WIDGET_BACKGROUND
        )

        # Checkboxes e Radiobuttons
        style.configure('TCheckbutton', background=self.COLOR_BACKGROUND, foreground=self.COLOR_TEXT)
        style.configure('TRadiobutton', background=self.COLOR_BACKGROUND, foreground=self.COLOR_TEXT)
        style.map('TRadiobutton',
            indicatorcolor=[('selected', self.COLOR_PRIMARY), ('!selected', self.COLOR_WIDGET_BACKGROUND)]
        )
        style.map('TCheckbutton',
            indicatorcolor=[('selected', self.COLOR_PRIMARY), ('!selected', self.COLOR_WIDGET_BACKGROUND)]
        )


    def load_icons(self):
        """Carrega todos os ícones da aplicação."""
        try:
            self.root.iconbitmap(resource_path("favicon/favicon.ico"))
            self.paste_icon = ImageTk.PhotoImage(Image.open(resource_path("favicon/paste_icon.png")).resize((16, 16)))
            self.clear_icon = ImageTk.PhotoImage(Image.open(resource_path("favicon/clear_icon.png")).resize((16, 16)))
            self.browse_icon = ImageTk.PhotoImage(Image.open(resource_path("favicon/browse_icon.png")).resize((16, 16)))
            self.download_icon = ImageTk.PhotoImage(Image.open(resource_path("favicon/download_icon.png")).resize((16, 16)))
            self.cancel_icon = ImageTk.PhotoImage(Image.open(resource_path("favicon/cancel_icon.png")).resize((16, 16)))
        except Exception as e:
            print(f"Aviso: Não foi possível carregar os ícones. Erro: {e}")
            self.paste_icon, self.clear_icon, self.browse_icon, self.download_icon, self.cancel_icon = (None,)*5

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Labelframe(main_frame, text="Entrada e Destino", padding=15)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Link do Vídeo/Áudio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.link_entry = ttk.Entry(input_frame)
        self.link_entry.grid(row=0, column=1, columnspan=2, pady=5, sticky=tk.EW)
        
        button_frame_link = ttk.Frame(input_frame)
        button_frame_link.grid(row=0, column=3, pady=5, padx=(5,0))
        self.paste_button = ttk.Button(button_frame_link, text="Colar", image=self.paste_icon, compound=tk.LEFT, command=self.paste_clipboard)
        self.paste_button.pack(side=tk.LEFT, padx=(0, 5))
        self.clear_button = ttk.Button(button_frame_link, text="Limpar", image=self.clear_icon, compound=tk.LEFT, command=self.clear_link_entry)
        self.clear_button.pack(side=tk.LEFT)
        
        ttk.Label(input_frame, text="Título/Nome:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.title_label = ttk.Label(input_frame, text="(aguardando análise)")
        self.title_label.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=5)

        ttk.Label(input_frame, text="Salvar em:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.path_entry = ttk.Entry(input_frame)
        self.path_entry.grid(row=2, column=1, columnspan=2, pady=5, sticky=tk.EW)
        self.browse_button = ttk.Button(input_frame, text="Procurar", image=self.browse_icon, compound=tk.LEFT, command=self.browse_path)
        self.browse_button.grid(row=2, column=3, pady=5, padx=(5,0))

        options_frame = ttk.Labelframe(main_frame, text="Opções de Download", padding=15)
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        options_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(options_frame, text="Nome da Pasta (opcional):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_name_entry = ttk.Entry(options_frame)
        self.folder_name_entry.grid(row=0, column=1, pady=5, sticky=tk.EW, columnspan=2)
        
        self.create_subfolder_var = tk.BooleanVar(value=True)
        self.create_subfolder_checkbox = ttk.Checkbutton(options_frame, text="Criar pasta de download automaticamente", variable=self.create_subfolder_var)
        self.create_subfolder_checkbox.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 10))
        
        self.download_type = tk.StringVar(value="video_audio") 
        format_frame = ttk.Frame(options_frame)
        format_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Label(format_frame, text="Formato:").pack(side=tk.LEFT, anchor=tk.W)
        ttk.Radiobutton(format_frame, text="Vídeo Completo (MP4)", variable=self.download_type, value="video_audio").pack(side=tk.LEFT, padx=(10, 5))
        ttk.Radiobutton(format_frame, text="Apenas Áudio (MP3)", variable=self.download_type, value="audio_only").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="Apenas Vídeo (MP4)", variable=self.download_type, value="video_only").pack(side=tk.LEFT, padx=5)

        ttk.Label(options_frame, text="Arquivo de Cookies:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        self.cookie_file_entry = ttk.Entry(options_frame)
        self.cookie_file_entry.grid(row=3, column=1, sticky=tk.EW, pady=(10, 5))
        self.browse_cookies_button = ttk.Button(options_frame, text="Procurar", image=self.browse_icon, compound=tk.LEFT, command=self.browse_cookie_file)
        self.browse_cookies_button.grid(row=3, column=2, padx=(5,0), pady=(10, 5))

        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        action_button_frame = ttk.Frame(status_frame)
        action_button_frame.pack(pady=10)
        self.download_button = ttk.Button(action_button_frame, text="Baixar", style="Accent.TButton", image=self.download_icon, compound=tk.LEFT, command=self.start_download)
        self.download_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(action_button_frame, text="Cancelar", image=self.cancel_icon, compound=tk.LEFT, command=self.cancel_download, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        self.progress_bar = ttk.Progressbar(status_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5, padx=10)
        self.status_label = ttk.Label(status_frame, text="Pronto para baixar...")
        self.status_label.pack(anchor=tk.W, padx=10, pady=5)

    def browse_path(self):
        initial_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        download_directory = filedialog.askdirectory(initialdir=initial_dir)
        if download_directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, download_directory)
    def browse_cookie_file(self):
        file_path = filedialog.askopenfilename(title="Selecione o arquivo de cookies", filetypes=(("Netscape HTTP Cookie File", "*.txt"), ("All Files", "*.*")))
        if file_path:
            self.cookie_file_entry.delete(0, tk.END)
            self.cookie_file_entry.insert(0, file_path)
    def start_download(self):
        url = self.link_entry.get()
        base_download_path = self.path_entry.get()
        if not url: messagebox.showwarning("Entrada Inválida", "Por favor, insira o link para download."); return
        if not base_download_path: messagebox.showwarning("Entrada Inválida", "Por favor, selecione o diretório para salvar."); return
        self.download_button.config(state=tk.DISABLED); self.cancel_button.config(state=tk.NORMAL)
        self.status_label.config(text="Verificando link..."); self.progress_bar['value'] = 0
        self.download_thread = threading.Thread(target=self._prepare_and_start_download); self.download_thread.start()
    def _prepare_and_start_download(self):
        url = self.link_entry.get(); base_download_path = self.path_entry.get()
        folder_or_prefix_name = self.folder_name_entry.get().strip(); create_subfolder = self.create_subfolder_var.get()
        cookie_file_path = self.cookie_file_entry.get(); self.download_playlist = False; original_url = url
        try:
            ydl_opts_light = {"quiet": True, "skip_download": True, "extract_flat": True}
            if cookie_file_path and os.path.exists(cookie_file_path): ydl_opts_light['cookiefile'] = cookie_file_path
            with yt_dlp.YoutubeDL(ydl_opts_light) as ydl:
                info = ydl.extract_info(url, download=False)
                self.video_title = info.get("title", "Título não encontrado")
                self.root.after(0, lambda: self.title_label.config(text=self.video_title))
                is_playlist = "entries" in info and info.get("_type") == "playlist"
                if is_playlist:
                    total_items = len(info.get("entries", [])); question = f"Este link contém uma playlist com {total_items} itens. Deseja baixar todos?"
                    answer = messagebox.askyesno("Playlist Detectada", question); self.download_playlist = answer
                    if not answer: url = original_url
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro de Análise", f"Não foi possível analisar o link: {e}"))
            self.root.after(0, self._reset_ui_state); return
        download_choice = self.download_type.get(); audio_only = (download_choice == "audio_only"); video_only = (download_choice == "video_only")
        self._run_download(url, base_download_path, folder_or_prefix_name, create_subfolder, audio_only, video_only, cookie_file_path)
    def _run_download(self, url, base_download_path, folder_or_prefix_name, create_subfolder, audio_only, video_only, cookie_file_path):
        self.swiftdl_core.ydl_opts["noplaylist"] = not self.download_playlist
        success = self.swiftdl_core.download(url, base_download_path, folder_or_prefix_name, create_subfolder, audio_only, video_only, cookie_file_path)
        self.root.after(0, self._download_finished, success)
    def _download_finished(self, success):
        self._reset_ui_state()
        if success:
            self.status_label.config(text="Download concluído com sucesso!")
            messagebox.showinfo("Download Concluído", "O download foi concluído com sucesso!")
        else:
            if self.swiftdl_core.download_canceled:
                self.status_label.config(text="Download cancelado."); messagebox.showinfo("Download Cancelado", "O download foi cancelado pelo usuário.")
            else:
                self.status_label.config(text="Download falhou."); messagebox.showerror("Download Falhou", "O download não pôde ser concluído. Verifique o link e as permissões.")
    def _reset_ui_state(self):
        self.download_button.config(state=tk.NORMAL); self.cancel_button.config(state=tk.DISABLED); self.progress_bar['value'] = 0
    def cancel_download(self):
        self.swiftdl_core.cancel_download(); self.status_label.config(text="Cancelando..."); self.cancel_button.config(state=tk.DISABLED)
    def clear_link_entry(self):
        self.link_entry.delete(0, tk.END); self.title_label.config(text="(aguardando análise)")
        self.status_label.config(text="Pronto para baixar..."); self.progress_bar['value'] = 0
    def paste_clipboard(self):
        try:
            self.link_entry.delete(0, tk.END); self.link_entry.insert(0, self.root.clipboard_get())
        except tk.TclError: messagebox.showwarning("Erro", "A área de transferência está vazia.")
    def update_progress(self, percent, status): self.root.after(0, self._update_gui_progress, percent, status)
    def _update_gui_progress(self, percent, status):
        if status == 'downloading': self.progress_bar['value'] = percent; self.status_label.config(text=f"Baixando: {percent:.2f}%")
        elif status == 'finished': self.progress_bar['value'] = 100; self.status_label.config(text="Finalizando...")
        elif status == 'error': self.progress_bar['value'] = 0; self.status_label.config(text="Ocorreu um erro no download.")

if __name__ == '__main__':
    if not check_ffmpeg():
        messagebox.showerror(
            "FFmpeg não encontrado",
            "O FFmpeg é essencial para o SwiftDL funcionar corretamente.\n\n"
            "Por favor, instale-o e adicione-o ao PATH do sistema, ou coloque o executável na mesma pasta do SwiftDL."
        )
    else:
        root = tk.Tk()
        app = SwiftDLApp(root)
        root.mainloop()