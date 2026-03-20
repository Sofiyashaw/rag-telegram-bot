from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from services.chat_service import handle_query, summarize
from config import TOKEN
from utils.logger import log


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 RAG Bot is LIVE \n\n/ask <question>\n/summarize"
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a question.\nExample: /ask What is Python?"
        )
        return

    query = " ".join(context.args)
    user_id = update.effective_user.id

    log(f"User {user_id} asked: {query}")

    answer, sources = handle_query(user_id, query)

    await update.message.reply_text(
        f"{answer}\n\n---\nSources: {', '.join(sources)}"
    )


async def summarize_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    result = summarize(user_id)
    await update.message.reply_text(result)


# ENTRY POINT
log("Starting Telegram Bot...")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("summarize", summarize_cmd))

log("🚀 PIPELINE READY — Bot is live and accepting requests!")

app.run_polling()