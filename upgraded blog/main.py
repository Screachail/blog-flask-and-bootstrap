import smtplib
import ssl

from flask import Flask, render_template, url_for, request
import requests

all_posts = requests.get("https://api.npoint.io/a53029a368980191a77b").json()
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html', all_posts=all_posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in all_posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    global data
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    ctx = ssl.create_default_context()
    password = "SENDER EMAIL PASSWORD"  # Your app password goes here
    sender = "SENDER GMAIL"  # Your gmail address
    receiver = "YOUR EMAIL"  # Recipient's address
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, email_message)





if __name__ == "__main__":
    app.run(debug=True)
