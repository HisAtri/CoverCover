from flask import Flask, request, abort, send_from_directory
from flask_caching import Cache
import requests
import logging

from mod import mulist
from mod import read_config
from mod import music
from mod import imagex

app = Flask(__name__)
config = read_config.load()
cache = Cache(app, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './flask_cache'
})


# 缓存键，解决缓存未忽略参数的情况
def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return path + args


# 主页，返回/src/index.html
@app.route("/")
def index_page():
    return send_from_directory('src', 'index.html')


# 资源目录。路由该目录
@app.route('/src/<path:filename>')
def serve_file(filename):
    try:
        return send_from_directory('src', filename)
    except FileNotFoundError:
        abort(404)


# JsonAPI GET列出所有无图片的音乐
@app.route("/list_music")
def list_music():
    return mulist.search_music(config["root_path"])


# POST API 服务端搜索，形式为/search POST keywords=<keywords>
@app.route("/search", methods=["POST"])
def search():
    keywords = request.form.get("keywords", "")
    if keywords:
        return music.search(keywords)
    else:
        abort(403, "请携带搜索词")


# TextAPI Album图片链接接口，带缓存，传入参数id=song_id
@app.route("/image")
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def search_image():
    song_id = request.args.get("id", None)
    if song_id:
        return music.search_img(song_id)
    else:
        abort(403, "缺少指定音乐ID")


# POST API 插入图片
@app.route("/insert", methods=["POST"])
def insert_data():
    file_path = request.form.get("file", "")
    insert_id = request.form.get("id", "")
    if insert_id == "" and file_path == "":
        return 400
    else:
        try:
            img_url = music.search_img(insert_id)
            image_b = imagex.processed_image(img_url)
            mulist.insert(file_path, image_b)
        except Exception as e:
            return 500, e


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('')
    # serve(app, host='0.0.0.0', port=args.port)
    app.run(host='0.0.0.0', port=28891)
