# Entregable APIS Álvaro Giménez

The initial idea was to make a post using the RESTful API of Twitter. Due to the recent payment restrictions applied to the developer tools in Twitter, I have chosen to make something similar using Mastodon (another social media platform that I did not know before).

The core requirements are the following:

Authenticate with the MASTODON  API using valid credentials
Publish a post successfully (minimum 1 character, maximum 280 characters)
Handle errors gracefully (invalid credentials, rate limits, network errors)
Protect secrets - Use environment variables or secure configuration files
Include documentation - README with setup instructions

# Project structure is the following:

For this application, we first create an account and access the developer section of a Mastodon instance, where we create a new application with write permissions, which are enough for the purpose of publishing posts.

Once the application is created, an access token is generated. This token is required to authenticate requests with the Mastodon API and allows the application to publish messages.

We then create a Python script to publish a post by sending an HTTP POST request to the Mastodon API. The message content is sent in JSON format in the request body.

In order to secure the access token, it is not hardcoded in the source code. Instead, an environment variable is created to store the token, and this variable is accessed from the main.py script at runtime.

# Config steps
To configure the project we will have to download the dependencies shown in requirements.txt. To do so execute the following command in the terminal "pip install -r requirements.txt"

You will have to store your mastodon api key as an environment variable. To do show execute the following command: export MASTODON_TOKEN="your api key"