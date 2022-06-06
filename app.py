import logging
from multiprocessing.dummy import Array
import os
from anyio import Any # Save token details in another file
import telegram
from dotenv import load_dotenv
from telegram import Update, ParseMode, ForceReply
from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    CallbackContext
)

import praw
from unidecode import unidecode

logging.basicConfig( 
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # asctime: Time format, returns timestamp up to milisecond 
    # name: Name of the logger
    # levelname: Log severity
    # message: Log cause
    level = logging.INFO # Shows notifications for severity info and above 
) 
logger = logging.getLogger(__name__) # Create the first logger instance 

load_dotenv("./.env")
TELEGRAM_TOKEN = os.getenv("telegramToken")
REDDIT_CLIENT_ID = os.getenv("redditClientId")
REDDIT_SECRET = os.getenv("redditSecret")
REDDIT_USER_AGENT = os.getenv("redditUserAgent")

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued.

    Args:
        update (Update): _description_
        context (CallbackContext): _description_
    """
    startMsg = "Which subreddit would you like to visit today?"
    update.message.reply_text(startMsg)

def getTopComments(sub: Any) -> list:
    """Returns a list of the top three comments of the input submission.

    Args:
        sub (Any): A Submission object, representing a Reddit submission

    Returns:
        list: [ 
            (commentScore, commentBody)
        ]
    """
    commentsList = []
    print("comments preprocessed list", sub.comments[:3])
    for comment in sub.comments[:3]:
        score = comment.score
        body = unidecode(comment.body)
        commentsList.append((score, body))
    
    return commentsList

    
def getTeleMsg(sub: Any) -> str:
    """ Returns a Telegram message containing information on the input Reddit submission.

    Args:
        sub (Any): A Submission object, representing a Reddit submission

    Returns:
        str: A Tegram message with the following format

        {hyperlinked title}
        by {author}
        🠕 {upvotesNo}, {upvoteRatio} Upvotes

        {Submission body}

        # For 3 comments
        💬 🠕 {commentScore} 
        {Comment body}

    """
    title = sub.title
    author = sub.author.name
    commentsNo = sub.num_comments
    upvotesNo, upvoteRatio = sub.score, sub.upvote_ratio
    subUrl= sub.url
    comments = getTopComments(sub)
    print("subUrl", subUrl)
    msgList= []

    titleMsg = f"<a href='{subUrl}'> {title} </a>"
    authorMsg = f"by u\{author}"
    statsMsg = f" \U0001F815 {upvotesNo}, {upvoteRatio * 100}% Upvoted \U0001F4AC {commentsNo}" #\U0001F815 
    bodyMsg = unidecode(sub.selftext)
    msgList= [titleMsg, authorMsg, statsMsg, "\n", bodyMsg] 
    
    for comment in comments:
        print("comment", comment)
        commentMsg = f"\n \U0001F4AC \U0001F815 {comment[0]} \n {comment[1]}" 
        # open("log", "w").write(comment[1])
        msgList.append(commentMsg) 

    msg = "\n".join(msgList)

    return msg


def getRedditPosts(update: Update, context: CallbackContext) -> None:
    """ Initialises a Reddit PRAW instance, and sends a message containing information from a subreddit.

    Args:
        update (Update): _description_
        context (CallbackContext): _description_
    """
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_SECRET, user_agent=REDDIT_USER_AGENT)
    message = update.message.text
    subreddit = "all" if message == "." else message
    # print("subreddit", subreddit)
    submissions = reddit.subreddit(subreddit).hot(limit=3)
    # submissions = next(x for x in reddit.subreddit(subreddit).hot(limit=3) if not x.stickied)
    # print("submissions", submissions)

    for sub in submissions:
        # print("sub", sub)
        message = getTeleMsg(sub)
        # print("Message generated")
        update.message.reply_text(message, parse_mode=ParseMode.HTML) # parse_mode=ParseMode.MARKDOWN_V2 HTML

    return 

def error_handling(update: Update, context: CallbackContext) -> None:
    """Logs all errors or message caused by updates.

    Args:
        update (Update): _description_
        context (CallbackContext): _description_
    """

    logger.warning("Update '%s' caused error '%s'", update, context)
    
def main():
    updater = Updater(TELEGRAM_TOKEN)  # Create the updater: Pass in bot's token to init bot 
    
    dispatcher = updater.dispatcher # Init dispatcher to register the different handlers 
    dispatcher.add_handler(CommandHandler("start", start)) # Add message command -> /start
    dispatcher.add_handler(MessageHandler(Filters.text, getRedditPosts)) # Add message handler

    dispatcher.add_error_handler(error_handling)# # Add error handler 
    updater.start_polling() # Start running bot 
    updater.idle() # Run the bot until Ctl-C is pressed 

if __name__ == "__main__":
    main()