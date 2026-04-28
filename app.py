from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "guessgame123"

def new_game():
    session["answer"] = random.randint(1, 100)
    session["count"] = 0

@app.route("/", methods=["GET", "POST"])
def index():
    if "answer" not in session:
        new_game()

    message = "🎮 猜 1～100 的數字"

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
        except:
            return render_template("index.html", message="請輸入數字")

        session["count"] += 1
        answer = session["answer"]

        if guess > answer:
            message = "📈 太大"
        elif guess < answer:
            message = "📉 太小"
        else:
            message = f"🎉 猜對！共 {session['count']} 次"
            new_game()

    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
