import flet as ft
from downloader import download_media, get_info
import threading
import os

def main(page: ft.Page):
    # App General Config
    page.title = "Nour Downloader (YouTube, TikTok, FB, etc.)"
    page.theme_mode = "dark"
    page.window_width = 450
    page.window_height = 800
    page.padding = 30
    page.bgcolor = "#121212"  # Deep Premium Dark
    page.scroll = "auto"
    
    # Custom Gold Color
    gold_color = "#D4AF37"
    dark_card = "#1E1E1E"

    # State
    current_info = None

    # Components
    header = ft.Text(
        "Nour Downloader", 
        size=28, 
        weight="bold", 
        color=gold_color,
        text_align="center",
        width=400
    )
    
    subtitle = ft.Text(
        "Download anything, anywhere.",
        size=14,
        color="#888888",
        text_align="center",
        italic=True,
        width=400
    )

    url_input = ft.TextField(
        label="Paste Video Link",
        hint_text="https://www.youtube.com/watch?v=...",
        border_color=gold_color,
        border_radius=15,
        focused_border_color=gold_color,
        prefix_icon="link",
        height=65,
        on_change=lambda e: update_preview(e.data)
    )

    # Preview Area
    preview_img = ft.Image(
        src="",
        width=300,
        height=180,
        border_radius=12,
        fit="cover",
        visible=False
    )
    
    title_text = ft.Text("", size=16, weight="bold", color="white", visible=False)
    info_text = ft.Text("", size=13, color="#AAAAAA", visible=False)
    
    preview_card = ft.Container(
        content=ft.Column([
            preview_img,
            title_text,
            info_text
        ], alignment="center"),
        bgcolor=dark_card,
        padding=15,
        border_radius=15,
        visible=False,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.Colors.with_opacity(0.1, "black"))
    )

    status_text = ft.Text("", size=14, italic=True)
    progress_bar = ft.ProgressBar(width=400, color=gold_color, bgcolor="#333333", visible=False)

    def update_preview(url):
        if not url:
            preview_card.visible = False
            page.update()
            return

        def fetch_info():
            nonlocal current_info
            status_text.value = "Analyzing link..."
            status_text.color = gold_color
            page.update()
            
            info = get_info(url)
            if info["success"]:
                current_info = info
                preview_img.src = info["thumbnail"]
                preview_img.visible = True
                title_text.value = info["title"]
                title_text.visible = True
                info_text.value = f"Duration: {info['duration']} | By: {info['uploader']}"
                info_text.visible = True
                preview_card.visible = True
                status_text.value = "Ready to download!"
                status_text.color = "green"
            else:
                status_text.value = f"Error: {info.get('error', 'Invalid link')}"
                status_text.color = "red"
                preview_card.visible = False
            page.update()

        threading.Thread(target=fetch_info).start()

    def start_download(format_type):
        url = url_input.value
        if not url:
            status_text.value = "Please enter a valid link first"
            status_text.color = "orange"
            page.update()
            return
            
        def download_proc():
            progress_bar.visible = True
            status_text.value = f"Downloading {format_type.upper()}..."
            status_text.color = gold_color
            page.update()
            
            res = download_media(url, format_type=format_type)
            
            if res["success"]:
                status_text.value = f"Successfully Downloaded: {res['title']}"
                status_text.color = "green"
            else:
                status_text.value = f"Failed to download: {res.get('error', 'Unknown Error')}"
                status_text.color = "red"
            
            progress_bar.visible = False
            page.update()

        threading.Thread(target=download_proc).start()

    # Buttons
    btn_video = ft.ElevatedButton(
        content=ft.Text("Download MP4 Video", weight="bold", color="black"),
        icon="video_library",
        bgcolor=gold_color,
        width=400,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=lambda _: start_download("video")
    )
    
    btn_audio = ft.ElevatedButton(
        content=ft.Text("Download MP3 Audio", weight="bold"),
        icon="audio_file",
        bgcolor="#333333",
        width=400,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=lambda _: start_download("audio")
    )

    # Platforms list
    platforms_row = ft.Row([
        ft.Icon("play_circle_filled", color="#FF0000", size=30), # YouTube
        ft.Icon("music_video", color="#ffffff" if page.theme_mode == "dark" else "#000000", size=30),       # TikTok
        ft.Icon("facebook", color="#1877F2", size=30),          # FB
        ft.Icon("camera_alt", color="#E4405F", size=30),          # IG (standard camera icon as alternative)
    ], alignment="center", spacing=20)

    # Layout Assembly
    page.add(
        ft.Column([
            ft.Container(height=20),
            header,
            subtitle,
            ft.Divider(height=40, color="#333333"),
            url_input,
            ft.Container(height=10),
            status_text,
            progress_bar,
            preview_card,
            ft.Container(height=20),
            btn_video,
            ft.Container(height=10),
            btn_audio,
            ft.Container(height=30),
            ft.Text("Supported Platforms", size=12, color="#555555", weight="bold"),
            platforms_row,
            ft.Container(height=20),
            ft.Text("Dahab Downloader Engine v1.0", size=10, color="#222222")
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main)
