import os
from pyrogram import Client, filters
import openai

# Set up your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Your Telegram API Credentials
api_id = YOUR_API_ID  # Get it from https://my.telegram.org
api_hash = "YOUR_API_HASH"
string_session = "YOUR_STRING_SESSION"

# Initialize the bot
bot = Client("assistant_bot", api_id=api_id, api_hash=api_hash, session_string=string_session)

@bot.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hey there! I'm your friendly AssistantBot. Aap mujhse kisi bhi cheez ke liye baat kar sakte hain!")

@bot.on_message(filters.text & filters.mentioned)
def mention_handler(client, message):
    user_message = message.text
    bot_name = client.get_me().username

    # Stripping the bot name from the message
    user_query = user_message.replace(f"@{bot_name}", "").strip()

    # Get a response from OpenAI if user query is not empty
    if user_query:
        response = get_openai_response(user_query)

        # Determine the response language based on the user's input
        if is_hinglish(user_query):
            message.reply_text(response)  # Assistant response in Hinglish if user is in Hinglish
        else:
            message.reply_text(response)  # Assistant response in English if user is in English

def is_hinglish(text):
    """A simple function to detect if the text is Hinglish."""
    # Checking for common Hindi words in the message
    hindi_words = ['hai', 'kya', 'aap', 'tum', 'main', 'na', 'se', 'ka', 'ke', 'bhi', 'toh', 'hain', 'par', 'aur', 'hoon', 'wo']

    # If the message contains a proportion of Hindi words, consider it Hinglish
    hindi_word_count = sum(word in text.lower() for word in hindi_words)
    return hindi_word_count > 0

def get_openai_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can replace it with the latest available model
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return "I'm sorry, I couldn't process your request right now. Please try again."

# Additional command for casual conversation
@bot.on_message(filters.text)
def chat_response(client, message):
    user_message = message.text.strip()

    # Ignore messages from the bot itself
    if message.from_user.id == client.get_me().id:
        return

    # Get a response from OpenAI
    if user_message:
        response = get_openai_response(user_message)
        # Similar detection of response language
        if is_hinglish(user_message):
            message.reply_text(response)  # Assistant responds in Hinglish
        else:
            message.reply_text(response)  # Assistant responds in English

if __name__ == "__main__":
    bot.run()