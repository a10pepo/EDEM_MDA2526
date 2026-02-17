import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_data(filename):
    file = DATA_DIR / filename
    if not file.exists():
        return []
    return json.loads(file.read_text())

def save_data(filename, data):
    file = DATA_DIR / filename
    file.write_text(json.dumps(data, indent=2))

def save_published_post(content, post_id=None):
    posts = load_data("published.json")
    posts.append({
        "content": content,
        "post_id": post_id,
        "published_at": datetime.now().isoformat()
    })
    save_data("published.json", posts)


