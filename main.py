import os
import threading
import yt_dlp
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

TOKEN = os.getenv('BOT_TOKEN', '8335419718:AAHADQsTY_dn5U-s0BcfLWAQiVOUSkM10us')
CHANNEL_USERNAME = '@aabaq22'

async def is_user_subscribed(bot, user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking sub: {e}")
        return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    text = update.message.text
    if "instagram.com" in text:
        msg = await update.message.reply_text("⏳ جاري تحضير وتنزيل المقطع، انتظر لحظة...")
        file_path = f"video_{user_id}.mp4"
        
        ydl_opts = {
            'outtmpl': file_path,
            'format': 'mp4/best',
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([text])
            
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video, caption="✅ تم التنزيل بنجاح!")
            
            await msg.delete()
        except Exception as e:
            await update.message.reply_text("❌ عذراً، فشل تنزيل المقطع. تأكد من أن الحساب عام والرابط صحيح.")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    else:
        await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو من إنستغرام لتحميله.")

def main():
    threading.Thread(target=run_health_check_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
