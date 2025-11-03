from typing import Final
from telegram import Update
from telegram.ext import *
import google.generativeai as genai

f = open('token.txt','r')
TOKEN: Final = f.read()
BOT_USERNAME: Final = '@goodxd_bot'
api_key = 'API_KEY'

#Fuction to generate the response through AI
def gemini_ai_response(text: str) -> str:
    genai.configure(api_key=api_key)
    gem = genai.GenerativeModel('gemini-pro')
    resp = gem.generate_content(text)
    if resp and hasattr(resp, 'text'):
        desired_text = resp.text
        return desired_text
    else:
        return 'Error: No response text found'




# Function to handle user responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hello! I am a Good bot nice to meet you'
    elif 'how are you' in processed:
        return 'I am fine! I am a bot though, what will happen to me lol!'
    elif 'what can you do' in processed:
        return 'Sorry, I dont do much now but I will be updated in few months or days.'
    elif 'i am bored' in processed:
        return ('Wait! You can check these YouTube channels if you are bored: \n1) Carryminati: you can check his old videos if there is no new video.\n2) Mr. Beast is also a good catch. \nThat\'s my suggestions, you can find more recommendations on YouTube.')
    elif 'you are a bot right' in processed:
        return 'So what do you think I am? 😉'
    else:
        return gemini_ai_response(processed)

# Command handlers
async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! I am a good bot. I can talk to your group members nicely.')

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('SO WHAT YOU NEED HELP :) ')

async def shut_command(update: Update, context: CallbackContext):
    await update.message.reply_text('Bye bye! Have a nice day or night whatever :0')

async def aimode_command(update: Update, context: CallbackContext):
    await update.message.reply_text('AI mode is already enabled. Type your message and I will respond with an AI-generated answer.')


# Function to handle incoming messages
async def handle_message(update: Update, context: CallbackContext):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# Error handler
async def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('shut', shut_command))
    app.add_handler(CommandHandler('aimode', aimode_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error)

    print("Polling....")
    app.run_polling(poll_interval=2)
