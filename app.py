from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_ban_status():
    uid = request.form.get('uid')
    
    if not uid:
        return "الرجاء إدخال معرف اللاعب (UID)"
    
    try:
        api_url = f"https://scromnyi.vercel.app/region/ban-info?uid={uid}"
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or "ban_status" not in data:
            return render_template('result.html', error="❌ لم يتم العثور على معلومات لهذا اللاعب")
        
        player_info = {
            'uid': uid,
            'nickname': data.get("nickname", "غير متوفر"),
            'ban_status': "غير مبند ✅" if data["ban_status"] == "Not banned" else "مبند ❌",
            'ban_period': data.get("ban_period", "غير متوفر"),
            'region': data.get("region", "غير متوفر")
        }
        
        return render_template('result.html', player=player_info)
        
    except requests.exceptions.RequestException as e:
        return render_template('result.html', error=f"❌ خطأ في الاتصال بالخادم: {e}")
    except Exception as e:
        return render_template('result.html', error=f"❌ خطأ غير متوقع: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=2010)