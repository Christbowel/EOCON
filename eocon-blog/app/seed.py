import hashlib
import secrets


def hash_password(password):
    salt = "eocon"
    return hashlib.sha256((salt + password).encode()).hexdigest()


def seed_database(db):
    cursor = db.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        return

    admin_pw = secrets.token_urlsafe(32)

    users = [
        ("orgateam", "orga@eocon.local", hash_password(admin_pw), "admin",
         secrets.token_hex(24)),
        ("speaker_mk", "mk@eocon.local", hash_password(secrets.token_urlsafe(20)),
         "author", secrets.token_hex(24)),
        ("trainer_dv", "dv@eocon.local", hash_password(secrets.token_urlsafe(20)),
         "author", secrets.token_hex(24)),
        ("attendee01", "attendee01@eocon.local",
         hash_password(secrets.token_urlsafe(20)), "reader", None),
    ]
    for u in users:
        db.execute(
            "INSERT INTO users (username, email, password_hash, role, api_token) "
            "VALUES (?, ?, ?, ?, ?)", u
        )

    posts = [
        ("EOCON 2026: Where Africa Secures the Digital Future",
         "eocon-2026-secure-the-future",
         "EOCON 2026, 7th edition, is an annual bilingual cybersecurity convention "
         "held at Hotel Onomo in Douala, Cameroon. Available both on-site and online, "
         "EOCON brings together Africa, the diaspora and the global cybersecurity "
         "community around expert talks, technical workshops, strategic panels and "
         "the EyesOpenCTF. Whether you attend on-site in Douala or online from Paris, "
         "Montreal, Lagos or London, the convention is a gateway to opportunities, "
         "collaborations, careers and business partnerships in cybersecurity. This "
         "edition expects 1000+ attendees, 35+ expert speakers from 15+ countries, "
         "building on a 91% satisfaction rate from previous years.",
         1, "published", "img/cover-schedule.avif", "2026-06-15 09:00:00"),
        ("EyesOpenCTF: 48 Hours, 8 Disciplines, 40+ Challenges",
         "eyesopenctf-2026",
         "The EyesOpenCTF is a 48-hour Capture The Flag competition open to teams "
         "worldwide, held before the main conference and open to all registered "
         "participants. Teams of one to two players compete across eight disciplines: "
         "binary exploitation (PWN), web application security, digital forensics, "
         "cryptography, log analysis, AI security, reverse engineering and OSINT. "
         "With 40+ challenges and over 10,000 points up for grabs, participants "
         "register a team, receive operator access credentials, solve challenges "
         "to recover Reality Fragments, then unlock the evolving story and climb "
         "the leaderboard. Flags follow the format EOCON{...}.",
         1, "published", "img/cover-ctf.avif", "2026-06-20 14:00:00"),
        ("Call for Speakers: Share Your Expertise, Shape the Future",
         "call-for-speakers-2026",
         "EOCON 2026 is accepting talk proposals until September 30, 2026. Topics "
         "of interest include offensive security and red teaming, threat intelligence "
         "and hunting, cloud and infrastructure security, AI in cybersecurity, digital "
         "forensics and incident response, application and API security, OT/ICS/SCADA "
         "security, privacy and data protection, governance risk and compliance, "
         "emerging threats in Africa, open source security tools, and cybersecurity "
         "awareness and culture. Talk formats range from lightning talks of 10 to 15 "
         "minutes, standard talks of 30 to 50 minutes, workshops up to 2 hours, and "
         "panel discussions of 60 to 80 minutes.",
         2, "published", "img/cover-keynote.avif", "2026-07-01 10:00:00"),
        ("Workshops: Learn by Doing",
         "workshops-learn-by-doing",
         "EOCON workshops offer hands-on technical training led by industry experts. "
         "Spots are limited and registration is recommended early. Workshop sessions "
         "run up to two hours and cover practical skills that participants can apply "
         "immediately. Past editions have included sessions on penetration testing "
         "methodologies, secure code review, container security, and incident response "
         "playbook development. The hands-on format ensures that every participant "
         "leaves with concrete techniques rather than just theory. Detailed workshop "
         "titles and schedules will be announced as speakers are confirmed.",
         2, "published", "img/cover-fuzzing.avif", "2026-07-10 11:30:00"),
        ("Hotel Onomo, Douala: Your EOCON 2026 Venue",
         "venue-hotel-onomo-douala",
         "EOCON 2026 takes place at Hotel Onomo on Boulevard de la Liberte in Douala, "
         "Cameroon. The modern 4-star hotel offers conference facilities, high-speed "
         "WiFi and excellent accessibility. Douala is Cameroon's economic capital and "
         "a central African hub, making it an ideal location for a pan-African "
         "cybersecurity event. Douala International Airport (DLA) is about 10 minutes "
         "by taxi from the venue. Taxis and ride-sharing services are readily available "
         "in the city. Special hotel rates are offered to EOCON attendees with a "
         "booking code available on request from the organising team.",
         1, "published", "img/cover-reverse.avif", "2026-07-18 09:00:00"),
        ("Volunteer at EOCON 2026: Build the Future From the Inside",
         "volunteer-eocon-2026",
         "EOCON relies on volunteers to deliver a world-class experience. Volunteers "
         "receive free conference access, an exclusive volunteer T-shirt, networking "
         "opportunities, an official EOCON certificate, priority access to workshops, "
         "and behind-the-scenes experience of a major cybersecurity event. Available "
         "roles include Registration Team, Session Support covering moderation and "
         "speaker assistance both on-site and online, CTF Support helping build "
         "challenges and assist participants, Media and Social coverage, Sponsoring "
         "Ambassador for sponsor prospecting, and Logistics handling venue setup, "
         "internet and audio configuration.",
         3, "published", "img/cover-webapp.avif", "2026-07-25 15:00:00"),
        ("Understanding Taint Analysis: Tracing Data from Source to Sink",
         "taint-analysis-source-to-sink",
         "Taint analysis is a fundamental technique in application security research. "
         "The method tracks user-controlled data from its entry point, the source, "
         "through the application logic until it reaches a potentially dangerous "
         "function, the sink. Common sources include HTTP request parameters, file "
         "uploads, and database reads. Dangerous sinks include functions like eval, "
         "exec, SQL query builders, and OS command executors. Static analysis tools "
         "such as CodeQL and Semgrep automate source-to-sink tracing across multiple "
         "files and function boundaries. Manual triage with grep remains effective "
         "for rapid first passes on unfamiliar codebases. Mastering this workflow is "
         "essential for anyone working in vulnerability research or secure code review.",
         3, "published", "img/cover-homelab.webp", "2026-08-02 08:00:00"),
        ("Draft: Sponsors and Partners",
         "draft-sponsors-and-partners",
         "EOCON sponsors reach 1000+ cybersecurity professionals, decision-makers, "
         "researchers and students from 15+ countries, both in person and online. "
         "Sponsorship packages and details are available in the sponsorship deck. "
         "Confirmed sponsors will be announced on the main site.",
         1, "draft", None, "2026-08-10 10:00:00"),
    ]
    for p in posts:
        db.execute(
            "INSERT INTO posts (title, slug, body, author_id, status, cover_image, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)", p
        )

    tags = [
        ("eocon", "eocon"),
        ("ctf", "ctf"),
        ("talks", "talks"),
        ("2026", "2026"),
        ("security", "security"),
        ("workshops", "workshops"),
        ("venue", "venue"),
        ("volunteer", "volunteer"),
        ("research", "research"),
    ]
    for t in tags:
        db.execute("INSERT INTO tags (name, slug) VALUES (?, ?)", t)

    categories = [
        ("Conference", "conference"),
        ("Training", "training"),
        ("Community", "community"),
    ]
    for c in categories:
        db.execute("INSERT INTO categories (name, slug) VALUES (?, ?)", c)

    post_tags = [
        (1, 1), (1, 4),
        (2, 1), (2, 2), (2, 4),
        (3, 3), (3, 1),
        (4, 6), (4, 1),
        (5, 7), (5, 1),
        (6, 8), (6, 1),
        (7, 5), (7, 9),
    ]
    for pt in post_tags:
        db.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", pt)

    post_categories = [
        (1, 1), (2, 1), (3, 1), (4, 2), (5, 1), (6, 3), (7, 2)
    ]
    for pc in post_categories:
        db.execute(
            "INSERT INTO post_categories (post_id, category_id) VALUES (?, ?)", pc
        )

    comments = [
        (1, "cyber_jay", "91% satisfaction rate is impressive. Registering now."),
        (1, "douala_local", "Great to see a world-class cybersec event in Cameroon."),
        (2, "ctf_squad", "48 hours and 8 disciplines, our team is ready."),
        (2, "osint_fan", "OSINT + AI security as CTF disciplines is a nice touch."),
        (3, "appsec_speaker", "Submitted a proposal on API security, fingers crossed."),
        (3, "red_team_ops", "Offensive security and red teaming track sounds great."),
        (4, "blue_teamer", "Hands-on is the only way to learn incident response."),
        (5, "travel_hacker", "DLA is well connected, easy to get to Onomo from the airport."),
        (6, "volunteer_2025", "Volunteered last year, the networking alone was worth it."),
        (7, "codeql_user", "Source to sink tracing with CodeQL changed my workflow entirely."),
    ]
    for c in comments:
        db.execute(
            "INSERT INTO comments (post_id, author_name, body) VALUES (?, ?, ?)", c
        )

    settings_data = [
        ("site_name", "EOCON Blog"),
        ("tagline", "Secure the Future"),
        ("per_page", "10"),
        ("allow_comments", "true"),
        ("maintenance_mode", "false"),
    ]
    for s in settings_data:
        db.execute("INSERT INTO settings (key, value) VALUES (?, ?)", s)

    snippets = [
        ("header",
         "<header><h1>EOCON Blog</h1><nav>About | CTF | Workshops | Speakers</nav></header>"),
        ("footer",
         "<footer><p>EyesOpen Security Association</p></footer>"),
    ]
    for s in snippets:
        db.execute("INSERT INTO snippets (name, content) VALUES (?, ?)", s)

    db.commit()
