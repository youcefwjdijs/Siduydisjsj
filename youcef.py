import requests
import telebot

# Replace with your actual bot token
BOT_TOKEN = '7753706778:AAGykg8kHGv3OI_UMLSDkipnVVGM7rovf3E'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name or "صديقي"
    welcome_message = (
        f"أهلاً بك يا {user_first_name}! 👋\n\n"
        "أنا بوت فحص حالة تبنيد لاعبي فري فاير.\n\n"
        "لاستخدامي، أرسل الأمر /check متبوعًا بمعرف اللاعب (UID).\n"
        "مثال: `/check 123456789`\n\n"
        "سأقوم بفحص حالة التبنيد للاعب وعرض المعلومات لك."
    )
    bot.reply_to(message, welcome_message, parse_mode='Markdown')

@bot.message_handler(commands=['check'])
def check_ban_status(message):
    try:
        # Extract UID from the message
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "الرجاء إدخال معرف اللاعب (UID) بعد الأمر /check. مثال: `/check 123456789`", parse_mode='Markdown')
            return
        
        uid = parts[1]
        
        # Construct the API URL
        api_url = f"https://scromnyi.vercel.app/region/ban-info?uid={uid}"
        
        # Make the API request
        response = requests.get(api_url )
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        
        data = response.json()
        
        # Check if the response contains expected data
        if not data or "ban_status" not in data:
            bot.reply_to(message, "❌ لم يتم العثور على معلومات لهذا اللاعب أو أن الـ API لم يعد بيانات صحيحة.")
            return

        # Extracting information
        nickname = data.get("nickname", "غير متوفر")
        ban_status = data.get("ban_status", "غير متوفر")
        ban_period = data.get("ban_period", "غير متوفر")
        region = data.get("region", "غير متوفر")
        
        # Format the message based on ban status
        if ban_status == "Not banned":
            status_emoji = "✅"
            status_text = "غير مبند"
            period_info = ""
        else:
            status_emoji = "❌"
            status_text = "مبند"
            period_info = f"\n⏱️ **مدة التبنيد:** `{ban_period}`" if ban_period else ""

        message_text = (
            f"✨ **حالة اللاعب:** ✨\n"
            f"---------------------------\n"
            f"🆔 **المعرف (UID):** `{uid}`\n"
            f"📛 **الاسم:** `{nickname}`\n"
            f"🌍 **المنطقة:** `{region}`\n"
            f"{status_emoji} **الحالة:** `{status_text}`{period_info}\n"
            f"---------------------------"
        )
        
        bot.reply_to(message, message_text, parse_mode='Markdown')
        
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء الاتصال بالـ API: {e}")
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ غير متوقع: {e}")

# Start polling for messages
print("Bot is running...")
bot.polling(none_stop=True)
