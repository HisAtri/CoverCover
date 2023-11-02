from flask import Flask, request, abort, redirect, send_from_directory
import requests
import logging

from mod import mulist
from mod import read_config


app = Flask(__name__)
config = read_config.load()


@app.route("/")
def index_page():
    return send_from_directory('src', 'index.html')


@app.route("/list_music")
def list_music():
    return mulist.search_music(config["root_path"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('')
    # serve(app, host='0.0.0.0', port=args.port)
    app.run(host='0.0.0.0', port=28884)
