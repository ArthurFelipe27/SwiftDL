# baixar_playlist.py
import os
import sys
import yt_dlp

def get_ffmpeg_path():
    """
    Detecta o caminho do ffmpeg.exe embutido no executável ou na pasta do projeto
    """
    if getattr(sys, 'frozen', False):  # Quando rodar como .exe
        base_path = sys._MEIPASS  # Pasta temporária criada pelo PyInstaller
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "ffmpeg", "ffmpeg.exe")

def baixar_playlist_audio_mp3_320kbps(url, caminho_base='.', hook_progresso=None):
    ffmpeg_path = get_ffmpeg_path()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{caminho_base}/%(playlist_title)s/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'prefer_ffmpeg': True,
        'ffmpeg_location': ffmpeg_path,
        'keepvideo': False,
        'ignoreerrors': True,
    }
    if hook_progresso:
        ydl_opts['progress_hooks'] = [hook_progresso]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_playlist_video_mp4_720p(url, caminho_base='.', hook_progresso=None):
    ffmpeg_path = get_ffmpeg_path()
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]',
        'outtmpl': f'{caminho_base}/%(playlist_title)s/%(title)s.%(ext)s',
        'prefer_ffmpeg': True,
        'ffmpeg_location': ffmpeg_path,
        'ignoreerrors': True,
    }
    if hook_progresso:
        ydl_opts['progress_hooks'] = [hook_progresso]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_playlist_completo_mp4(url, caminho_base='.', hook_progresso=None):
    ffmpeg_path = get_ffmpeg_path()
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{caminho_base}/%(playlist_title)s/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'prefer_ffmpeg': True,
        'ffmpeg_location': ffmpeg_path,
        'ignoreerrors': True,
    }
    if hook_progresso:
        ydl_opts['progress_hooks'] = [hook_progresso]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
