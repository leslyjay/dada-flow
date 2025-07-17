# 🌸 Dada Flow Initiative Website

A web platform built to **spread love, dignity, and awareness** around menstrual hygiene for schoolgirls in **Kilifi, Kenya**. This powerful platform allows users to connect, volunteer, and view programs aimed at empowering young women.

---

## 🚀 Features

- 🏠 Home, About, Programs, Gallery, Contact Pages  
- 📬 Contact form with Gmail integration  
- 🧾 Newsletter / Volunteer email signup  
- 🛡️ Admin inbox (secured with login)  
- 📤 Export subscribers as CSV  
- ⚡ Built with Flask + Tailwind CSS  

---

## 🛠️ Tech Stack

- Python (Flask)
- Flask-Mail
- Tailwind CSS (CDN)
- HTML Templates (Jinja2)

---

## 📁 Folder Structure
📦 DadaFlowWebsite/
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
├── templates/
│ ├── index.html
│ ├── about.html
│ ├── programs.html
│ ├── gallery.html
│ ├── contact.html
│ ├── login.html
│ ├── volunteer.html
│ └── admin_inbox.html
├── static/
│ └── img/ (logo and images)


---

## 📧 Contact Form (Gmail Setup)

1. Enable 2-Step Verification on your Gmail
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Set these in `app.py` or your `.env`:

```python
app.config['MAIL_USERNAME'] = 'dadaflowinitiative@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password_here'

💞 Credits
Built by [Dada Flow Digital Team 💻]

Designed to touch lives, uplift girls, and empower the future

Engineered with ❤️ in Kenya