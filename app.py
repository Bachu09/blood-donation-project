import json
import os


# Load existing donors
def load_donors():
    if os.path.exists("donors.json"):
        with open("donors.json", "r") as f:
            return json.load(f)
    return []

# Save new donor
def save_donor(donor):
    donors = load_donors()
    donors.append(donor)
    with open("donors.json", "w") as f:
        json.dump(donors, f, indent=4)

# Load users
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return []

# Save new user
def save_user(user):
    users = load_users()
    users.append(user)
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Load camps
def load_camps():
    if os.path.exists("camps.json"):
        with open("camps.json", "r") as f:
            return json.load(f)
    return []

# Save new camp
def save_camp(camp):
    camps = load_camps()
    camps.append(camp)
    with open("camps.json", "w") as f:
        json.dump(camps, f, indent=4)

# Load messages
def load_messages():
    if os.path.exists("messages.json"):
        with open("messages.json", "r") as f:
            return json.load(f)
    return []

# Save message
def save_message(msg):
    messages = load_messages()
    messages.append(msg)
    with open("messages.json", "w") as f:
        json.dump(messages, f, indent=4)

from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "something_secret_and_random"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Load users from users.json
        with open("users.json", "r") as f:
            users = json.load(f)

        # Check if email and password match
        for user in users:
            if user["email"] == email and user["password"] == password:
                session["user"] = user["name"]  # Store user's name in session
                flash(f"Welcome {user['name']}! You’ve successfully logged in.", "success")
                return redirect(url_for("home"))

        flash("Account not found. Please sign up.", "error")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "<h3>Passwords do not match!</h3><a href='/signup'>Try again</a>"

        user = {
            "name": name,
            "email": email,
            "password": password  # ⚠️ You can hash this later for better security
        }

        # Save user using proper function (appends to list and saves clean JSON)
        save_user(user)

        return "<h2>Account created successfully!</h2><a href='/login'>Go to Login</a>"

    return render_template("signup.html")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        donor = {
            "name": request.form["name"],
            "age": request.form["age"],
            "blood_group": request.form["blood_group"],
            "city": request.form["location"],
            "contact": request.form["phone"],
            "message": request.form.get("message", "")
        }
        save_donor(donor)
        return "<h2>Thank you for registering as a donor! ❤️</h2><a href='/'>Go Home</a>"
    return render_template("donate.html")

@app.route("/donors")
def view_donors():
    donors = load_donors()
    search_query = request.args.get('search', '').strip().lower()

    if search_query:
        donors = [
            donor for donor in donors
            if search_query in donor["name"].lower()
            or search_query in donor["city"].lower()
            or donor["blood_group"].lower() == search_query  # exact match for blood group
        ]

    return render_template("donors.html", donors=donors)


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        volunteer = {
            "name": request.form["name"],
            "email": request.form["email"],
            "interest": request.form["interest"],
            "city": request.form["city"]
        }
        # Save to file or database
        with open("volunteers.json", "a") as f:
            f.write(json.dumps(volunteer)+"\n")
        return render_template("thankyou.html", message="Thank you joining us! ❤️")
    return render_template("join.html")


@app.route("/camp", methods=["GET", "POST"])
def organize_camp():
    if request.method == "POST":
        camp = {
            "name": request.form["name"],
            "email": request.form["email"],
            "location": request.form["location"],
            "date": request.form["date"],
            "description": request.form["description"]
        }
        with open("camps.json", "a") as f:
            f.write(json.dumps(camp) + "\n")
        return render_template("thankyou.html", message="Thank you joining us! ❤️")
    return render_template("camp_form.html")


@app.route("/request", methods=["GET", "POST"])
def request_blood():
    if request.method == "POST":
        request_data = {
            "name": request.form["name"],
            "blood_group": request.form["blood_group"],
            "city": request.form["city"],
            "hospital": request.form["hospital"],
            "reason": request.form["reason"],
            "contact": request.form["contact"]
        }
        with open("requests.json", "a") as f:
            f.write(json.dumps(request_data) + "\n")
        return "<h2>Your blood request has been submitted. 🙏</h2><a href='/'>Go Home</a>"
    return render_template("request.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        contact = {
            "name": request.form["name"],
            "email": request.form["email"],
            "subject": request.form["subject"],
            "message": request.form["message"]
        }
        with open("contacts.json", "a") as f:
            f.write(json.dumps(contact) + "\n")
        return render_template("thankyou.html", message="Thank you joining us! ❤️")
    return render_template("contact.html")

if __name__=='__main__':
    app.run(debug=True)