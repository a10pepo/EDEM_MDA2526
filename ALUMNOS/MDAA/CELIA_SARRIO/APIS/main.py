import os
from dotenv import load_dotenv
from topic_generator import generate_tweet
from validators import validate_post
from storage import load_data, save_data

load_dotenv()
MODE = os.getenv("APP_MODE", "development")

def main():
    print("🚀 X Post Publisher\n")
    print("Tópicos disponibles:")
    print("- technology")
    print("- programming")
    print("- education")
    print("- sports")
    print("- random\n")

    topic = input("Elige un tópico: ").strip().lower()
    tweet = generate_tweet(topic)

    validate_post(tweet)

    print("\n📄 Tweet generado:\n")
    print(tweet)

    confirm = input("\n¿Publicar este tweet? (y/n): ").lower()
    if confirm != "y":
        print("❌ Publicación cancelada")
        return

    published = load_data("published.json")

    if MODE == "development":
        published.append({
            "content": tweet,
            "mode": "development"
        })
        save_data("published.json", published)
        print("\n🧪 MODO DEVELOPMENT: tweet guardado localmente")
        return

    from x_client import publish_to_x

    try:
        post_id = publish_to_x(tweet)
        published.append({
            "content": tweet,
            "post_id": post_id,
            "mode": "production"
        })
        save_data("published.json", published)
        print(f"\n✅ Tweet publicado en X | ID: {post_id}")
    except Exception as e:
        print("❌ Error al publicar:", e)

if __name__ == "__main__":
    main()
