from flask import Flask, render_template
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

users = {
    "archie.andrews@email.com": "football4life",
    "veronica.lodge@email.com": "fashiondiva"
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.is_submitted():
        print("Submitted.")

    if form.validate():
        print("Valid.")

    if form.validate_on_submit():
       print("Submitted and Valid.")
    elif form.errors:
        print(form.errors.items())
        print(form.email.errors)
        print(form.password.errors)

    return render_template("login.html", form = form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
