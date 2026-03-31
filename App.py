from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Firebase
cred = credentials.Certificate("send-snap-9ab1c-firebase-adminsdk-fbsvc-867042e170.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
loggedInUserDetails ={}

# ========== AUTH DECORATOR ==========
def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user = session.get("user")
            if not user or (role and user["role"] != role):
                flash("Access denied. Please log in with appropriate credentials.")
                return redirect(url_for("login"))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# ========== ROUTES ==========

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.")
            return redirect(url_for("login"))

        try:
            user_query = db.collection("users").where("email", "==", email).where("password", "==", password).stream()
            user = next(user_query, None)

            if user:
                user_data = user.to_dict()
                session["user"] = {
                    "email": user_data["email"],
                    "role": user_data["role"]
                }
                flash("Login successful!")

                if user_data["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("problem_View"))
            else:
                flash("Invalid credentials. Please try again.")
        except Exception as e:
            flash(f"Login failed due to server error: {str(e)}")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if not email or not password or not role:
            flash("All fields are required.")
            return redirect(url_for("register"))

        try:
            existing_user = db.collection("users").where("email", "==", email).stream()
            if any(existing_user):
                flash("User already exists. Please login.")
                return redirect(url_for("login"))

            user_data = {
                "email": email,
                "password": password,  # For production, hash this!
                "role": role
            }

            db.collection("users").add(user_data)
            flash("Registration successful! Please login.")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Registration failed: {str(e)}")

    return render_template("registration.html")

@app.route("/postProblem", methods=["GET", "POST"])
@login_required(role="user")
def postProblem():
    if request.method == "POST":
        mobile = request.form.get("mobile")
        photo_file = request.files.get("photo")
        comment = request.form.get("comment")
        problem_type = request.form.get("problem_type")
        location = request.form.get("location")

        if not mobile or not photo_file or not comment or not problem_type or not location:
            flash("All fields are required.")
            return redirect(url_for("postProblem"))

        try:
            safe_filename = secure_filename(photo_file.filename)
            photo_filename = f"{datetime.utcnow().timestamp()}_{safe_filename}"
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo_file.save(photo_path)

            report_data = {
                "mobile": mobile,
                "photo": photo_filename,
                "comment": comment,
                "problem_type": problem_type,
                "location": location,
                "status": "Pending",
                "admin_comment": "",
                "email":session['user']['email'],
                "created_at": datetime.utcnow()
            }

            db.collection("problem_reports").add(report_data)
            flash("Problem submitted successfully!")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Failed to submit problem: {str(e)}")

    return render_template("submit_problem.html")

@app.route("/admin")
@login_required(role="admin")
def admin_dashboard():
    try:
        reports = db.collection("problem_reports").order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        report_list = [r.to_dict() | {"id": r.id} for r in reports]
        return render_template("admin_dashboard.html", reports=report_list)
    except Exception as e:
        flash(f"Failed to load reports: {str(e)}")
        return render_template("admin_dashboard.html", reports=[])

@app.route("/problemView")
@login_required(role="user")
def problem_View():
    try:
        reports = db.collection("problem_reports").order_by("created_at", direction=firestore.Query.DESCENDING).stream()
        report_list = [r.to_dict() | {"id": r.id} for r in reports]
        return render_template("problemView.html", reports=report_list)
    except Exception as e:
        flash(f"Failed to load your reports: {str(e)}")
        return render_template("problemView.html", reports=[])

@app.route("/admin/update/<report_id>", methods=["POST"])
@login_required(role="admin")
def update_report(report_id):
    try:
        report_ref = db.collection("problem_reports").document(report_id)
        print(report_ref)
        report_ref.update({
            "status": request.form.get("status"),
            "admin_comment": request.form.get("admin_comment")
        })
        updated_report = report_ref.get().to_dict()
        # Check if the issue is resolved
        if request.form.get("status") == 'Resolved':
           # Email content
            subject = f"{updated_report['problem_type']} Issue Has Been Resolved"
            body = """Hi there,

            Thank you for reporting the issue. We're happy to let you know that it's been resolved.

            If you have any further concerns, feel free to reach out.

            Best regards,
            Support Team
            """

            sender_email = "clientproject735@gmail.com"
            receiver_email = updated_report['email']
            password = "jehahzmyfvdehykd"  # ✅ App Password without spaces
            print("Reciver mail : ",receiver_email)

            # Create MIMEText object
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = receiver_email

            # Send the email using SMTP
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                print("✅ Email sent successfully.")
            except Exception as e:
                print(f"❌ Error sending email: {e}")
                flash("Report updated successfully!")
    except Exception as e:
        flash(f"Failed to update report: {str(e)}")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete/<report_id>", methods=["POST"])
@login_required(role="admin")
def delete_report(report_id):
    try:
        report_ref = db.collection("problem_reports").document(report_id)
        report_ref.delete()
        flash("Report deleted successfully!")
    except Exception as e:
        flash(f"Failed to delete report: {str(e)}")
    return redirect(url_for("admin_dashboard"))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/service")
def service():
    return render_template("service.html")

# ========== INIT ==========
if __name__ == "__main__":
    app.run(debug=True)
