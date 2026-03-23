from flask import (Flask, render_template, request,
                   redirect, url_for, flash, g, abort, session)
import sqlite3, re, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "studycircle_secret_key_2024")
DB = "studycircle.db"

# ─────────────────────────── DB helpers ──────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db:
        db.close()

def valid_email(e):
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$", e.strip()))

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def member_count(db, gid):
    return db.execute(
        "SELECT COUNT(*) FROM members WHERE group_id=?", (gid,)
    ).fetchone()[0]

def pending_count(db, gid):
    return db.execute(
        "SELECT COUNT(*) FROM join_requests WHERE group_id=? AND status='pending'",
        (gid,)
    ).fetchone()[0]

# ─────────────────────────── Auth helpers ────────────────────────────────────

def current_user():
    """Return logged-in email from session, or None."""
    return session.get("user_email")


def require_organiser(gid):
    """
    Redirects to login if not logged in.
    Aborts with 403 if logged-in user is NOT the organiser of this group.
    Compares session email against contact_email in DB —
    works for ALL groups including seeded ones.
    """
    email = current_user()
    if not email:
        flash("Please log in to access the admin panel.", "warning")
        abort(redirect(url_for("login", next=request.url)))

    grp = get_db().execute(
        "SELECT contact_email FROM study_groups WHERE id=?", (gid,)
    ).fetchone()
    if not grp:
        abort(404)
    if email.lower() != grp["contact_email"].lower():
        abort(403)

# ─────────────────────────── DB init + seed ──────────────────────────────────

def init_db():
    db = sqlite3.connect(DB)
    db.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS study_groups (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        name          TEXT    NOT NULL,
        subject       TEXT    NOT NULL,
        description   TEXT    NOT NULL,
        location      TEXT    NOT NULL,
        schedule      TEXT    NOT NULL,
        max_members   INTEGER NOT NULL DEFAULT 10,
        organiser     TEXT    NOT NULL,
        contact_email TEXT    NOT NULL,
        tags          TEXT    DEFAULT '',
        status        TEXT    DEFAULT 'open',
        created_at    TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS join_requests (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id      INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
        full_name     TEXT    NOT NULL,
        email         TEXT    NOT NULL,
        student_id    TEXT    NOT NULL,
        year_of_study TEXT    NOT NULL,
        reason        TEXT    NOT NULL,
        status        TEXT    DEFAULT 'pending',
        requested_at  TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS members (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id      INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
        full_name     TEXT    NOT NULL,
        email         TEXT    NOT NULL,
        student_id    TEXT    NOT NULL,
        role          TEXT    DEFAULT 'member',
        joined_at     TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS announcements (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id  INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
        title     TEXT    NOT NULL,
        body      TEXT    NOT NULL,
        posted_at TEXT    NOT NULL
    );

    CREATE TABLE IF NOT EXISTS discussions (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id   INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
        author     TEXT    NOT NULL,
        email      TEXT    NOT NULL,
        message    TEXT    NOT NULL,
        parent_id  INTEGER DEFAULT NULL,
        posted_at  TEXT    NOT NULL
    );
    """)
    db.commit()

    # ── Seed only if empty ────────────────────────────────────────────────────
    if db.execute("SELECT COUNT(*) FROM study_groups").fetchone()[0] > 0:
        db.close()
        return

    t = ts()
    groups = [
        ("Data Structures Warriors", "Computer Science",
         "Weekly DSA problem-solving sessions. We grind LeetCode, practice system design, "
         "and prepare for placement interviews. Beginners welcome — we start from basics.",
         "Library Room 3", "Sat & Sun 3–5 PM", 8, "Arjun Sharma", "arjun@college.edu",
         "DSA,LeetCode,Placements,System Design"),

        ("Calculus Crusaders", "Mathematics",
         "Deep-dive into integrals, series, ODEs, and multivariable calculus using Thomas & Finney. "
         "We work through problem sets together and hold doubt-clearing sessions before exams.",
         "Block-A Seminar Hall", "Mon & Wed 5–6:30 PM", 10, "Priya Nair", "priya@uni.edu",
         "Calculus,Maths,Exams,Problem Sets"),

        ("Quantum Physics Club", "Physics",
         "Exploring quantum mechanics and modern physics from Griffiths. Weekly concept discussions, "
         "problem-solving marathons, and occasional journal paper reviews.",
         "Physics Lab 2", "Tue & Thu 4–6 PM", 6, "Rahul Verma", "rahul@college.edu",
         "Physics,Quantum,Research,Griffiths"),

        ("ML & AI Explorers", "Data Science",
         "Building real ML projects together — supervised learning, neural nets, NLP, and cloud deployment. "
         "We run Kaggle competitions as a team and document everything on GitHub.",
         "Online (Google Meet)", "Sun 2–4 PM", 12, "Sneha Rao", "sneha@tech.edu",
         "ML,AI,Python,Deep Learning,Kaggle"),

        ("Organic Chemistry Fighters", "Chemistry",
         "Mastering reaction mechanisms, IUPAC naming, spectroscopy (IR, NMR, MS), and retrosynthesis. "
         "Friendly peer-teaching environment with a strong focus on exam preparation.",
         "Chem Block Room 5", "Fri 3–5 PM", 8, "Vikram Iyer", "vikram@college.edu",
         "Chemistry,Organic,Mechanisms,Spectroscopy"),

        ("Economics & Markets", "Economics",
         "Discussing macro & micro economics, financial markets, and Indian economic policy. "
         "We also cover current affairs and case studies for competitive exam preparation.",
         "Commerce Block 2", "Wed 4–5:30 PM", 15, "Meera Pillai", "meera@uni.edu",
         "Economics,Markets,Finance,UPSC"),

        ("GATE Computer Science Prep", "Computer Science",
         "Structured preparation for GATE CSE — OS, DBMS, CN, Algorithms, TOC. "
         "We follow a topic-wise schedule with weekly mock tests and peer review.",
         "Room 207, Main Block", "Mon/Wed/Fri 6–8 PM", 20, "Kiran Babu", "kiran@college.edu",
         "GATE,CSE,OS,DBMS,Algorithms"),

        ("English Literature Circle", "English Literature",
         "Reading and analysing classic and contemporary literature. "
         "Monthly book discussions, essay writing workshops, and poetry appreciation sessions.",
         "Arts Block Common Room", "Sat 11 AM–1 PM", 12, "Divya Menon", "divya@arts.edu",
         "Literature,Reading,Essays,Poetry"),
    ]

    for g_data in groups:
        gid = db.execute("""
            INSERT INTO study_groups
              (name,subject,description,location,schedule,max_members,
               organiser,contact_email,tags,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (*g_data, t)).lastrowid

        gname      = g_data[0]
        gorganiser = g_data[6]
        gorg_email = g_data[7]

        db.execute("""
            INSERT INTO members (group_id,full_name,email,student_id,role,joined_at)
            VALUES (?,?,?,?,?,?)
        """, (gid, gorganiser, gorg_email, "ORGANISER", "organiser", t))

        db.execute("""
            INSERT INTO announcements (group_id,title,body,posted_at)
            VALUES (?,?,?,?)
        """, (gid,
              f"Welcome to {gname}!",
              "Thanks for joining! Our first session details have been shared via email. "
              "Please introduce yourself in the discussion thread below.",
              t))

        db.execute("""
            INSERT INTO discussions (group_id,author,email,message,parent_id,posted_at)
            VALUES (?,?,?,?,?,?)
        """, (gid, gorganiser, gorg_email,
              "Welcome everyone! Drop a quick intro below — your name, year, and what you're hoping to get out of this group.",
              None, t))

    for req in [
        ("Anjali Mehta", "anjali@college.edu", "21CS045", "3rd Year",
         "I want to crack FAANG. I need a disciplined group to practice DSA daily. "
         "I can contribute by sharing resources and helping juniors."),
        ("Suresh Kumar", "suresh@college.edu", "22CS018", "2nd Year",
         "Just started competitive programming. This group looks perfect for structured DSA prep. "
         "I am very consistent and never miss sessions."),
    ]:
        db.execute("""
            INSERT INTO join_requests
              (group_id,full_name,email,student_id,year_of_study,reason,status,requested_at)
            VALUES (1,?,?,?,?,?,'pending',?)
        """, (*req, t))

    extras = {
        3: [("Pooja Singh","pooja@college.edu","21PH012"),
            ("Aditya Roy","aditya@college.edu","20PH034"),
            ("Nandini Das","nandini@college.edu","21PH056")],
        4: [("Ravi Teja","ravi@tech.edu","21DS001"),
            ("Lavanya K","lavanya@tech.edu","21DS022"),
            ("Manoj P","manoj@tech.edu","20DS099")],
        5: [("Preeti Gupta","preeti@college.edu","21CH011")],
    }
    for gid, mlist in extras.items():
        for m in mlist:
            db.execute("""
                INSERT INTO members (group_id,full_name,email,student_id,role,joined_at)
                VALUES (?,?,?,?,'member',?)
            """, (gid, m[0], m[1], m[2], t))

    db.commit()
    db.close()

# ─────────────────────────── Login / Logout ──────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if not valid_email(email):
            flash("Enter a valid email address.", "danger")
            return render_template("login.html")

        db = get_db()
        member_row = db.execute(
            "SELECT full_name FROM members WHERE LOWER(email)=?", (email,)
        ).fetchone()

        if not member_row:
            flash("No account found with that email. Join a group first or create one.", "warning")
            return render_template("login.html")

        session["user_email"] = email
        session["user_name"]  = member_row["full_name"]
        session.modified = True

        next_url = request.args.get("next")
        flash(f"Welcome back, {member_row['full_name']}!", "success")
        return redirect(next_url or url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You've been logged out.", "success")
    return redirect(url_for("index"))

# ─────────────────────────── Routes ──────────────────────────────────────────

@app.route("/")
def index():
    db  = get_db()
    q   = request.args.get("q", "").strip()
    sub = request.args.get("subject", "").strip()
    tag = request.args.get("tag", "").strip()

    sql    = "SELECT * FROM study_groups WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR description LIKE ? OR tags LIKE ? OR organiser LIKE ?)"
        params += [f"%{q}%"] * 4
    if sub:
        sql += " AND subject=?"
        params.append(sub)
    if tag:
        sql += " AND tags LIKE ?"
        params.append(f"%{tag}%")
    sql += " ORDER BY created_at DESC"

    rows     = db.execute(sql, params).fetchall()
    subjects = db.execute(
        "SELECT DISTINCT subject FROM study_groups ORDER BY subject"
    ).fetchall()

    groups = []
    for row in rows:
        groups.append({
            **dict(row),
            "member_count": member_count(db, row["id"]),
            "pending_count": pending_count(db, row["id"]),
        })

    return render_template("index.html",
        groups=groups, subjects=subjects,
        query=q, subject_filter=sub, tag_filter=tag)


@app.route("/group/<int:gid>")
def group_detail(gid):
    db    = get_db()
    group = db.execute("SELECT * FROM study_groups WHERE id=?", (gid,)).fetchone()
    if not group:
        abort(404)

    mc      = member_count(db, gid)
    pc      = pending_count(db, gid)
    members = db.execute(
        "SELECT * FROM members WHERE group_id=? ORDER BY role DESC, joined_at", (gid,)
    ).fetchall()
    announcements = db.execute(
        "SELECT * FROM announcements WHERE group_id=? ORDER BY posted_at DESC", (gid,)
    ).fetchall()
    top_posts = db.execute(
        "SELECT * FROM discussions WHERE group_id=? AND parent_id IS NULL ORDER BY posted_at DESC",
        (gid,)
    ).fetchall()
    replies_raw = db.execute(
        "SELECT * FROM discussions WHERE group_id=? AND parent_id IS NOT NULL ORDER BY posted_at",
        (gid,)
    ).fetchall()
    replies = {}
    for r in replies_raw:
        replies.setdefault(r["parent_id"], []).append(dict(r))

    # Show admin link only to the actual organiser
    is_organiser = (
        current_user() and
        current_user().lower() == group["contact_email"].lower()
    )

    return render_template("group_detail.html",
        group=dict(group), mc=mc, pc=pc,
        members=members, announcements=announcements,
        top_posts=top_posts, replies=replies,
        is_organiser=is_organiser)


@app.route("/group/<int:gid>/discuss", methods=["POST"])
def post_discussion(gid):
    db    = get_db()
    group = db.execute("SELECT id FROM study_groups WHERE id=?", (gid,)).fetchone()
    if not group:
        abort(404)

    author    = request.form.get("author", "").strip()
    email     = request.form.get("email", "").strip()
    message   = request.form.get("message", "").strip()
    parent_id = request.form.get("parent_id") or None

    errors = []
    if len(author) < 2:
        errors.append("Name must be at least 2 characters.")
    if not valid_email(email):
        errors.append("Enter a valid email address.")
    if len(message) < 5:
        errors.append("Message must be at least 5 characters.")

    if errors:
        for e in errors:
            flash(e, "danger")
        return redirect(url_for("group_detail", gid=gid) + "#discuss")

    db.execute("""
        INSERT INTO discussions (group_id,author,email,message,parent_id,posted_at)
        VALUES (?,?,?,?,?,?)
    """, (gid, author, email, message, parent_id, ts()))
    db.commit()
    flash("Your message has been posted.", "success")
    return redirect(url_for("group_detail", gid=gid) + "#discuss")


@app.route("/group/<int:gid>/join", methods=["GET", "POST"])
def join_group(gid):
    db    = get_db()
    group = db.execute("SELECT * FROM study_groups WHERE id=?", (gid,)).fetchone()
    if not group:
        abort(404)

    mc = member_count(db, gid)

    if mc >= group["max_members"]:
        flash("This group is full and not accepting new members.", "warning")
        return redirect(url_for("group_detail", gid=gid))
    if group["status"] == "closed":
        flash("This group is currently closed to new members.", "warning")
        return redirect(url_for("group_detail", gid=gid))

    if request.method == "POST":
        full_name     = request.form.get("full_name", "").strip()
        email         = request.form.get("email", "").strip()
        student_id    = request.form.get("student_id", "").strip()
        year_of_study = request.form.get("year_of_study", "").strip()
        reason        = request.form.get("reason", "").strip()

        errors = []
        if len(full_name) < 3:
            errors.append("Full name must be at least 3 characters.")
        if not valid_email(email):
            errors.append("Enter a valid email address (e.g. name@college.edu).")
        if len(student_id) < 4:
            errors.append("Student ID must be at least 4 characters.")
        if not year_of_study:
            errors.append("Please select your year of study.")
        if len(reason) < 20:
            errors.append("Please write at least 20 characters explaining why you want to join.")

        if not errors:
            already_member = db.execute(
                "SELECT id FROM members WHERE group_id=? AND LOWER(email)=LOWER(?)",
                (gid, email)
            ).fetchone()
            if already_member:
                errors.append("This email address is already registered as a member of this group.")

            already_pending = db.execute(
                "SELECT id FROM join_requests WHERE group_id=? AND LOWER(email)=LOWER(?) AND status='pending'",
                (gid, email)
            ).fetchone()
            if already_pending:
                errors.append("A join request from this email is already pending approval. Please wait for the organiser to review it.")

            was_rejected = db.execute(
                "SELECT id FROM join_requests WHERE group_id=? AND LOWER(email)=LOWER(?) AND status='rejected'",
                (gid, email)
            ).fetchone()
            if was_rejected:
                errors.append("A previous join request from this email was rejected. Please contact the organiser directly.")

            mc_now = member_count(db, gid)
            if mc_now >= group["max_members"]:
                errors.append("Sorry, this group just became full. Please check back later.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("join.html",
                group=dict(group), mc=mc, form_data=request.form)

        db.execute("""
            INSERT INTO join_requests
              (group_id,full_name,email,student_id,year_of_study,reason,status,requested_at)
            VALUES (?,?,?,?,?,?,'pending',?)
        """, (gid, full_name, email, student_id, year_of_study, reason, ts()))
        db.commit()

        return redirect(url_for("success",
            action="requested", group_name=group["name"]))

    return render_template("join.html",
        group=dict(group), mc=mc, form_data={})


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name          = request.form.get("name", "").strip()
        subject       = request.form.get("subject", "").strip()
        description   = request.form.get("description", "").strip()
        location      = request.form.get("location", "").strip()
        schedule      = request.form.get("schedule", "").strip()
        max_members   = request.form.get("max_members", "").strip()
        organiser     = request.form.get("organiser", "").strip()
        contact_email = request.form.get("contact_email", "").strip()
        tags          = request.form.get("tags", "").strip()

        errors = []
        if len(name) < 3:
            errors.append("Group name must be at least 3 characters.")
        if not subject:
            errors.append("Please select a subject.")
        if len(description) < 20:
            errors.append("Description must be at least 20 characters.")
        if not location:
            errors.append("Location is required.")
        if not schedule:
            errors.append("Schedule is required.")
        if len(organiser) < 3:
            errors.append("Organiser name must be at least 3 characters.")
        if not valid_email(contact_email):
            errors.append("Enter a valid contact email address.")
        try:
            max_int = int(max_members)
            if not (2 <= max_int <= 50):
                errors.append("Max members must be between 2 and 50.")
        except ValueError:
            errors.append("Max members must be a valid number.")
            max_int = 0

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("create.html", form_data=request.form)

        db  = get_db()
        gid = db.execute("""
            INSERT INTO study_groups
              (name,subject,description,location,schedule,max_members,
               organiser,contact_email,tags,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (name, subject, description, location, schedule, max_int,
              organiser, contact_email, tags, ts())).lastrowid

        db.execute("""
            INSERT INTO members (group_id,full_name,email,student_id,role,joined_at)
            VALUES (?,?,?,?,?,?)
        """, (gid, organiser, contact_email, "ORGANISER", "organiser", ts()))

        db.execute("""
            INSERT INTO announcements (group_id,title,body,posted_at)
            VALUES (?,?,?,?)
        """, (gid, f"Welcome to {name}!",
              "The group is now live. Share this page with your classmates and start studying together!",
              ts()))
        db.commit()

        # Auto log them in as the organiser after creating
        session["user_email"] = contact_email.lower()
        session["user_name"]  = organiser
        session.modified = True

        return redirect(url_for("success", action="created", group_name=name))

    return render_template("create.html", form_data={})


# ─────────────────── Admin routes — organiser only ───────────────────────────

@app.route("/admin/<int:gid>")
def admin_panel(gid):
    require_organiser(gid)          # ← BLOCKS anyone who is not the organiser

    db    = get_db()
    group = db.execute("SELECT * FROM study_groups WHERE id=?", (gid,)).fetchone()

    pending  = db.execute(
        "SELECT * FROM join_requests WHERE group_id=? AND status='pending' ORDER BY requested_at",
        (gid,)
    ).fetchall()
    approved = db.execute(
        "SELECT * FROM join_requests WHERE group_id=? AND status='approved' ORDER BY requested_at DESC LIMIT 10",
        (gid,)
    ).fetchall()
    rejected = db.execute(
        "SELECT * FROM join_requests WHERE group_id=? AND status='rejected' ORDER BY requested_at DESC LIMIT 10",
        (gid,)
    ).fetchall()
    members  = db.execute(
        "SELECT * FROM members WHERE group_id=? ORDER BY role DESC, joined_at", (gid,)
    ).fetchall()
    mc = member_count(db, gid)

    return render_template("admin.html",
        group=dict(group), pending=pending,
        approved=approved, rejected=rejected,
        members=members, mc=mc)


@app.route("/admin/<int:gid>/approve/<int:rid>", methods=["POST"])
def approve_request(gid, rid):
    require_organiser(gid)          # ← BLOCKS anyone who is not the organiser

    db  = get_db()
    req = db.execute(
        "SELECT * FROM join_requests WHERE id=? AND group_id=?", (rid, gid)
    ).fetchone()
    if not req:
        abort(404)

    grp = db.execute("SELECT * FROM study_groups WHERE id=?", (gid,)).fetchone()
    mc  = member_count(db, gid)

    if mc >= grp["max_members"]:
        flash("Cannot approve — group is now full.", "warning")
        db.execute("UPDATE join_requests SET status='rejected' WHERE id=?", (rid,))
        db.commit()
        return redirect(url_for("admin_panel", gid=gid))

    db.execute("UPDATE join_requests SET status='approved' WHERE id=?", (rid,))
    db.execute("""
        INSERT INTO members (group_id,full_name,email,student_id,role,joined_at)
        VALUES (?,?,?,?,'member',?)
    """, (gid, req["full_name"], req["email"], req["student_id"], ts()))
    db.commit()
    flash(f"{req['full_name']} has been approved and added to the group.", "success")
    return redirect(url_for("admin_panel", gid=gid))


@app.route("/admin/<int:gid>/reject/<int:rid>", methods=["POST"])
def reject_request(gid, rid):
    require_organiser(gid)          # ← BLOCKS anyone who is not the organiser

    db  = get_db()
    req = db.execute(
        "SELECT * FROM join_requests WHERE id=? AND group_id=?", (rid, gid)
    ).fetchone()
    if not req:
        abort(404)

    db.execute("UPDATE join_requests SET status='rejected' WHERE id=?", (rid,))
    db.commit()
    flash(f"{req['full_name']}'s request has been rejected.", "danger")
    return redirect(url_for("admin_panel", gid=gid))


@app.route("/admin/<int:gid>/remove/<int:mid>", methods=["POST"])
def remove_member(gid, mid):
    require_organiser(gid)          # ← BLOCKS anyone who is not the organiser

    db = get_db()
    m  = db.execute("SELECT * FROM members WHERE id=? AND group_id=?", (mid, gid)).fetchone()
    if not m:
        abort(404)
    if m["role"] == "organiser":
        flash("Cannot remove the organiser.", "warning")
        return redirect(url_for("admin_panel", gid=gid))
    db.execute("DELETE FROM members WHERE id=?", (mid,))
    db.commit()
    flash(f"{m['full_name']} has been removed from the group.", "success")
    return redirect(url_for("admin_panel", gid=gid))


@app.route("/admin/<int:gid>/announce", methods=["POST"])
def post_announcement(gid):
    require_organiser(gid)          # ← BLOCKS anyone who is not the organiser

    db    = get_db()
    group = db.execute("SELECT id FROM study_groups WHERE id=?", (gid,)).fetchone()
    if not group:
        abort(404)

    title = request.form.get("title", "").strip()
    body  = request.form.get("body", "").strip()

    if not title or not body:
        flash("Both title and message are required.", "danger")
        return redirect(url_for("admin_panel", gid=gid))

    db.execute(
        "INSERT INTO announcements (group_id,title,body,posted_at) VALUES (?,?,?,?)",
        (gid, title, body, ts())
    )
    db.commit()
    flash("Announcement posted successfully.", "success")
    return redirect(url_for("admin_panel", gid=gid))


@app.route("/admin/<int:gid>/toggle-status", methods=["POST"])
def toggle_status(gid):
    require_organiser(gid)          # ← BLOCKS anyone who is not the organiser

    db    = get_db()
    group = db.execute("SELECT * FROM study_groups WHERE id=?", (gid,)).fetchone()
    if not group:
        abort(404)

    new_status = "closed" if group["status"] == "open" else "open"
    db.execute("UPDATE study_groups SET status=? WHERE id=?", (new_status, gid))
    db.commit()
    flash(f"Group is now {new_status}.", "success")
    return redirect(url_for("admin_panel", gid=gid))


# ─────────────────────────── Dashboard ───────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    logged_in_email = current_user()
    db    = get_db()
    email = logged_in_email or request.args.get("email", "").strip()
    result = None

    if email:
        if not valid_email(email):
            flash("Enter a valid email address.", "danger")
        else:
            my_groups = db.execute("""
                SELECT sg.*, m.role, m.joined_at as my_joined
                FROM study_groups sg
                JOIN members m ON sg.id = m.group_id
                WHERE LOWER(m.email)=LOWER(?)
                ORDER BY m.joined_at DESC
            """, (email,)).fetchall()

            my_requests = db.execute("""
                SELECT jr.*, sg.name as group_name, sg.subject
                FROM join_requests jr
                JOIN study_groups sg ON jr.group_id = sg.id
                WHERE LOWER(jr.email)=LOWER(?)
                ORDER BY jr.requested_at DESC
            """, (email,)).fetchall()

            my_organised = db.execute("""
                SELECT * FROM study_groups
                WHERE LOWER(contact_email)=LOWER(?)
                ORDER BY created_at DESC
            """, (email,)).fetchall()

            result = {
                "email": email,
                "my_groups": my_groups,
                "my_requests": my_requests,
                "my_organised": my_organised,
            }

    return render_template("dashboard.html",
        result=result,
        logged_in=bool(logged_in_email),
        user_name=session.get("user_name"))


@app.route("/success")
def success():
    return render_template("success.html",
        action=request.args.get("action", "created"),
        group_name=request.args.get("group_name", "the group"))


# ─────────────────────────── Error handlers ──────────────────────────────────

@app.errorhandler(403)
def forbidden(_):
    return render_template("404.html"), 403

@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(_):
    return render_template("404.html"), 500


# Makes current_user available in every template automatically
@app.context_processor
def inject_user():
    return {
        "current_user_email": current_user(),
        "current_user_name":  session.get("user_name"),
    }


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
