from flask import Flask, render_template, request, redirect, flash, session, url_for, send_file
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash
from fpdf import FPDF
import csv
from io import BytesIO
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Email Configuration 
app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dixie.cartwright26@ethereal.email'
app.config['MAIL_PASSWORD'] = 'pDEcgfWNH8jenha669'

mail = Mail(app)

# ===== Admin Credentials (Hashed) =====
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")  # Store hashed password

# ===== In-memory stores =====
messages = []
subscribers = []

@app.route("/test-email")
def test_email():
    try:
        msg = Message("🔥 Test Email from Dada Flow",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=["dadaflowinitiative@gmail.com"])  # Replace with your real test email
        msg.body = "Brother genius, this is a test email from your Flask app."
        mail.send(msg)
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Failed to send: {e}"

# ===== Login Route =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin"] = True
            return redirect("/admin/dashboard")
        else:
            flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully.", "info")
    return redirect("/login")

# ===== Admin Dashboard with Stats =====
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/login")

    latest_msg = messages[-1] if messages else None
    return render_template("dashboard.html", 
        total_msgs=len(messages),
        total_subs=len(subscribers),
        latest_msg=latest_msg
    )

# ===== Admin Inbox =====
@app.route("/admin/inbox")
def admin_inbox():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("admin_inbox.html", messages=messages)

# ===== Message Delete =====
@app.route("/admin/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    if not session.get("admin"):
        return redirect("/login")
    global messages
    messages = [msg for msg in messages if msg["id"] != msg_id]
    flash("Message deleted.", "success")
    return redirect("/admin/inbox")

# ===== Reply Page (Form) =====
@app.route("/admin/reply/<int:msg_id>", methods=["GET", "POST"])
def reply_message(msg_id):
    if not session.get("admin"):
        return redirect("/login")
    msg = next((m for m in messages if m["id"] == msg_id), None)
    if not msg:
        flash("Message not found", "error")
        return redirect("/admin/inbox")

    if request.method == "POST":
        reply_body = request.form["reply"]
        try:
            reply_email = Message(
                subject="Reply from Dada Flow Admin",
                sender=app.config['MAIL_USERNAME'],
                recipients=[msg["email"]],
                body=reply_body
            )
            mail.send(reply_email)
            flash("Reply sent successfully ✅", "success")
        except Exception as e:
            flash(f"Failed to send reply: {str(e)}", "error")
        return redirect("/admin/inbox")

    return render_template("reply.html", message=msg)

# ===== Export Inbox =====
@app.route("/export/csv")
def export_csv():
    if not session.get("admin"):
        return redirect("/login")
    output = BytesIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Message"])
    for msg in messages:
        writer.writerow([msg["id"], msg["name"], msg["email"], msg["message"]])
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="inbox_messages.csv", mimetype="text/csv")

@app.route("/export/pdf")
def export_pdf():
    if not session.get("admin"):
        return redirect("/login")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dada Flow - Admin Inbox Messages", ln=True, align='C')
    pdf.ln(10)
    for msg in messages:
        pdf.multi_cell(0, 10, f"Name: {msg['name']}\nEmail: {msg['email']}\nMessage: {msg['message']}\n", border=1)
        pdf.ln(2)
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="inbox_messages.pdf", mimetype="application/pdf")

# ===== Contact Page =====
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        try:
            msg_obj = Message(
                subject=f"New Message from {name} via Dada Flow",
                sender=email,
                recipients=["dadaflowinitiative@gmail.com"],
                body=f"From: {name} <{email}>\n\n{message}"
            )
            mail.send(msg_obj)

            messages.append({
                "id": len(messages) + 1,
                "name": name,
                "email": email,
                "message": message,
                "date": datetime.datetime.now()
            })

            flash("Message sent! ❤️", "success")
        except Exception as e:
            flash(f"Failed to send: {str(e)}", "error")
        return redirect("/contact")

    return render_template("contact.html")

# ===== Newsletter =====
@app.route("/subscribe", methods=["POST"])
def subscribe():
    name = request.form["name"]
    email = request.form["email"]
    subscribers.append((name, email))
    flash("Thanks for subscribing ❤️", "success")
    return redirect("/")

# ===== Pages =====
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/programs")
def programs():
    return render_template("programs.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

volunteers = []

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Store the volunteer locally
        volunteers.append({
            "name": name,
            "email": email,
            "message": message
        })

        # Attempt to send confirmation email to admin
        try:
            msg = Message(
                subject=f"New Volunteer: {name}",
                sender=email,
                recipients=["dadaflowinitiative@gmail.com"],
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Thank you for signing up to volunteer! ❤️", "success")
        except Exception as e:
            flash(f"Volunteer saved, but email failed: {str(e)}", "error")

        return redirect("/volunteer")

    return render_template("volunteer.html")

@app.route("/admin/volunteers")
def admin_volunteers():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("admin_volunteers.html", volunteers=volunteers)

@app.route("/admin/volunteers/download")
def download_volunteers():
    if not session.get("admin"):
        return redirect("/login")

    from flask import make_response
    import csv

    si = []
    output = csv.writer(si := [])
    output.writerow(["Name", "Email", "Message"])
    output.writerows([[v["name"], v["email"], v["message"]] for v in volunteers])

    response = make_response("\n".join([",".join(row) for row in si]))
    response.headers["Content-Disposition"] = "attachment; filename=volunteers.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@app.route("/donate")
def donate():
    return render_template("donate.html")

# ===== Run =====
if __name__ == "__main__":
    app.run(debug=True)
