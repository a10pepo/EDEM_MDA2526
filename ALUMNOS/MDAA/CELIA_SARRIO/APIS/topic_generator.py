import random
from datetime import datetime

TOPICS = {
    "technology": [
        "Technology keeps evolving and shaping the future.",
        "Innovation in tech is changing how we live and work.",
        "Staying updated with technology is key in today's world."
    ],
    "programming": [
        "Programming is not just code, it's problem solving.",
        "Clean code makes future maintenance easier.",
        "Learning programming opens endless opportunities."
    ],
    "education": [
        "Education is the foundation of personal growth.",
        "Learning never stops, even outside the classroom.",
        "Education empowers people to build a better future."
    ],
    "sports": [
        "Sports teach discipline, teamwork, and perseverance.",
        "Every match is a new opportunity to improve.",
        "Sports bring people together beyond competition."
    ],
    "random": [
        "Small steps every day lead to big results.",
        "Consistency is more important than motivation.",
        "Progress comes from learning and adapting."
    ]
}

def generate_tweet(topic: str) -> str:
    if topic not in TOPICS:
        topic = "random"

    base = random.choice(TOPICS[topic])
    timestamp = datetime.now().strftime("%Y-%m-%d")

    return f"{base} ({timestamp})"
