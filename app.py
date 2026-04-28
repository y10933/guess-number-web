from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "guessgame_rank_v2"

def new_game(level):
    session["level"] = level
    session["answer"] = random.randint(1, level)
    session["count"] = 0

    # 排行榜（最少次數）
    if "rank" not in session:
        session["rank"] = []

    # 歷史紀錄（每一局）
    if "history" not in session:
        session["history"] = []

@app.route("/", methods=["GET", "POST"])
def index():

    if "answer" not in session:
        new_game(100)

    level = session.get("level", 100)
    message = "🎮 開始猜數字！"

    # 切換難度
    if request.method == "POST" and "level" in request.form:
        level = int(request.form["level"])
        new_game(level)
        message = f"🎯 難度切換：1 ~ {level}"

    # 猜數字
    elif request.method == "POST":
        guess = int(request.form["guess"])
        session["count"] += 1
        answer = session["answer"]

        if guess > answer:
            message = "📈 太大"
        elif guess < answer:
            message = "📉 太小"
        else:
            message = f"🎉 正確！共 {session['count']} 次"

            # 🔥 排行榜（最少次數）
            rank = session.get("rank", [])
            rank.append(session["count"])
            rank.sort()
            session["rank"] = rank[:5]

            # 🔥 每一局歷史紀錄
            history = session.get("history", [])
            history.append(session["count"])
            session["history"] = history[-10:]  # 保留最近10局

            new_game(level)

    return render_template(
        "index.html",
        message=message,
        level=level,
        rank=session.get("rank", []),
        history=session.get("history", [])
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
