import yt_dlp
import os

def download_media(url, format_type='video', output_path='downloads'):
    """
    Downloads media from URL using yt-dlp.
    format_type: 'video' (best) or 'audio' (mp3)
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    options = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    if format_type == 'audio':
        options.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Default best video+audio
        options.update({
            'format': 'bestvideo+bestaudio/best',
        })

    # Support for TikTok, FB, etc. is native in yt-dlp
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                "success": True,
                "title": info.get('title', 'Unknown Title'),
                "filename": ydl.prepare_filename(info),
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration_string', '0:00'),
                "uploader": info.get('uploader', 'Unknown Uploaded')
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_info(url):
    """
    Just retrieves info without downloading
    """
    options = {
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "success": True,
                "title": info.get('title', 'Unknown Title'),
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration_string', '0:00'),
                "uploader": info.get('uploader', 'Unknown Uploader'),
                "id": info.get('id')
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
