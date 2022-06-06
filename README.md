# About
Want to stop scrolling endlessly on Reddit? @RedditTop3Bot is here to help! View only the top Reddit posts and community responses on Telegram.

This Telegram bot returns the 3 hottest submission of a given subreddit, along with the top 3 comments for each submission.

# Installation

```
pip install -r requirements.txt
```

# Usage
## Creating an .env file 
Create an .env file in the project root directory with the following variables: 
- telegramToken
- redditClientId
- redditSecret
- redditUserAgent

Ensure that there are no spaces between the equation signs, as the spaces could be identified as characters that are part of the variable.

## Telegram 
1. Enter @Botfather in the search tab and select the verified account.
2. Choose or type the /newbot command and send it.
3. Follow the instructions sent by @Botfather. 
4. Copy the token under "Use this token to access the HTTP API:" 
5. Save the token in the .env file as telegramToken. 

Click [here](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot) for a guide with accompanying screenshots.

## Reddit 
1. Go to [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/) and log into Reddit.
2. Select "Create App" on the navigation bar. 
3. Complete the form. 
- For application type (Radio buttons), select "script". 
- For redirect URI, type: 127.0.0.1:8080

4. Save the following variables in the .env file. 
- Name of Reddit application: redditUserAgent
- Client Secret: redditSecret 
- Client ID: redditClientId

# Running the application 
``` 
python app.py
```


# References 
[Building a Reddit Autoposter Telegram Bot with Python](https://www.section.io/engineering-education/telegram-bot-python/)

