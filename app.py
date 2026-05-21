from flask import Flask, render_template, jsonify
import os
import random

app = Flask(__name__)

BASE_FOLDER = "static/images"

image_files = []
current_index = 0


# 初期化（チーム読み込み）
def load_images(team):

    global image_files, current_index

    folder = os.path.join(BASE_FOLDER, team)

    image_files = [
        os.path.join(team, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    random.shuffle(image_files)
    current_index = 0


@app.route("/")
def index():
    return render_template("index.html")


# 次の画像
@app.route("/next")
def next_image():

    global current_index

    if current_index >= len(image_files):
        return jsonify({"end": True})

    path = image_files[current_index]
    current_index += 1

    return jsonify({
        "image": "/static/images/" + path,
        "name": os.path.splitext(os.path.basename(path))[0]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)