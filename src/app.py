import secrets
import uuid
from datetime import datetime, timedelta

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# In-memory storage (dict of SecretData)
secrets_store = {}


class SecretData:
    def __init__(self, content, time_limit):
        self.id = str(uuid.uuid4())
        self.content = content
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=time_limit)
        self.viewed = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        content = request.form.get("content")
        time_limit = int(request.form.get("time_limit", 30))

        if not content:
            flash("Content is required")
            return redirect(url_for("create"))

        secret = SecretData(content, time_limit)
        secrets_store[secret.id] = secret

        return render_template("create_success.html", secret_id=secret.id)

    return render_template("create.html")


@app.route("/reveal", methods=["GET", "POST"])
def reveal():
    if request.method == "POST":
        secret_id = request.form.get("secret_id")

        if not secret_id:
            return render_template("reveal.html", error="Token is required")

        secret = secrets_store.get(secret_id)

        if not secret:
            return render_template("reveal.html", error="Secret not found")

        if datetime.now() > secret.expires_at:
            del secrets_store[secret_id]
            return render_template("reveal.html", error="Secret expired")

        if secret.viewed:
            return render_template("reveal.html", error="Secret already viewed")

        secret.viewed = True
        content = secret.content
        del secrets_store[secret_id]  # Burn after viewing
        return render_template("reveal.html", content=content)

    return render_template("reveal.html")


@app.route("/peek/<secret_id>")
def peek(secret_id):
    secret = secrets_store.get(secret_id)

    if not secret:
        return "NOT_FOUND"

    if datetime.now() > secret.expires_at:
        del secrets_store[secret_id]
        return "EXPIRED"

    return "VALID"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)
