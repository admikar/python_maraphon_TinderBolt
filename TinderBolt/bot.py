from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *
async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "Main menu",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "Chat with GPT 🧠"
    })

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande": "Ариана Гранде 🔥",
        "date_robbie": "Марго Робби 🔥🔥",
        "date_zendaya": "Зендея     🔥🔥🔥",
        "date_gosling": "Райан Гослинг 😎",
        "date_hardy": "Том Харди   😎😎"
    })

async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Waiting answer.....")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context, "Good chose, Invite for 5 messages")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)

async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")

    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text, {
        "message_next": "Next message",
        "message_date": "Invite to date"
    })
    dialog.list.clear()

async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "Thinking about answer....")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)

async def profile(update, context):
    dialog.mode = "profile"
    text = load_message("profile")
    await send_photo(update, context, "profile")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "How old are you? ...")

async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["age"] = text
        await send_text(update, context, "What are your job? ...")
    elif dialog.count == 2:
        dialog.user["occupation"] = text
        await send_text(update, context, "What are your hobby? ...")
    elif dialog.count == 3:
        dialog.user["hobby"] = text
        await send_text(update, context, "What are you don't like in people? ...")
    elif dialog.count == 4:
        dialog.user["annoys"] = text
        await send_text(update, context, "What are your aim of meeting? ...")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("profile")
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "ChatGPT 🧠, thinking ... ")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)

async def opener(update, context):
    dialog.mode = "opener"
    text = load_message("opener")
    await send_photo(update, context, "opener")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Name of girl? ...")

async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, "How old girl? ...")
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, "Your view from 1 till 10? ...")
    elif dialog.count == 3:
        dialog.user["handsome"] = text
        await send_text(update, context, "Where are you work? ...")
    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, "Aim of meeting? ...")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("opener")
        user_info = dialog_user_info_to_str(dialog.user)
        answer = await chatgpt.send_question(prompt, user_info)
        await send_text(update, context, answer)




async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    if dialog.mode == "date":
        await date_dialog(update, context)
    if dialog.mode == "message":
        await message_dialog(update, context)
    if dialog.mode == "profile":
        await profile_dialog(update, context)
    if dialog.mode == "opener":
        await opener_dialog(update, context)
    else:
        await send_text(update, context, "*Hello!*")
        await send_text(update, context, "_How are you?_")
        await send_text(update, context, "Your message " + update.message.text)

        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Run process?", {
            "Run": "Running",
            "Stop": "Stopping"
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "Run":
        await send_text(update, context, "Process started.")
    else:
        await send_text(update, context, "Process stopped.")

dialog = Dialog()
dialog.mode = None
dialog.list = []
dialog.count = 0
dialog.user = {}

chatgpt = ChatGptService(token="XXXXX")

app = ApplicationBuilder().token("XXXXX").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
