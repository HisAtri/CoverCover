# 列出文件及元数据
import mutagen
import os
from mutagen import File
from mutagen.id3 import ID3, APIC, error


# Mutagen检查当前文件是否包含图片，没有图片->True
def no_cover_art(file_path):
    audio = mutagen.File(file_path)
    if hasattr(audio, "pictures"):
        return len(audio.pictures) == 0
    return True


def search_music(path):
    extensions = ['.mp3', '.wav', '.flac']
    # 初始化音乐列表
    musics_without_cover = []

    # 递归遍历：拓展名为上述，且元数据不包含图片
    def traverse_directory(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(tuple(extensions)) & no_cover_art(file_path):
                    audio = mutagen.File(file_path)
                    musics_without_cover.append({
                        "path": file_path,
                        "artist": audio["artist"],
                        "title": audio["title"],
                        "album": audio["album"]
                    })

            # 递归子目录
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                traverse_directory(subdir_path)

    traverse_directory(path)
    return musics_without_cover


def insert(path, image):
    # 这里的image是图片对象，从网络下载
    audio = ID3(path)
    apic = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Front Cover', data=image)
