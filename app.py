from flask import Flask, render_template, jsonify
import os
import random

app = Flask(__name__)

BASE_FOLDER = "static/images"

image_files = []
current_index = 0
current_team = ""


# -------------------------
# チーム読み込み
# -------------------------
def load_team(team):

    global image_files, current_index, current_team

    folder = os.path.join(BASE_FOLDER, team)

    image_files = [
        f"/static/images/{team}/{f}"
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    random.shuffle(image_files)

    current_index = 0
    current_team = team


@app.route("/")
def index():
    return render_template("index.html")


# -------------------------
# 次の画像
# -------------------------
@app.route("/next")
def next_image():

    global current_index

    if current_index >= len(image_files):
        return jsonify({"end": True})

    path = image_files[current_index]
    name = os.path.splitext(os.path.basename(path))[0]

    current_index += 1

    return jsonify({
        "image": path,
        "name": name
    })


# -------------------------
# チーム選択
# -------------------------
@app.route("/team/<team>")
def team(team):
    load_team(team)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)