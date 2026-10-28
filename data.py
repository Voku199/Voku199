"""Veškerý obsah profilu. Uprav tady a spusť `python build.py`."""

USER = "Voku199"
NAME = "Vojtěch Kurinec"
HANDLE = "voku"
LOCATION = "Czechia"
PORTFOLIO = "https://voku199.github.io/Portfolio/"

# Rotující konec věty "I build …" v hlavičce (max ~40 znaků, ať se vejde)
ROTATING = [
    "web apps for real laser-game arenas",
    "Minecraft plugins for my friends' SMP",
    "WebXR games for the Quest 3",
    "small tools that run my day",
]

NOW = "liteclip — a 50 MB replay buffer for games"

ABOUT = (
    "Student from Czechia who ships things people actually use. "
    "Most of it is Python and Flask, plus a bit of Java, JavaScript and three.js "
    "whenever an idea needs it. Two laser-game arenas run their bookings on my code, "
    "my school parliament votes in my app, and my friends fight with my plugin's weapons."
)

# Ručně ověřená fakta, která skript nespočítá
FACTS = [
    ("2", "laser-game arenas on my code"),
    ("1", "hackathon, Bakix built in a day"),
]

ACHIEVEMENTS = [
    "Built the booking + stats site for a **real laser-game arena** in České Budějovice and a second one for STARDOMS Domažlice (replacing their WordPress).",
    "Shipped **Bakix**, an AI study assistant on top of Bakaláři with OAuth and Stripe Premium, at a vibe-coding hackathon (19 May 2026).",
    "Wrote **LID**, the app my school parliament uses for ideas and secret ballots.",
    "Made a **WebXR laser-game** for the Quest 3 where you move by walking on the spot.",
]

# link=None -> karta není klikací (soukromé repo)
PROJECTS = [
    {
        "name": "CB Lasergame",
        "line": "Live site for a real arena: bookings, Laserforce stats, three-tier admin.",
        "tags": ["Flask", "SQLite", "Resend"],
        "link": None,
    },
    {
        "name": "Bakix",
        "line": "AI study assistant for Czech students on top of Bakaláři.",
        "tags": ["Flask", "OAuth", "Stripe"],
        "link": "https://bakix.cz",
    },
    {
        "name": "VR Lasergame",
        "line": "Deathmatch vs 6 bots on Quest 3. Walk on the spot to move.",
        "tags": ["WebXR", "three.js", "Flask"],
        "link": None,
    },
    {
        "name": "Mythicals",
        "line": "Paper plugin: 8 one-per-server weapons, 3 lives, a secret Death Note.",
        "tags": ["Java", "Paper", "Gradle"],
        "link": None,
    },
    {
        "name": "liteclip",
        "line": "Replay buffer: F8 saves the last 30 s, one click sends it to Discord.",
        "tags": ["Python", "ffmpeg", "NVENC"],
        "link": None,
    },
    {
        "name": "LID",
        "line": "School parliament app: ideas, secret ballots, a public board.",
        "tags": ["Flask", "SQLite", "PDF.js"],
        "link": None,
    },
]

# Složky monorepa, které se do statistik nepočítají (kopie, cizí kód)
EXCLUDE = ["vr-lasergame-v2", "Keylogging", "hacksandbox"]

LINKS = [
    ("Portfolio", PORTFOLIO),
    ("Bakix", "https://bakix.cz"),
    ("Email", "mailto:vojta.kurinec@gmail.com"),
]
