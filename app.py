from flask import Flask, render_template, redirect, request, make_response, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)




@app.route("/loginsubmit", methods=["POST"])
def loginsubmit():
    uname = request.form.get("name")
    password = request.form.get("pass")
    user = User.query.filter_by(username=uname).first()
    print(user)
    if user:
        if password == user.password:
            # resp = make_response(render_template('dashboard.html'))
            # resp.set_cookie("dashboard", "true")
            # resp.set_cookie("username", uname)
            # return resp
            return render_template('dashboard.html', user=user)
        else:
            return "Wrong password."
    else:
        # Redirect to the login page with an error message
        return redirect(url_for('home'))



@app.route("/createaccount", methods=["POST"])
def createaccount():
    if request.method == 'POST':
        username = request.form['regname']
        password = request.form['regpass']
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for('register'))
        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('home.html')   
    return render_template('home.html')            


@app.route("/sample")
def sample():
    return render_template('sample.html')

@app.route("/logout")
def logout():
    return render_template("home.html") 

@app.route("/", methods=["POST", 'GET'])
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
