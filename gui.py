# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
from yt_dlp import YoutubeDL
from baixar_playlist import (
    baixar_playlist_audio_mp3_320kbps,
    baixar_playlist_video_mp4_720p,
    baixar_playlist_completo_mp4
)
import estilo

# Estilo
if estilo.BOOTSTRAP_ATIVO:
    from ttkbootstrap import ttk
else:
    from tkinter import ttk

# Variáveis globais
progresso_percentual = 0
total_videos = 0
videos_baixados = 0

def escolher_diretorio(entry_widget):
    pasta = filedialog.askdirectory()
    if pasta:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, pasta)

def hook_progresso(d):
    global videos_baixados
    if d['status'] == 'finished':
        videos_baixados += 1
        percentual_total = (videos_baixados / total_videos) * 100
        progress_var.set(percentual_total)
        progress_bar.update_idletasks()
        status_label.config(text=f"Baixando {videos_baixados} de {total_videos} arquivos...")

def contar_videos_playlist(url):
    ydl_opts = {'quiet': True, 'extract_flat': 'in_playlist'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return len(info.get('entries', [url]))

def thread_download():
    global total_videos, videos_baixados
    try:
        total_videos = contar_videos_playlist(entry_url.get().strip())
        videos_baixados = 0
        status_label.config(text=f"Iniciando download de {total_videos} arquivos...")

        # Escolhe a função com base na seleção do formato
        formato_escolhido = formato_var.get()

        if formato_escolhido == "mp3":
            baixar_playlist_audio_mp3_320kbps(
                url=entry_url.get().strip(),
                caminho_base=entry_destino.get().strip(),
                hook_progresso=hook_progresso
            )
        elif formato_escolhido == "video":
            baixar_playlist_video_mp4_720p(
                url=entry_url.get().strip(),
                caminho_base=entry_destino.get().strip(),
                hook_progresso=hook_progresso
            )
        elif formato_escolhido == "completo":
            baixar_playlist_completo_mp4(
                url=entry_url.get().strip(),
                caminho_base=entry_destino.get().strip(),
                hook_progresso=hook_progresso
            )

        status_label.config(text="Download finalizado com sucesso!")
        messagebox.showinfo("Concluído", "Download finalizado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
        status_label.config(text="Erro durante o download.")
    finally:
        btn_baixar.config(state='normal')
        progress_var.set(0)

def iniciar_download():
    if not entry_url.get().strip() or not entry_destino.get().strip():
        messagebox.showerror("Erro", "Por favor, insira o link e selecione o destino.")
        return

    btn_baixar.config(state='disabled')
    Thread(target=thread_download).start()

# GUI principal
root = tk.Tk()
estilo.aplicar_estilo(root)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Frame principal
main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(1, weight=1)

# Link da Playlist
ttk.Label(main_frame, text="Link da Playlist:").grid(row=0, column=0, sticky='w', pady=(0, 5))
entry_url = ttk.Entry(main_frame)
entry_url.grid(row=0, column=1, columnspan=2, sticky='ew', pady=(0, 5))

# Destino
ttk.Label(main_frame, text="Destino:").grid(row=1, column=0, sticky='w', pady=(0, 5))
entry_destino = ttk.Entry(main_frame)
entry_destino.grid(row=1, column=1, sticky='ew', pady=(0, 5))
estilo.criar_botao(main_frame, "Procurar", lambda: escolher_diretorio(entry_destino), "info").grid(row=1, column=2, padx=5)

# Formato
ttk.Label(main_frame, text="Formato:").grid(row=2, column=0, sticky='w', pady=(10, 5))
formato_var = tk.StringVar(value="mp3")
formato_frame = ttk.Frame(main_frame)
formato_frame.grid(row=2, column=1, columnspan=2, sticky='w')
ttk.Radiobutton(formato_frame, text="Somente áudio (MP3)", variable=formato_var, value="mp3").pack(anchor='w')
ttk.Radiobutton(formato_frame, text="Somente vídeo (MP4)", variable=formato_var, value="video").pack(anchor='w')
ttk.Radiobutton(formato_frame, text="Vídeo completo com áudio (MP4)", variable=formato_var, value="completo").pack(anchor='w')

# Progresso
ttk.Label(main_frame, text="Progresso:").grid(row=3, column=0, sticky='w', pady=(10, 5))
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100)
progress_bar.grid(row=3, column=1, columnspan=2, sticky='ew', pady=(10, 5))

# Botão de download
btn_baixar = estilo.criar_botao(main_frame, "Baixar Playlist", iniciar_download, "success")
btn_baixar.grid(row=4, column=1, pady=10)

# Status
status_label = ttk.Label(main_frame, text="")
status_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(5, 0))

root.mainloop()
