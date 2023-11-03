import requests

from mod import read_config

config = read_config.load()


def ncm(title):
    api = config["api_url"]
    response = requests.get(f"{api}/search?keywords={title}")
    if response.status_code == 200:
        result_list = response.json()["result"]
        id_list = []
        for song_detail in result_list["songs"]:
            id_list.append({"id": song_detail["id"],
                            "name": song_detail["name"],
                            "artist": "&".join([i["name"] for i in song_detail["artists"]])})

        return id_list


def ncm_image(ncm_id):
    api_url = config["api_url"]+"song/detail?ids="+str(ncm_id)
    response = requests.get(api_url)
    # 检查响应状态码
    if response.status_code == 200:
        detail = response.json()
        return detail["songs"][0]["al"]["picUrl"]
    else:
        return ""


# 聚合多个搜索
def search(title):
    match config["api_type"]:
        case "ncm_api":
            return ncm(title)


# 图片搜索，返回图片URL
def search_img(song_id):
    match config["api_type"]:
        case "ncm_api":
            return ncm_image(song_id)
