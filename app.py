from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "game"

def new_game():
    session["answer"] = random.randint(1, 100)
    session["count"] = 0

@app.route("/", methods=["GET", "POST"])
def index():
    if "answer" not in session:
        new_game()

    message = "🎮 猜 1～100"

    if request.method == "POST":
        guess = int(request.form["guess"])
        session["count"] += 1

        if guess > session["answer"]:
            message = "📈 太大"
        elif guess < session["answer"]:
            message = "📉 太小"
        else:
            message = f"🎉 猜對！共 {session['count']} 次"
            new_game()

    return render_template("index.html", message=message)

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
