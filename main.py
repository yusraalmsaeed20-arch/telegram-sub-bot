import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# التوكن الجديد المباشر
TOKEN = os.getenv('BOT_TOKEN', '8335419718:AAFiqjaMYJr3VyxiL3QlYLPVUZJ2Bq48PdE')
CHANNEL_USERNAME = '@aabaq22'

async def is_user_subscribed(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking sub: {e}")
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
        
    user_id = update.message.from_user.id
    subscribed = await is_user_subscribed(context.bot, user_id)
    
    if not subscribed:
        channel_link = f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
        keyboard = [[InlineKeyboardButton("📢 اشترك في القناة أولاً من هنا", url=channel_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ عذراً! يجب عليك الاشتراك في القناة أولاً لاستخدام البوت.",
            reply_markup=reply_markup
        )
        return

    text = update.message.text.strip()
    
    if text.startswith("http://") or text.startswith("https://"):
        msg = await update.message.reply_text("⏳ جاري تحضير وتنزيل المقطع، انتظر لحظة...")
        file_name = f"vid_{user_id}.mp4"
        
        ydl_opts = {
            'outtmpl': file_name,
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([text]))
            
            if os.path.exists(file_name):
                with open(file_name, 'rb') as video:
                    await update.message.reply_video(video=video, caption="✅ تم التنزيل بنجاح!")
                os.remove(file_name)
            else:
                await update.message.reply_text("❌ لم يتم العثور على الملف بعد التحميل.")
            
            await msg.delete()
        except Exception as e:
            print(f"Error: {e}")
            await update.message.reply_text("❌ عذراً، فشل تنزيل المقطع. تأكد من أن الرابط صحيح والحساب عام.")
    else:
        await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو من (إنستغرام، فيسبوك، سناب شات، بينتريست، تيك توك) لتحميله.")

def main():
    threading.Thread(target=run_health_check_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
