# StudyCircle — Study Group Finder

A full-featured Flask web application for students to create, discover, and join study groups.

---

## Features

| Feature | Details |
|---|---|
| Browse groups | Search by keyword, subject, tag. Live client-side filter. |
| Create group | Validated form — name, subject, description, schedule, tags |
| Group detail page | Members list, announcements, discussion board with replies |
| Join request | Full validated form — name, email, student ID, year, reason |
| Join validations | Duplicate email check, capacity check, rejection history check |
| Admin panel | Approve / reject requests, post announcements, remove members, open/close group |
| Discussion board | Top-level posts + threaded replies per group |
| Dashboard | Look up your groups and request status by email |
| Responsive | Works on mobile, tablet, and desktop |

---

## Tech Stack

- **Backend**: Python 3, Flask, SQLite
- **Frontend**: HTML5, Bootstrap 5, CSS3
- **Behaviour**: JavaScript, jQuery 3.7
- **Templating**: Jinja2
- **Database**: SQLite (auto-created on first run)

---

## Project Structure

```
studycircle/
├── app.py                    ← Flask routes, DB schema, validation logic
├── requirements.txt
├── studycircle.db            ← Auto-created on first run
├── templates/
│   ├── base.html             ← Shared layout (navbar, flash, footer)
│   ├── index.html            ← Browse + search groups
│   ├── group_detail.html     ← Detail + members + announcements + discussion
│   ├── join.html             ← Join request form (full validation)
│   ├── create.html           ← Create group form
│   ├── admin.html            ← Admin panel (approve/reject/announce/remove)
│   ├── dashboard.html        ← Personal dashboard
│   ├── success.html          ← Confirmation page
│   └── 404.html              ← Error page
└── static/
    ├── css/style.css         ← Custom styles
    └── js/script.js          ← jQuery behaviours
```

---

## Setup & Run

```bash
# 1. Clone / unzip and enter directory
cd studycircle

# 2. Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py

# 5. Open in browser
http://127.0.0.1:5000
```

The SQLite database (`studycircle.db`) is created automatically with sample data on first run.

---

## Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home — browse + search groups |
| `/group/<id>` | GET | Group detail — members, announcements, discussion |
| `/group/<id>/join` | GET/POST | Join request form (validated) |
| `/group/<id>/discuss` | POST | Post a discussion message or reply |
| `/create` | GET/POST | Create a new group |
| `/admin/<id>` | GET | Admin panel for a group |
| `/admin/<id>/approve/<rid>` | POST | Approve a join request |
| `/admin/<id>/reject/<rid>` | POST | Reject a join request |
| `/admin/<id>/remove/<mid>` | POST | Remove a member |
| `/admin/<id>/announce` | POST | Post an announcement |
| `/admin/<id>/toggle-status` | POST | Open/close the group |
| `/dashboard` | GET | Personal dashboard — look up by email |
| `/success` | GET | Post-action confirmation |

---

## Join Request Validations

- Full name — minimum 3 characters
- Email — valid format (`name@domain.tld`)
- Student ID — minimum 4 characters
- Year of study — must select from dropdown
- Reason — minimum 20 characters
- Duplicate check — same email cannot submit twice for same group
- Member check — already-a-member emails are rejected
- Rejection check — previously rejected emails are blocked
- Capacity check — re-verified at submit time

---

## Git Setup

```bash
git init
git add .
git commit -m "Initial commit — StudyCircle v1.0"
git remote add origin https://github.com/YOUR_USERNAME/studycircle.git
git push -u origin main
```
