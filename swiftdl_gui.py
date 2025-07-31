import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import yt_dlp
from datetime import datetime
from swiftdl_core import SwiftDLCore

class SwiftDLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SwiftDL - Download de Mídia")
        self.root.geometry("600x570") # Ajustado o tamanho da janela para acomodar o campo de cookies
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("TEntry", font=("Arial", 10))
        self.style.configure("TCheckbutton", font=("Arial", 10))
        self.style.configure("TProgressbar", thickness=20)

        self.swiftdl_core = SwiftDLCore()
        self.swiftdl_core.set_progress_callback(self.update_progress)

        self.download_playlist = False # Começa como False, será definido na análise
        self.video_title = ""
        self.create_widgets()
        self.download_thread = None

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Linha 0: Link do Vídeo/Áudio
        ttk.Label(main_frame, text="Link do Vídeo/Áudio:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.link_entry = ttk.Entry(main_frame, width=48)
        self.link_entry.grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))
        self.paste_button = ttk.Button(main_frame, text="Colar", command=self.paste_clipboard)
        self.paste_button.grid(row=0, column=2, pady=5, padx=5)
        self.clear_button = ttk.Button(main_frame, text="Limpar", command=self.clear_link_entry)
        self.clear_button.grid(row=0, column=3, pady=5, padx=5)

        # Linha 1: Título do vídeo
        ttk.Label(main_frame, text="Título/Nome:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.title_label = ttk.Label(main_frame, text="(aguardando análise)")
        self.title_label.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=5)

        # Linha 2: Salvar em
        ttk.Label(main_frame, text="Salvar em:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.path_entry = ttk.Entry(main_frame, width=50)
        self.path_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
        self.browse_button = ttk.Button(main_frame, text="Procurar", command=self.browse_path)
        self.browse_button.grid(row=2, column=2, pady=5, padx=5)

        # Linha 3: Nome da Pasta (opcional)
        ttk.Label(main_frame, text="Nome da Pasta (opcional):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.folder_name_entry = ttk.Entry(main_frame, width=60)
        self.folder_name_entry.grid(row=3, column=1, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        self.folder_name_entry.insert(0, "")

        # Linha 4: Criar pasta de download automaticamente
        self.create_subfolder_var = tk.BooleanVar(value=True)
        self.create_subfolder_checkbox = ttk.Checkbutton(main_frame, text="Criar pasta de download automaticamente", variable=self.create_subfolder_var)
        self.create_subfolder_checkbox.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Linha 5: Baixar apenas áudio (MP3)
        self.audio_only_var = tk.BooleanVar()
        self.audio_only_checkbox = ttk.Checkbutton(main_frame, text="Baixar apenas áudio (MP3)", variable=self.audio_only_var)
        self.audio_only_checkbox.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Linha 6: Baixar apenas vídeo (MP4)
        self.video_only_var = tk.BooleanVar()
        self.video_only_checkbox = ttk.Checkbutton(main_frame, text="Baixar apenas vídeo (MP4)", variable=self.video_only_var)
        self.video_only_checkbox.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Nova Linha 7: Arquivo de Cookies
        ttk.Label(main_frame, text="Arquivo de Cookies (opcional):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.cookie_file_entry = ttk.Entry(main_frame, width=50)
        self.cookie_file_entry.grid(row=7, column=1, pady=5, sticky=(tk.W, tk.E))
        self.browse_cookies_button = ttk.Button(main_frame, text="Procurar", command=self.browse_cookie_file)
        self.browse_cookies_button.grid(row=7, column=2, pady=5, padx=5)

        # Linha 8: Botões de Ação
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        self.download_button = ttk.Button(button_frame, text="Baixar", command=self.start_download)
        self.download_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        # Linha 9: Barra de Progresso
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.grid(row=9, column=0, columnspan=3, pady=10)

        # Linha 10: Status do Download
        self.status_label = ttk.Label(main_frame, text="Pronto para baixar...")
        self.status_label.grid(row=10, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Configurar coluna 1 para expandir
        main_frame.grid_columnconfigure(1, weight=1)

    def browse_path(self):
        """Abre uma caixa de diálogo para o usuário selecionar o diretório de download."""
        initial_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        download_directory = filedialog.askdirectory(initialdir=initial_dir)
        if download_directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, download_directory)

    def browse_cookie_file(self):
        """Abre uma caixa de diálogo para o usuário selecionar o arquivo de cookies."""
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo de cookies",
            filetypes=(("Netscape HTTP Cookie File", "*.txt"), ("All Files", "*.*"))
        )
        if file_path:
            self.cookie_file_entry.delete(0, tk.END)
            self.cookie_file_entry.insert(0, file_path)

    def start_download(self):
        """Inicia o processo de download em uma thread separada."""
        url = self.link_entry.get()
        base_download_path = self.path_entry.get()
        folder_or_prefix_name = self.folder_name_entry.get().strip()
        create_subfolder = self.create_subfolder_var.get()
        cookie_file_path = self.cookie_file_entry.get()

        if not url:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira o link para download.")
            return

        if not base_download_path:
            messagebox.showwarning("Entrada Inválida", "Por favor, selecione o diretório para salvar.")
            return

        # Desabilita o botão de download e habilita o de cancelar, e atualiza o status da UI
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.status_label.config(text="Verificando link... (pode levar alguns segundos para playlists grandes)")
        self.progress_bar['value'] = 0

        # Inicia a análise e o download em uma nova thread para não travar a GUI
        self.download_thread = threading.Thread(
            target=self._prepare_and_start_download,
            args=(url, base_download_path, folder_or_prefix_name, create_subfolder, cookie_file_path)
        )
        self.download_thread.start()

    def _prepare_and_start_download(self, url, base_download_path, folder_or_prefix_name, create_subfolder, cookie_file_path):
        """
        Analisa o link, detecta playlists e pergunta ao usuário,
        então inicia o download no core.
        """
        self.download_playlist = False # Reseta a flag para cada nova análise
        original_url = url # Guarda a URL original caso o usuário não queira a playlist completa

        try:
            # Opções leves para extrair informações básicas sem baixar todo o conteúdo
            ydl_opts_light = {"quiet": True, "skip_download": True, "extract_flat": True}
            # Inclui o cookiefile para a verificação inicial, útil para playlists privadas
            if cookie_file_path and os.path.exists(cookie_file_path):
                ydl_opts_light['cookiefile'] = cookie_file_path

            with yt_dlp.YoutubeDL(ydl_opts_light) as ydl:
                info = ydl.extract_info(url, download=False)

                # Tenta obter o título. Se for uma playlist, inicialmente pode ser o título do primeiro item
                self.video_title = info.get("title", "Título não encontrado")
                self.root.after(0, lambda: self.title_label.config(text=self.video_title))

                # Verifica se é uma playlist baseada no tipo de informação ou heurística da URL
                is_a_playlist_by_info = "entries" in info and info.get("_type") == "playlist"
                is_a_playlist_by_url = 'list=' in url.lower() or 'playlist?' in url.lower() or 'index=' in url.lower()

                if is_a_playlist_by_info or is_a_playlist_by_url:
                    total_items = 0
                    # Tenta obter o número exato de itens para a pergunta
                    if is_a_playlist_by_info and info.get("entries"):
                        total_items = len(info["entries"])
                        # Se for uma playlist e tiver um título mais genérico, usa-o
                        if info.get("title"):
                            self.video_title = info["title"]
                            self.root.after(0, lambda: self.title_label.config(text=self.video_title))
                    elif is_a_playlist_by_url:
                        # Se detectado pela URL, mas extract_flat não deu o total de entries (raro para URLs válidas)
                        self.root.after(0, lambda: self.status_label.config(text="Playlist potencial detectada. Analisando itens para contagem..."))
                        try:
                            # Tenta uma extração mais completa para obter o total de itens, se necessário
                            ydl_opts_full_info = {"quiet": True, "skip_download": True}
                            if cookie_file_path and os.path.exists(cookie_file_path):
                                ydl_opts_full_info['cookiefile'] = cookie_file_path

                            with yt_dlp.YoutubeDL(ydl_opts_full_info) as ydl_full_info:
                                full_info = ydl_full_info.extract_info(url, download=False)
                                if "entries" in full_info:
                                    total_items = len(full_info["entries"])
                                    if full_info.get("title"):
                                        self.video_title = full_info["title"]
                                        self.root.after(0, lambda: self.title_label.config(text=self.video_title))
                        except Exception as e_full_info:
                            print(f"Erro ao obter info completa da playlist (pode ser vídeo privado/indisponível na playlist): {e_full_info}")
                            # Se falhar a info completa, ainda assim tentamos perguntar
                            self.video_title = "Playlist detectada" if not self.video_title else self.video_title


                    question_text = ""
                    if total_items > 0:
                        question_text = f"Este link contém uma playlist com {total_items} itens. Deseja baixar todos?"
                    else:
                        question_text = "Este link parece ser uma playlist. Deseja baixar todos os itens? (Não foi possível obter a contagem exata de itens)."

                    answer = messagebox.askyesno("Playlist Detectada", question_text)
                    self.download_playlist = answer

                    if not answer:
                        # Se o usuário NÃO quiser a playlist completa, o yt-dlp deve baixar apenas o primeiro item.
                        # Para isso, usaremos a URL original e setaremos 'noplaylist' para True no core.
                        url = original_url # Garante que a URL seja a original do primeiro item ou da playlist
                        self.download_playlist = False # Força o download de um único item
                    # Se answer for True, self.download_playlist já é True e a URL original será usada.
                else:
                    self.download_playlist = False # Não é uma playlist, baixa item único


        except yt_dlp.utils.DownloadError as e:
            error_message = str(e)
            if "Private video" in error_message or "unavailable videos are hidden" in error_message:
                self.root.after(0, lambda: messagebox.showerror("Erro de Acesso",
                                                                 "Não foi possível acessar o vídeo/playlist. Pode ser um vídeo privado ou indisponível. "
                                                                 "Tente fornecer um arquivo de cookies se tiver acesso à conta."))
            elif "No video formats found" in error_message:
                self.root.after(0, lambda: messagebox.showerror("Erro de Formato",
                                                                 "Nenhum formato de vídeo/áudio compatível encontrado para este link. "
                                                                 "O vídeo pode ser restrito ou não suportado."))
            else:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao processar o link: {e}"))
            self.root.after(0, lambda: self.status_label.config(text="Erro ao analisar o link."))
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.cancel_button.config(state=tk.DISABLED))
            return
        except Exception as e:
            # Captura outros erros inesperados durante a análise
            self.root.after(0, lambda: self.status_label.config(text="Erro inesperado ao analisar o link."))
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro inesperado durante a análise: {e}"))
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.cancel_button.config(state=tk.DISABLED))
            return

        # Validação das opções de download (áudio/vídeo)
        audio_only = self.audio_only_var.get()
        video_only = self.video_only_var.get()

        if audio_only and video_only:
            messagebox.showwarning("Opção Inválida", "Selecione apenas uma opção: áudio ou vídeo.")
            self.root.after(0, lambda: self.download_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.cancel_button.config(state=tk.DISABLED))
            return

        if not audio_only and not video_only:
            audio_only = False  # Padrão é baixar vídeo completo (audio e video)

        # Inicia o download real no core
        self.download_thread = threading.Thread(
            target=self._run_download,
            args=(url, base_download_path, folder_or_prefix_name, create_subfolder, audio_only, cookie_file_path)
        )
        self.download_thread.start()

    def _run_download(self, url, base_download_path, folder_or_prefix_name, create_subfolder, audio_only, cookie_file_path):
        """Executa o método de download no SwiftDLCore."""
        # Define a opção 'noplaylist' no core com base na escolha do usuário na GUI
        self.swiftdl_core.ydl_opts["noplaylist"] = not self.download_playlist
        success = self.swiftdl_core.download(url, base_download_path, folder_or_prefix_name, create_subfolder, audio_only, cookie_file_path)
        self.root.after(0, self._download_finished, success)

    def _download_finished(self, success):
        """Atualiza a GUI após o término do download (sucesso, falha ou cancelamento)."""
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0

        if success:
            self.status_label.config(text="Download concluído com sucesso!")
            messagebox.showinfo("Download Concluído", "O download foi concluído com sucesso!")
        else:
            self.status_label.config(text="Download cancelado ou falhou.")
            # Exibe uma mensagem de cancelamento ou de erro, dependendo da causa
            if self.swiftdl_core.download_canceled:
                messagebox.showinfo("Download Cancelado", "O download foi cancelado pelo usuário.")
            else:
                # Se não foi cancelado pelo usuário, assume que foi um erro
                messagebox.showerror("Download Falhou", "O download não pôde ser concluído devido a um erro. Verifique o link e as permissões.")


    def cancel_download(self):
        """Solicita o cancelamento do download em andamento."""
        self.swiftdl_core.cancel_download()
        self.status_label.config(text="Solicitando cancelamento...")
        self.cancel_button.config(state=tk.DISABLED)

    def clear_link_entry(self):
        """Limpa o campo de entrada do link."""
        self.link_entry.delete(0, tk.END)
        self.title_label.config(text="(aguardando análise)")
        self.status_label.config(text="Pronto para baixar...")
        self.progress_bar['value'] = 0

    def paste_clipboard(self):
        """Cola o conteúdo da área de transferência no campo de link."""
        try:
            clipboard = self.root.clipboard_get()
            self.link_entry.delete(0, tk.END)
            if self.is_valid_link(clipboard):
                self.link_entry.insert(0, clipboard)
                # Inicia a análise automaticamente após colar um link válido
                self.start_download()
            else:
                messagebox.showwarning("Link inválido", "O conteúdo colado não parece ser um link suportado (YouTube, TikTok, etc).")
        except tk.TclError:
            messagebox.showwarning("Erro", "A área de transferência está vazia ou contém conteúdo inválido.")

    def is_valid_link(self, text):
        """Verifica se o texto parece ser um link válido de uma plataforma suportada."""
        # Lista de plataformas suportadas, pode ser expandida
        platforms = ["youtube.com", "youtu.be", "tiktok.com", "instagram.com", "facebook.com", "pinterest.com"]
        return any(p in text.lower() for p in platforms)

    def update_progress(self, percent, status):
        """Atualiza a barra de progresso e o status na GUI de forma segura na thread principal."""
        self.root.after(0, self._update_gui_progress, percent, status)

    def _update_gui_progress(self, percent, status):
        """Atualiza os widgets da GUI com o progresso do download."""
        if status == 'downloading':
            self.progress_bar['value'] = percent
            self.status_label.config(text=f"Baixando: {percent:.2f}%")
        elif status == 'finished':
            self.progress_bar['value'] = 100
            self.status_label.config(text="Finalizando...")
        elif status == 'error':
            self.progress_bar['value'] = 0
            self.status_label.config(text="Ocorreu um erro no download.")

if __name__ == '__main__':
    root = tk.Tk()
    app = SwiftDLApp(root)
    root.mainloop()