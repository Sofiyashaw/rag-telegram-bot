from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rag import retrieve, generate_answer, summarize_text
# Lara - 8741515350:AAGiZSgbYgCib67_Dmn3qxD1arg6_Ij1WwU
# Sofi - 8021770693:AAF667Qr3lC2_bZ_-P4Pc0kc2U7uG0jsbGI
TOKEN = "8021770693:AAF667Qr3lC2_bZ_-P4Pc0kc2U7uG0jsbGI"

# 🔹 Store last 3 interactions per user
user_history = {}

# 🔹 Store last response for summarize
last_response = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot is running ✅\nUse /ask <question>\nUse /summarize"
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "Please provide a question.\nExample: /ask What is Python?"
        )
        return

    query = " ".join(context.args)
    print(f"User query: {query}")

    # 🔹 Retrieve docs (with source names)
    retrieved = retrieve(query)

    context_text = "\n".join([doc for doc, _ in retrieved])
    sources = [name for _, name in retrieved]

    # 🔹 Add history (last 3)
    history_text = ""
    if user_id in user_history:
        history_text = "\n".join(user_history[user_id])

    full_context = history_text + "\n" + context_text

    answer = generate_answer(query, full_context)

    # 🔹 Save history (max 3)
    user_history.setdefault(user_id, []).append(f"Q: {query}\nA: {answer}")
    user_history[user_id] = user_history[user_id][-3:]

    # 🔹 Save last response for summarize
    last_response[user_id] = answer

    await update.message.reply_text(
        f"{answer}\n\n---\nSources: {', '.join(sources)}"
    )


async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in last_response:
        await update.message.reply_text("No previous response to summarize.")
        return

    summary = summarize_text(last_response[user_id])

    await update.message.reply_text(f"Summary:\n{summary}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/ask <question>\n/summarize\n/help"
    )


print("Starting Telegram Bot...")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("summarize", summarize))
app.add_handler(CommandHandler("help", help_command))

print("RUN COMPLETED ✅ Bot is live...")

app.run_polling()