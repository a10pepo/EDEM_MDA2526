# Entregable APIS Álvaro Giménez

The initial idea was to make a post using the restful api of twitter. Due to the recent payment restriction applied to the developer tools in twitter, I've chosen to make something similar with mastodon (another social media I didn't know before).

The core requirements are the following: 

Authenticate with the X API using valid credentials
Publish a post successfully (minimum 1 character, maximum 280 characters)
Handle errors gracefully (invalid credentials, rate limits, network errors)
Protect secrets - Use environment variables or secure configuration files
Include documentation - README with setup instructions

The project structure is the following: 

-For our application, we first create an account and acces the developer section, where we have to create a new api key allowing just the write feature (for this purpose we don't need to allow any more).

-Once we have created an api key we will see 3 params: application id, secret and access token. For the project, just using the api key generated we will be able to post the message.

-We then create a script to make the post, taking the api key as params and our message as body (in json format). In order to securize the api key, we are...
