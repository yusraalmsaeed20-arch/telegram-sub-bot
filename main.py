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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # التحقق من الرابط
    if "instagram.com" in text:
        msg = await update.message.reply_text("⏳ جاري تحميل المقطع من الإنستغرام...")
        user_id = update.message.from_user.id
        output_template = f"vid_{user_id}.mp4"
        
        ydl_opts = {
            'outtmpl': output_template,
            'format': 'best',
            'quiet': True,
        }
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([text]))
            
            if os.path.exists(output_template):
                with open(output_template, 'rb') as video:
                    await update.message.reply_video(video=video, caption="✅ تم التنزيل بنجاح!")
                os.remove(output_template)
            else:
                await update.message.reply_text("❌ لم يتم العثور على الفيديو. تأكد من أن الرابط عام.")
            await msg.delete()
        except Exception as e:
            await update.message.reply_text("❌ فشل التحميل. الرابط قد يكون خاصاً.")
    else:
        await update.message.reply_text("يرجى إرسال رابط فيديو **إنستغرام** فقط.")

def main():
    threading.Thread(target=run_health_check_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()            downloaded_file in os.listdir('.'):
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
