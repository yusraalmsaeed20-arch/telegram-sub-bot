import os, asyncio, yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '8335419718:AAFiqjaMYJr3VyxiL3QlYLPVUZJ2Bq48PdE'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip() if update.message else ""
    if "instagram.com" in text:
        msg = await update.message.reply_text("⏳ جاري تحميل المقطع...")
        u_id = update.message.from_user.id
        ydl_opts = {'outtmpl': f'v_{u_id}.%(ext)s', 'format': 'best', 'quiet': True}
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([text]))
            f_name = next((f for f in os.listdir('.') if f.startswith(f"v_{u_id}")), None)
            if f_name:
                with open(f_name, 'rb') as v: await update.message.reply_video(video=v, caption="✅ تم!")
                os.remove(f_name)
            else: await update.message.reply_text("❌ الفيديو غير موجود أو الحساب خاص.")
            await msg.delete()
        except Exception: await update.message.reply_text("❌ فشل التحميل.")
    else: await update.message.reply_text("أرسلي رابط إنستغرام فقط.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__': main()        
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
