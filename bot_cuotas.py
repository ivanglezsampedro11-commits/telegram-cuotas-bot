import os
import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 **Bot Picks**\n\n"
        "**Formato:**\n"
        "`partido / fecha / hora / pick / cuota / %éxito / %edge`\n\n"
        "**Ejemplo:**\n"
        "`barcelona - madrid / 11/01 / 20:00 / Gana Barcelona / 2.00 / 60% / +5.15%`"
    )

async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    lineas = texto.strip().split('\n')
    
    if not lineas:
        await update.message.reply_text("❌ Envía datos")
        return
    
    mensaje_parts = ["PICK DEL DIA:"]
    cuotas_total = 1.0
    
    for i, linea in enumerate(lineas, 1):
        # partido / fecha / hora / pick / cuota / %éxito / %edge
        patron = r'(.+?)\s*/\s*(\d{1,2}/\d{1,2})\s*/\s*(\d{1,2}:\d{2})\s*/\s*(.+?)\s*/\s*([\d.]+)\s*/\s*(\d+)%\s*/\s*([+-]?\d+\.?\d*)%'
        match = re.match(patron, linea.strip())
        
        if not match:
            await update.message.reply_text(f"❌ Error línea {i}: `{linea}`\nFormato: `partido / fecha / hora / pick / cuota / %éxito / %edge`")
            return
        
        partido, fecha, hora, pick, cuota_str, exito, edge = match.groups()
        
        try:
            cuota = float(cuota_str)
            cuotas_total *= cuota
        except:
            await update.message.reply_text(f"❌ Error cuota línea {i}")
            return
        
        # Formato EXACTO que pediste
        mensaje_parts.extend([
            "",
            f"- {partido.upper()}",
            f"- {hora}",
            f"- {pick.strip().upper()}",
            f"- ✅: {exito}%",
            f"- 📊: {edge}%"
        ])
    
    mensaje_parts.append(f"\nCUOTA CONJUNTA: {cuotas_total:.2f}")
    mensaje_final = '\n'.join(mensaje_parts)
    
    await update.message.reply_text(mensaje_final)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analizar))
    print("🤖 Bot iniciado")
    app.run_polling()

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8443))
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

    main()
