import os
import threading
import asyncio
import yt_dlp
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8335419718:AAF_ue96U84RiEScXTBQmjHFN6evECcgREg'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: 
        return
    text = update.message.text.strip()
    
    if text.startswith("http://") or text.startswith("https://"):
        msg = await update.message.reply_text("⏳ جاري تحميل المقطع...")
        u_id = update.message.from_user.id
        output_tmpl = f"vid_{u_id}.%(ext)s"
        
        ydl_opts = {
            'outtmpl': output_tmpl,
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([text]))
            
            f_name = next((f for f in os.listdir('.') if f.startswith(f"vid_{u_id}")), None)
            if f_name:
                with open(f_name, 'rb') as v:
                    await update.message.reply_video(video=v, caption="✅ تم التحميل بنجاح!")
                os.remove(f_name)
            else:
                await update.message.reply_text("❌ لم يتم العثور على الفيديو.")
            await msg.delete()
        except Exception:
            await update.message.reply_text("❌ فشل التحميل.")
    else:
        await update.message.reply_text("أهلاً بك! أرسلي لي رابط فيديو لتحميله.")

def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
