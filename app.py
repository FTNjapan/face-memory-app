# =========================================================
# 顔写真暗記アプリ（Web版）
# フォルダ＝チーム名 自動読み込み版
# =========================================================

import os
import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# =========================================================
# 画像フォルダ（ここがデータベース代わり）
# =========================================================
BASE_FOLDER = "static/images"

# =========================================================
# 状態管理（サーバー側）
# =========================================================
image_files = []   # 現在の画像一覧
current_index = 0  # 何枚目か


# =========================================================
# チーム一覧取得（←ここが重要）
# フォルダ名＝チーム名になる
# =========================================================
@app.route("/teams")
def get_teams():

    teams = [
        d for d in os.listdir(BASE_FOLDER)
        if os.path.isdir(os.path.join(BASE_FOLDER, d))
    ]

    return jsonify(teams)


# =========================================================
# チーム選択
# =========================================================
@app.route("/team/<team_name>")
def select_team(team_name):

    global image_files, current_index

    folder = os.path.join(BASE_FOLDER, team_name)

    # 画像一覧取得
    image_files = [
        f"/static/images/{team_name}/{f}"
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    # ランダム化
    random.shuffle(image_files)

    current_index = 0

    return jsonify({"status": "ok"})


# =========================================================
# 次の画像取得
# =========================================================
@app.route("/next")
def next_image():

    global image_files, current_index

    if current_index >= len(image_files):
        return {"end": True}

    path = image_files[current_index]

    filename = os.path.basename(path)
    name = os.path.splitext(filename)[0]

    current_index += 1

    return {
        "image": path,   # ←これでOK（そのまま使う）
        "answer": name
    }

# =========================================================
# 画面
# =========================================================
@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# Render対応
# =========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)