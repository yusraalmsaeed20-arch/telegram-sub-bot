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

TOKEN = '8335419718:AAFiqjaMYJr3VyxiL3QlYLPVUZJ2Bq48PdE'
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
        msg = await update.message.reply_text("⏳ جاري تحميل المقطع، انتظر لحظة...")
        output_template = f"vid_{user_id}.%(ext)s"
        
        ydl_opts = {
            'outtmpl': output_template,
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([text]))
            
            downloaded_file = None
            for file in os.listdir('.'):
                if file.startswith(f"vid_{user_id}"):
                    downloaded_file = file
                    break
            
            if downloaded_file and os.path.exists(downloaded_file):
                with open(downloaded_file, 'rb') as video:
                    await update.message.reply_video(video=video, caption="✅ تم التنزيل بنجاح!")
                os.remove(downloaded_file)
            else:
                await update.message.reply_text("❌ متعذر إيجاد الفيديو، تأكد من أن الرابط لحساب عام وليس خاصاً.")
            
            await msg.delete()
        except Exception as e:
            print(f"Download Error: {e}")
            await update.message.reply_text("❌ فشل تنزيل المقطع. تأكد أن الرابط يعمل وأن الحساب عام.")
    else:
        await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو لتحميله.")

def main():
    threading.Thread(target=run_health_check_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True, stop_signals=None)

if __name__ == '__main__':
    main()        ydl_opts = {
            'outtmpl': output_template,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([text]))
            
            # البحث عن الملف المنزل بغض النظر عن امتداده
            downloaded_file in os.listdir('.'):
                if file.startswith(f"vid_{user_id}"):
                    downloaded_file = file
                    break
            
            if downloaded_file and os.path.exists(downloaded_file):
                with open(downloaded_file, 'rb') as video:
                    await update.message.reply_video(video=video, caption="✅ تم التنزيل بنجاح!")
                os.remove(downloaded_file)
            else:
                await update.message.reply_text("❌ متعذر إيجاد الفيديو، تأكد من أن الرابط لحساب عام وليس خاصاً.")
            
            await msg.delete()
        except Exception as e:
            print(f"Download Error: {e}")
            await update.message.reply_text("❌ فشل تنزيل المقطع. تأكد أن الرابط يعمل وأن الحساب عام.")
    else:
        await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو لتحميله.")

def main():
    threading.Thread(target=run_health_check_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
