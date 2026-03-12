#Step 1: import libraries
from dotenv import load_dotenv #reads the .env
import os #obtains the .env credentials
import tweepy #interacts with the API

#Step 2: This function reads the .env and loads the variables included in there
load_dotenv()

#Step 3: we don't want our credentials to be visible, so we are telling our script to go to the .env and read what's in there
X_API_KEY= os.getenv("X_API_KEY")
X_API_SECRET= os.getenv("X_API_SECRET")
X_ACCESS_TOKEN= os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET= os.getenv("X_ACCESS_TOKEN_SECRET")
APP_MODE= os.getenv("APP_MODE")

if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
    print("There are credentials missing in the .env")
    exit()
    
print("Credentials loaded successfully")

#Step 4: Asking the user to write text and validate it
#Step 4.1: Write a function that validates the text
def text_validation(text):
    text = text.strip()
    
    if len(text) == 0:
        return False, "Text can't be empty"
    if len(text) < 1:
        return False, "Text can't have negative characters"
    if len(text) > 280:
        return False, f"Text is too long: {len(text)}. Text can't have more than 280 characters"

    return True, "Valid text"

#Step 4.2: Connect to the API
def api_connection():
    try:
        client = tweepy.Client(
            consumer_key = X_API_KEY,
            consumer_secret = X_API_SECRET,
            access_token = X_ACCESS_TOKEN,
            access_token_secret = X_ACCESS_TOKEN_SECRET
        )
        return client
    except Exception as e:
        print(f"Error when connecting with X API {e}")
        return None

def posting(client, text):
    try:
        response = client.create_tweet(text=text)
        return True, response.data
    
    except Exception as e:
        return False, str(e)
    
#Step 4.3: Main function
def main():
    text = input("Write your post: ")
    valid_post, message = text_validation(text)
    
    if not valid_post:
        print(f"Error. {message}")
        return
    print(f"Valid text. {len(text)} characters")
    print(f"Posting: {text}")
    
    confirmation = input("Are you sure you want to post this? (y/n): " )
    if confirmation.lower() == "n":
        print("Not posted")
        return
    
    #Connecting the API
    print("Connecting the API...")
    client = api_connection()
    
    if not client:
        print("Can't connect the API")
        return
    
    #Posting the post
    print("Posting...")
    success, result = posting(client, text)
    
    if success:
        print("Posted successfully")
        print(f"Post ID: {result["id"]}")
    else:
        print(f"Posting error: {result}")
    
if __name__ == "__main__":
    main()
    




