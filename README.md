# 📚 StudyCircle

> **Connect with students who share your subjects. Join a group, set a schedule, and reach your academic goals — together.**

StudyCircle is a full-stack web application built for college students to **discover, create, and manage study groups**. It features email-based login, an organiser admin panel, threaded discussions, join request approvals, and a personal dashboard — all wrapped in a clean, modern UI.

---



 🏠 Home Page — Browse & Search Groups
> Students land here first. The hero section, live search bar, subject filter, and tag filter all work together to help students find the right group instantly.

<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/5943c1fd-26a6-4e5d-ac84-d82db09a96d5" />


---
🔍 Search & Filter in Action
> Students can search by group name, subject, organiser name, or tag. Results update as filters are applied.

<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/4e8d6fda-4d76-49d4-819f-c274ceed089b" />


---

### 📋 Group Detail Page
> Clicking any group card opens this page. Shows full description, schedule, location, organiser info, member list, capacity bar, announcements, and the threaded discussion board.

![Group Detail](screenshots/group_detail.png)

---

 💬 Discussion Board
> Every group has a built-in threaded discussion board. Members can post messages and reply to existing threads — no login required to participate.


---

 📝 Join Request Form
> Students fill out this form to request membership. The organiser reviews each request before approving or rejecting it.

<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/f7df91b7-dd72-4fc4-842b-f67bed13d6bc" />


---

✅ Join Request Submitted — Success Page
> After submitting a join request or creating a group, students are shown this confirmation page.
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/1a039ebb-3dd7-421c-9da9-b69e67f32988" />

---

 ➕ Create a Group
> Any logged-in student can create a new study group. They fill in the name, subject, description, location, schedule, max members, and tags.
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/18495129-40d3-45a5-9c4f-13b7eae64511" />


---

 🔐 Login Page
> Email-based login — no password needed. Students log in with the same email they used when joining or creating a group.
<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/4690b0a9-54c1-4394-8257-52c68a618285" />


---

 🛠️ Admin Panel — Manage Requests
> Only the group organiser can access this panel. Shows all pending join requests with Approve / Reject buttons, request history, member list with remove option, and an announcement form.

<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/31095bfc-cbbe-4327-898d-eaf94c3ba585" />


---

📊 My Dashboard
> Students enter their email to see all groups they belong to, their role (organiser/member), and the status of all their join requests (pending/approved/rejected).

<img width="1920" height="1008" alt="image" src="https://github.com/user-attachments/assets/eeda0bba-dd97-4490-8c48-04ab1d6e1b7b" />


---

✨ Features

For Students
- 🔍 **Browse & search** study groups by name, subject, organiser, or tag
- 📋 **View full group details** — schedule, location, member count, capacity bar
- 📝 **Submit join requests** with name, student ID, year of study, and reason
- 💬 **Participate in discussions** — threaded posts with reply support
- 📊 **Personal dashboard** — see all your groups and request statuses
- 🔐 **Email-based login** — no password needed, uses your registered college email

 For Organisers
- ➕ **Create study groups** with full details and tags
- ✅ **Approve or reject** join requests one by one
- 👥 **View and manage** all group members
- ❌ **Remove members** from the group
- 📢 **Post announcements** visible to everyone on the group page
- 🔒 **Open or close** the group to new members with one click
- 🛡️ **Protected admin panel** — only accessible to the actual organiser

---

 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite (via `sqlite3`) |
| Frontend | HTML5, Jinja2 Templates |
| Styling | Bootstrap 5.3, Custom CSS |
| Icons | Bootstrap Icons 1.11 |
| Fonts | Syne (headings), DM Sans (body) |
| Auth | Flask Sessions (email-based) |
| JS | jQuery 3.7, Bootstrap JS |

---

 📁 Project Structure

```
studycircle/
│
├── app.py                        # Main Flask app — all routes and logic
├── requirements.txt              # Python dependencies
├── studycircle.db                # SQLite database (auto-created on first run)
│
├── static/
│   ├── css/
│   │   └── style.css             # All custom styles and CSS variables
│   └── js/
│       └── script.js             # Client-side validation and interactivity
│
├── templates/
│   ├── base.html                 # Base layout — navbar, flash messages, footer
│   ├── index.html                # Home page — hero, stats bar, search, group cards
│   ├── group_detail.html         # Group page — info, members, announcements, discussions
│   ├── join.html                 # Join request form with validation
│   ├── create.html               # Create group form
│   ├── admin.html                # Organiser-only admin panel
│   ├── dashboard.html            # Personal dashboard — groups and request status
│   ├── login.html                # Email login page
│   ├── success.html              # Confirmation page after join/create
│   └── 404.html                  # Error page (also used for 403, 500)

```

---

 🗄️ Database Schema

The app uses **5 SQLite tables**:

 `study_groups`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment ID |
| name | TEXT | Group name |
| subject | TEXT | Subject category |
| description | TEXT | Full description |
| location | TEXT | Meeting location |
| schedule | TEXT | Meeting schedule |
| max_members | INTEGER | Maximum allowed members |
| organiser | TEXT | Organiser's full name |
| contact_email | TEXT | Organiser's email (used for login auth) |
| tags | TEXT | Comma-separated tags |
| status | TEXT | `open` or `closed` |
| created_at | TEXT | Timestamp |

 `join_requests`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment ID |
| group_id | INTEGER FK | References `study_groups.id` |
| full_name | TEXT | Applicant's name |
| email | TEXT | Applicant's email |
| student_id | TEXT | College student ID |
| year_of_study | TEXT | 1st / 2nd / 3rd / 4th Year |
| reason | TEXT | Why they want to join |
| status | TEXT | `pending` / `approved` / `rejected` |
| requested_at | TEXT | Timestamp |

 `members`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment ID |
| group_id | INTEGER FK | References `study_groups.id` |
| full_name | TEXT | Member's name |
| email | TEXT | Member's email |
| student_id | TEXT | College student ID |
| role | TEXT | `organiser` or `member` |
| joined_at | TEXT | Timestamp |

 `announcements`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment ID |
| group_id | INTEGER FK | References `study_groups.id` |
| title | TEXT | Announcement title |
| body | TEXT | Full announcement text |
| posted_at | TEXT | Timestamp |

 `discussions`
| Column | Type | Description |
|---|---|---|
| id | INTEGER PK | Auto-increment ID |
| group_id | INTEGER FK | References `study_groups.id` |
| author | TEXT | Poster's name |
| email | TEXT | Poster's email |
| message | TEXT | Message content |
| parent_id | INTEGER | NULL for top-level, references parent post for replies |
| posted_at | TEXT | Timestamp |

---

#🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

 Installation & Running

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/studycircle.git
cd studycircle

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open your browser and visit: **http://127.0.0.1:5000**

The database is created and seeded automatically on first run — no setup needed.

---

 🌱 Seeded Demo Data

The app comes pre-loaded with **8 study groups** and their organiser accounts. You can log in as any of them to test the admin panel:

| Group | Subject | Organiser | Login Email |
|---|---|---|---|
| Data Structures Warriors | Computer Science | Arjun Sharma | arjun@college.edu |
| Calculus Crusaders | Mathematics | Priya Nair | priya@uni.edu |
| Quantum Physics Club | Physics | Rahul Verma | rahul@college.edu |
| ML & AI Explorers | Data Science | Sneha Rao | sneha@tech.edu |
| Organic Chemistry Fighters | Chemistry | Vikram Iyer | vikram@college.edu |
| Economics & Markets | Economics | Meera Pillai | meera@uni.edu |
| GATE CSE Prep | Computer Science | Kiran Babu | kiran@college.edu |
| English Literature Circle | English Literature | Divya Menon | divya@arts.edu |

Group 1 (Data Structures Warriors) also has **2 pre-seeded pending join requests** so you can test the approve/reject flow immediately after logging in as `arjun@college.edu`.

---
 🔐 How Authentication Works

StudyCircle uses a simple **email-based session login** — no passwords:

```
1. User visits /login
2. Enters their college email
3. App checks if that email exists in the members table
4. If found → email is stored in Flask session
5. User is now "logged in" as that person
```

**Organiser protection:** Every admin route calls `require_organiser(gid)` which compares the session email against the group's `contact_email` in the database. If they don't match → **403 Access Denied**. This works for all groups including seeded ones.

```python
def require_organiser(gid):
    email = current_user()
    if not email:
        # redirect to login
    grp = get_db().execute(
        "SELECT contact_email FROM study_groups WHERE id=?", (gid,)
    ).fetchone()
    if email.lower() != grp["contact_email"].lower():
        abort(403)   # wrong person → blocked
```

---

 🗺️ All Routes

| Method | URL | Description | Auth Required |
|---|---|---|---|
| GET | `/` | Home page — browse and search groups | No |
| GET | `/group/<id>` | Group detail page | No |
| POST | `/group/<id>/discuss` | Post a discussion message | No |
| GET/POST | `/group/<id>/join` | Submit a join request | No |
| GET/POST | `/create` | Create a new group | No |
| GET/POST | `/login` | Email login | No |
| GET | `/logout` | Log out | No |
| GET | `/dashboard` | Personal dashboard | No |
| GET | `/admin/<id>` | Admin panel | ✅ Organiser only |
| POST | `/admin/<id>/approve/<rid>` | Approve a join request | ✅ Organiser only |
| POST | `/admin/<id>/reject/<rid>` | Reject a join request | ✅ Organiser only |
| POST | `/admin/<id>/remove/<mid>` | Remove a member | ✅ Organiser only |
| POST | `/admin/<id>/announce` | Post an announcement | ✅ Organiser only |
| POST | `/admin/<id>/toggle-status` | Open/close the group | ✅ Organiser only |
| GET | `/success` | Confirmation page | No |

---
 📸 How to Add Screenshots

1. Run the app locally with `python app.py`
2. Open `http://127.0.0.1:5000` in your browser
3. Create a `screenshots/` folder in your project root
4. Take screenshots of each page and save them with these exact filenames:

| Filename | What to capture |
|---|---|
| `home.png` | Full home page with group cards visible |
| `search.png` | Home page with a search term typed in |
| `group_detail.png` | A group's detail page showing all info |
| `discussion.png` | The discussion board section of a group |
| `join.png` | The join request form |
| `success.png` | The success/confirmation page |
| `create.png` | The create group form |
| `login.png` | The login page |
| `admin.png` | The admin panel with pending requests |
| `dashboard.png` | The dashboard showing groups and requests |

**On Windows:** Press `Win + Shift + S` to snip a region → save as PNG into the `screenshots/` folder.

---

 ⚠️ Known Limitations

- No real password system — login is email-only (suitable for a college project)
- No email notifications when requests are approved or rejected
- No CSRF protection on forms
- SQLite is not suitable for high-traffic production use
- The secret key is hardcoded — should use environment variables in production

---

🔮 Future Improvements

- [ ] Password-based authentication with hashing
- [ ] Email notifications for request status updates
- [ ] CSRF token protection on all forms
- [ ] File and resource sharing inside groups
- [ ] Group chat / real-time messaging
- [ ] Student profile pages
- [ ] Mobile app version

---

👩‍💻 Built With

This project was built as a **Full Stack Web Development** college project using:
- **Flask** for the backend and routing
- **SQLite** for the database
- **Bootstrap 5** for responsive UI
- **Jinja2** for server-side templating
- **Custom CSS** for the StudyCircle design system

---

📄 License

This project is for educational purposes only.
