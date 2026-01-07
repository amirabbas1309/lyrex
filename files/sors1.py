import asyncio
from rubka.asynco import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json
import os
import random
import string
from pathlib import Path
from typing import Dict, List

DB_FILE = "user_data.json"
LOG_FILE = "chat_logs.json"
CODES_FILE = "coin_codes.json"
SERIAL_CODES_FILE = "serial_codes.json"
INTERNET_REQUESTS_FILE = "internet_requests.json"

bot = Robot(token="")
ADMIN_ID = ""
CREATOR_ID = ""

os.makedirs("profile_pics", exist_ok=True)

async def set_commands():
    print(await bot.set_commands(
        [
            {"command": "start", "description": "فعالسازی ربات"},
            {"command": "admin", "description": "پنل ادمین (مخصوص ادمین‌ها)"},
            {"command": "help", "description": "راهنمای استفاده از ربات"},
            {"command": "balance", "description": "موجودی و تراکنش‌ها"},
            {"command": "shop", "description": "فروشگاه سکه"},
            {"command": "serial", "description": "استفاده از کد سریال"},
            {"command": "internet", "description": "تبدیل موجودی به اینترنت"}
        ]
    ))

BTN_ROCK_PAPER_SCISSORS = "🪨 سنگ کاغذ قیچی"
BTN_DICE_GAME = "🎲 تاس"
BTN_WHEEL = "🎡 گردونه شانس"
BTN_BALANCE = "💰 موجودی"
BTN_SHOP = "🛍️ فروشگاه🎖"
BTN_SERIAL_CODE = "🔑 کد سریال"
BTN_HELP = "❓ راهنما"
BTN_INTERNET = "📱 تبدیل موجودی به اینترنت"

BTN_ROCK = "🪨 سنگ"
BTN_PAPER = "📄 کاغذ"
BTN_SCISSORS = "✂️ قیچی"
BTN_BACK = "🔙 بازگشت"

BTN_EVEN = "⚪ زوج"
BTN_ODD = "⚫ فرد"
BTN_DICE_BACK = "🔙 بازگشت"

BTN_BROADCAST = "📢 ارسال همگانی"
BTN_USER_COUNT = "👥 تعداد کاربران"
BTN_CREATE_SERIAL = "🔑 ساخت سریال"
BTN_MASS_CREDIT = "💳 افزایش اعتبار همگانی"
BTN_ADMIN_BACK = "🔙 بازگشت"

BTN_BUY_10K = "10,000 تومان ➜ 7,000"
BTN_BUY_20K = "20,000 تومان ➜ 15,000"
BTN_SHOP_BACK = "🔙 بازگشت"

BTN_1GB = "1 گیگ اینترنت - 10,000 تومان"
BTN_1_5GB = "1.5 گیگ اینترنت - 15,000 تومان"
BTN_INTERNET_BACK = "🔙 بازگشت"

DB = {
    "user_info": defaultdict(lambda: {
        "balance": 0,
        "today_profit": 0,
        "today_loss": 0,
        "last_activity": datetime.now().isoformat(),
        "wheel_last_spin": None,
        "transactions": []
    }),
    "serial_codes": {},
    "admin_codes": {},
    "internet_requests": {}
}

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(DB["user_info"], f, ensure_ascii=False, indent=4)
    
    with open(SERIAL_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(DB["serial_codes"], f, ensure_ascii=False, indent=4)
    
    with open(INTERNET_REQUESTS_FILE, "w", encoding="utf-8") as f:
        json.dump(DB["internet_requests"], f, ensure_ascii=False, indent=4)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                DB["user_info"].update(json.load(f))
            except:
                pass
    
    if os.path.exists(SERIAL_CODES_FILE):
        with open(SERIAL_CODES_FILE, "r", encoding="utf-8") as f:
            try:
                DB["serial_codes"].update(json.load(f))
            except:
                pass
    
    if os.path.exists(INTERNET_REQUESTS_FILE):
        with open(INTERNET_REQUESTS_FILE, "r", encoding="utf-8") as f:
            try:
                DB["internet_requests"].update(json.load(f))
            except:
                pass

def add_transaction(uid: str, amount: int, type: str, description: str):
    transaction = {
        "amount": amount,
        "type": type,
        "description": description,
        "timestamp": datetime.now().isoformat()
    }
    
    DB["user_info"][uid]["transactions"].append(transaction)
    
    if amount > 0:
        DB["user_info"][uid]["today_profit"] += amount
    else:
        DB["user_info"][uid]["today_loss"] += abs(amount)
    
    DB["user_info"][uid]["balance"] += amount
    save_db()

async def send_win_notification(uid: str, game_name: str, amount: int):
    user_info = DB["user_info"][uid]
    current_balance = user_info["balance"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    win_text = f"""
برد جدید🎖
🎮 بازی: {game_name}
💰 مبلغ اضافه شده: {amount:,} تومان
💎 موجودی کاربر: {current_balance:,} تومان
⏰ زمان: {time}
👤 کاربر: {uid}
"""
    
    try:
        await bot.send_message(CREATOR_ID, win_text)
        if ADMIN_ID != CREATOR_ID:
            await bot.send_message(ADMIN_ID, win_text)
    except Exception as e:
        print(f"خطا در ارسال اطلاعیه برد: {e}")

def reset_daily_stats():
    now = datetime.now()
    for uid, info in DB["user_info"].items():
        last_activity = datetime.fromisoformat(info["last_activity"])
        if (now - last_activity).days >= 1:
            info["today_profit"] = 0
            info["today_loss"] = 0
    save_db()

def generate_serial_code(amount: int) -> str:
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    DB["serial_codes"][code] = {
        "amount": amount,
        "used": False,
        "created_at": datetime.now().isoformat()
    }
    save_db()
    return code

async def send_main_menu(uid: str, text: str = "منوی اصلی:"):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="rps", text=BTN_ROCK_PAPER_SCISSORS))
    builder.row(builder.button(id="dice", text=BTN_DICE_GAME))
    builder.row(builder.button(id="wheel", text=BTN_WHEEL))
    builder.row(builder.button(id="balance", text=BTN_BALANCE))
    builder.row(builder.button(id="shop", text=BTN_SHOP))
    builder.row(builder.button(id="serial", text=BTN_SERIAL_CODE))
    builder.row(builder.button(id="internet", text=BTN_INTERNET))
    
    if uid in [ADMIN_ID, CREATOR_ID]:
        builder.row(builder.button(id="admin", text="🛠️ پنل مدیریت"))
    
    main_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, text, chat_keypad=main_keypad)

async def send_rps_menu(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="rock", text=BTN_ROCK))
    builder.row(builder.button(id="paper", text=BTN_PAPER))
    builder.row(builder.button(id="scissors", text=BTN_SCISSORS))
    builder.row(builder.button(id="back", text=BTN_BACK))
    
    rps_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "🎮 بازی سنگ کاغذ قیچی\n\n💰 هزینه بازی: 2,000 تومان\n\nانتخاب شما:", chat_keypad=rps_keypad)

async def send_dice_menu(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="even", text=BTN_EVEN))
    builder.row(builder.button(id="odd", text=BTN_ODD))
    builder.row(builder.button(id="dice_back", text=BTN_DICE_BACK))
    
    dice_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "🎲 بازی تاس\n\nشرط بندی روی زوج یا فرد بودن تاس\n\n💰 حداقل شرط: 10,000 تومان\n\nانتخاب شما:", chat_keypad=dice_keypad)

async def send_shop_menu(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="buy_10k", text=BTN_BUY_10K))
    builder.row(builder.button(id="buy_20k", text=BTN_BUY_20K))
    builder.row(builder.button(id="shop_back", text=BTN_SHOP_BACK))
    
    shop_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "🛍️ فروشگاه سکه\n\nلیست قیمت‌ها:", chat_keypad=shop_keypad)

async def send_internet_menu(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="1gb", text=BTN_1GB))
    builder.row(builder.button(id="1_5gb", text=BTN_1_5GB))
    builder.row(builder.button(id="internet_back", text=BTN_INTERNET_BACK))
    
    internet_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "📱 تبدیل موجودی به اینترنت\n\nبسته مورد نظر را انتخاب کنید:", chat_keypad=internet_keypad)

async def send_admin_menu(uid: str):
    builder = ChatKeypadBuilder()
    builder.row(builder.button(id="broadcast", text=BTN_BROADCAST))
    builder.row(builder.button(id="user_count", text=BTN_USER_COUNT))
    builder.row(builder.button(id="create_serial", text=BTN_CREATE_SERIAL))
    builder.row(builder.button(id="mass_credit", text=BTN_MASS_CREDIT))
    builder.row(builder.button(id="admin_back", text=BTN_ADMIN_BACK))
    
    admin_keypad = builder.build(resize_keyboard=True)
    await bot.send_message(uid, "🛠️ پنل مدیریت", chat_keypad=admin_keypad)

async def handle_rock_paper_scissors(uid: str, user_choice: str):
    user_balance = DB["user_info"][uid]["balance"]
    
    if user_balance < 2000:
        await bot.send_message(uid, "❌ موجودی شما برای بازی کافی نیست!\n💰 هزینه بازی: 2,000 تومان")
        return
    
    add_transaction(uid, -2000, "debit", "هزینه بازی سنگ کاغذ قیچی")
    
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    
    user_choice_text = ""
    bot_choice_text = ""
    
    if user_choice == "rock":
        user_choice_text = "🪨 سنگ"
    elif user_choice == "paper":
        user_choice_text = "📄 کاغذ"
    else:
        user_choice_text = "✂️ قیچی"
    
    if bot_choice == "rock":
        bot_choice_text = "🪨 سنگ"
    elif bot_choice == "paper":
        bot_choice_text = "📄 کاغذ"
    else:
        bot_choice_text = "✂️ قیچی"
    
    result_text = ""
    
    if user_choice == bot_choice:
        result_text = f"مساوی شدیم 🌚🗿\n\n🫵🏻تو = {user_choice_text}\n🤖ربات = {bot_choice_text}"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        add_transaction(uid, 5000, "credit", "برنده بازی سنگ کاغذ قیچی")
        result_text = f"هورا بردی ✅️🥳\n\n🫵🏻تو = {user_choice_text}\n🤖ربات = {bot_choice_text}\n\n🎁 جایزه: 5,000 تومان"
        await send_win_notification(uid, "سنگ کاغذ قیچی", 5000)
    else:
        result_text = f"ای وای باختی 😞💔\n\n🫵🏻تو = {user_choice_text}\n🤖ربات = {bot_choice_text}"
    
    await bot.send_message(uid, result_text)

async def handle_dice_game(uid: str, bet_type: str, bet_amount: int):
    user_balance = DB["user_info"][uid]["balance"]
    
    if bet_amount < 10000:
        await bot.send_message(uid, "❌ حداقل شرط 10,000 تومان است!")
        return
    
    if user_balance < bet_amount:
        await bot.send_message(uid, f"❌ موجودی شما کافی نیست!\n💰 موجودی فعلی: {user_balance:,} تومان")
        return
    
    add_transaction(uid, -bet_amount, "debit", f"شرط بازی تاس - {bet_type}")
    
    dice_roll = random.randint(1, 6)
    is_even = dice_roll % 2 == 0
    result_type = "زوج" if is_even else "فرد"
    
    result_text = f"🎲 نتیجه تاس: {dice_roll} ({result_type})\n\n"
    
    if (bet_type == "even" and is_even) or (bet_type == "odd" and not is_even):
        prize = 3000
        add_transaction(uid, prize, "credit", "برنده بازی تاس")
        result_text += f"✅ برنده شدید!\n💰 سود شما: {prize:,} تومان"
        await send_win_notification(uid, "بازی تاس", prize)
    else:
        result_text += f"❌ باختید!\n💸 مبلغ شرط از دست رفت"
    
    await bot.send_message(uid, result_text)

async def handle_wheel_spin(uid: str):
    user_balance = DB["user_info"][uid]["balance"]
    user_info = DB["user_info"][uid]
    
    if user_balance < 3000:
        await bot.send_message(uid, "❌ موجودی شما برای چرخاندن گردونه کافی نیست!\n💰 هزینه: 3,000 تومان")
        return
    
    if user_info.get("wheel_last_spin"):
        last_spin = datetime.fromisoformat(user_info["wheel_last_spin"])
        if (datetime.now() - last_spin).total_seconds() < 86400:
            await bot.send_message(uid, "⏰ شما امروز قبلاً گردونه را چرخانده‌اید!\n🕒 فردا دوباره امتحان کنید.")
            return
    
    add_transaction(uid, -3000, "debit", "هزینه چرخش گردونه")
    
    wheel_result = random.choices(
        [10000, 9000, 0],
        weights=[20, 15, 65],
        k=1
    )[0]
    
    user_info["wheel_last_spin"] = datetime.now().isoformat()
    
    result_text = "🎡 نتیجه گردونه شانس:\n\n"
    
    if wheel_result == 10000:
        add_transaction(uid, 10000, "credit", "برنده گردونه - 10,000 تومان")
        result_text += "🎉 مبلغ 10,000 تومان برنده شدید! 🎊"
        await send_win_notification(uid, "گردونه شانس", 10000)
    elif wheel_result == 9000:
        add_transaction(uid, 9000, "credit", "برنده گردونه - 9,000 تومان")
        result_text += "🎉 مبلغ 9,000 تومان برنده شدید! 🎊"
        await send_win_notification(uid, "گردونه شانس", 9000)
    else:
        result_text += "😞 متاسفانه این بار پوچ شدید!\n🍀 دفعه بعد شانس با شماست!"
    
    await bot.send_message(uid, result_text)
    save_db()

async def handle_serial_code(uid: str, code: str):
    code = code.upper().strip()
    
    if code in DB["serial_codes"] and not DB["serial_codes"][code]["used"]:
        amount = DB["serial_codes"][code]["amount"]
        DB["serial_codes"][code]["used"] = True
        add_transaction(uid, amount, "credit", f"استفاده از کد سریال: {code}")
        await bot.send_message(uid, f"✅ کد سریال معتبر!\n💰 مبلغ {amount:,} تومان به حساب شما اضافه شد.")
        save_db()
    else:
        await bot.send_message(uid, "❌ کد سریال نامعتبر یا قبلاً استفاده شده است!")

async def handle_internet_request(uid: str, package_type: str):
    user_balance = DB["user_info"][uid]["balance"]
    
    if package_type == "1gb":
        cost = 10000
        internet_amount = "1 گیگ"
    else:
        cost = 15000
        internet_amount = "1.5 گیگ"
    
    if user_balance < cost:
        await bot.send_message(uid, f"❌ موجودی شما کافی نیست!\n💰 هزینه: {cost:,} تومان\n💎 موجودی فعلی: {user_balance:,} تومان")
        return
    
    request_id = str(int(datetime.now().timestamp()))
    DB["internet_requests"][request_id] = {
        "user_id": uid,
        "package_type": package_type,
        "internet_amount": internet_amount,
        "cost": cost,
        "status": "pending",
        "timestamp": datetime.now().isoformat()
    }
    
    DB["user_info"][uid]["waiting_for"] = f"internet_info_{request_id}"
    save_db()
    
    await bot.send_message(uid, f"📱 درخواست {internet_amount} اینترنت\n\n💰 مبلغ: {cost:,} تومان\n\nلطفاً اطلاعات زیر را ارسال کنید:\n• شماره موبایل\n• ایدی اکانت\n\n(هر دو را در یک پیام ارسال کنید)")

async def process_internet_request(request_id: str, user_info_text: str):
    if request_id not in DB["internet_requests"]:
        return
    
    request = DB["internet_requests"][request_id]
    uid = request["user_id"]
    
    request_text = f"""
درخواست اینترنت جدید 📱

📦 مقدار اینترنت: {request['internet_amount']}
💰 مبلغ: {request['cost']:,} تومان
📞 شماره کاربر: {user_info_text}
👤 ایدی کاربر: {uid}
⏰ زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔑 کد درخواست: {request_id}

تایید درخواست با ارسال ✅ و لغو درخواست با ارسال ❌ انجام میشود
"""
    
    try:
        await bot.send_message(CREATOR_ID, request_text)
        if ADMIN_ID != CREATOR_ID:
            await bot.send_message(ADMIN_ID, request_text)
        
        await bot.send_message(uid, "✅ درخواست شما برای مدیریت ارسال شد. به زودی بررسی خواهد شد.")
    except Exception as e:
        await bot.send_message(uid, "❌ خطا در ارسال درخواست. لطفاً دوباره تلاش کنید.")
        print(f"خطا در ارسال درخواست اینترنت: {e}")

async def approve_internet_request(request_id: str):
    if request_id not in DB["internet_requests"]:
        return
    
    request = DB["internet_requests"][request_id]
    uid = request["user_id"]
    
    if request["status"] != "pending":
        return
    
    add_transaction(uid, -request["cost"], "debit", f"خرید اینترنت {request['internet_amount']}")
    
    request["status"] = "approved"
    request["approved_at"] = datetime.now().isoformat()
    save_db()
    
    await bot.send_message(uid, "با موفقیت انجام شد✅\n\n📦 اینترنت شما فعال شد!")
    
    if "waiting_for" in DB["user_info"][uid]:
        del DB["user_info"][uid]["waiting_for"]

async def reject_internet_request(request_id: str):
    if request_id not in DB["internet_requests"]:
        return
    
    request = DB["internet_requests"][request_id]
    uid = request["user_id"]
    
    if request["status"] != "pending":
        return
    
    request["status"] = "rejected"
    request["rejected_at"] = datetime.now().isoformat()
    save_db()
    
    await bot.send_message(uid, "❌ درخواست شما رد شد.")
    
    if "waiting_for" in DB["user_info"][uid]:
        del DB["user_info"][uid]["waiting_for"]

@bot.on_message()
async def message_handler(bot: Robot, msg: Message):
    uid = str(msg.chat_id)
    text = msg.text.strip() if msg.text else ""
    
    print(f"👤 کاربر با چت آیدی: {uid} پیام داد: {text}")
    
    if uid not in DB["user_info"]:
        DB["user_info"][uid]["balance"] = 0
        DB["user_info"][uid]["today_profit"] = 0
        DB["user_info"][uid]["today_loss"] = 0
        DB["user_info"][uid]["transactions"] = []
        save_db()
    
    DB["user_info"][uid]["last_activity"] = datetime.now().isoformat()
    
    user_state = DB["user_info"][uid].get("waiting_for", "")
    
    if uid in [ADMIN_ID, CREATOR_ID] and text in ["✅", "❌"]:
        for request_id, request in DB["internet_requests"].items():
            if request["status"] == "pending":
                if text == "✅":
                    await approve_internet_request(request_id)
                    await bot.send_message(uid, f"✅ درخواست {request_id} تایید شد.")
                else:
                    await reject_internet_request(request_id)
                    await bot.send_message(uid, f"❌ درخواست {request_id} رد شد.")
                return
    
    if user_state == "broadcast_message" and uid in [ADMIN_ID, CREATOR_ID]:
        DB["user_info"][uid]["waiting_for"] = ""
        users = list(DB["user_info"].keys())
        success = 0
        for user_id in users:
            try:
                await bot.send_message(user_id, f"📢 پیام همگانی:\n\n{text}")
                success += 1
                await asyncio.sleep(0.1)
            except:
                pass
        await bot.send_message(uid, f"✅ پیام به {success} کاربر ارسال شد.")
        return
    
    elif user_state == "dice_bet_amount":
        DB["user_info"][uid]["waiting_for"] = ""
        try:
            bet_amount = int(text.replace(",", "").replace("،", ""))
            bet_type = DB["user_info"][uid].get("dice_bet_type")
            if bet_type:
                await handle_dice_game(uid, bet_type, bet_amount)
        except ValueError:
            await bot.send_message(uid, "❌ لطفاً یک عدد معتبر وارد کنید!")
        return
    
    elif user_state == "serial_code_amount" and uid in [ADMIN_ID, CREATOR_ID]:
        DB["user_info"][uid]["waiting_for"] = ""
        try:
            amount = int(text.replace(",", "").replace("،", ""))
            code = generate_serial_code(amount)
            await bot.send_message(uid, f"✅ کد سریال ایجاد شد:\n\n🔑 کد: `{code}`\n💰 مبلغ: {amount:,} تومان")
        except ValueError:
            await bot.send_message(uid, "❌ لطفاً یک عدد معتبر وارد کنید!")
        return
    
    elif user_state == "mass_credit_amount" and uid in [ADMIN_ID, CREATOR_ID]:
        DB["user_info"][uid]["waiting_for"] = ""
        try:
            amount = int(text.replace(",", "").replace("،", ""))
            users_count = 0
            for user_id in DB["user_info"]:
                add_transaction(user_id, amount, "credit", f"افزایش اعتبار همگانی توسط مدیریت")
                users_count += 1
            await bot.send_message(uid, f"✅ مبلغ {amount:,} تومان به {users_count} کاربر اضافه شد.")
        except ValueError:
            await bot.send_message(uid, "❌ لطفاً یک عدد معتبر وارد کنید!")
        return
    
    elif user_state == "serial_code_input":
        DB["user_info"][uid]["waiting_for"] = ""
        await handle_serial_code(uid, text)
        return
    
    elif user_state.startswith("internet_info_"):
        request_id = user_state.replace("internet_info_", "")
        DB["user_info"][uid]["waiting_for"] = ""
        await process_internet_request(request_id, text)
        return
    
    if text == "/start" or text == BTN_BACK or text == BTN_ADMIN_BACK or text == BTN_SHOP_BACK or text == BTN_DICE_BACK or text == BTN_INTERNET_BACK:
        await send_main_menu(uid, "به منوی اصلی خوش آمدید! 🎮")
    
    elif text == BTN_ROCK_PAPER_SCISSORS:
        await send_rps_menu(uid)
    
    elif text == BTN_DICE_GAME:
        await send_dice_menu(uid)
    
    elif text == BTN_WHEEL:
        await handle_wheel_spin(uid)
    
    elif text == BTN_BALANCE or text == "/balance":
        user_info = DB["user_info"][uid]
        balance_text = f"""
لیـــــست تراکنــــش های امروز شــــما💵:

💰 مقدار سود: {user_info['today_profit']:,} تومان
💸 مقدار ضرر: {user_info['today_loss']:,} تومان
💎 اخرین موجودی شما: {user_info['balance']:,} تومان
"""
        await bot.send_message(uid, balance_text)
    
    elif text == BTN_SHOP or text == "/shop":
        await send_shop_menu(uid)
    
    elif text == BTN_SERIAL_CODE or text == "/serial":
        DB["user_info"][uid]["waiting_for"] = "serial_code_input"
        await bot.send_message(uid, "🔑 لطفاً کد سریال خود را وارد کنید:")
    
    elif text == BTN_INTERNET or text == "/internet":
        await send_internet_menu(uid)
    
    elif text == BTN_HELP or text == "/help":
        help_text = """
🎮 **راهنمای ربات بازی**

**🪨 سنگ کاغذ قیچی:**
- هزینه: 2,000 تومان
- جایزه برنده: 5,000 تومان

**🎲 بازی تاس:**
- حداقل شرط: 10,000 تومان
- سود برنده: 3,000 تومان

**🎡 گردونه شانس:**
- هزینه: 3,000 تومان
- هر 24 ساعت یکبار
- جوایز: 10,000، 9,000 تومان یا پوچ

**📱 تبدیل به اینترنت:**
- 1 گیگ: 10,000 تومان
- 1.5 گیگ: 15,000 تومان

**🛍️ فروشگاه:**
- خرید سکه با قیمت مناسب

**🔑 کد سریال:**
- استفاده از کدهای هدیه
"""
        await bot.send_message(uid, help_text)
    
    elif text in ["/admin", "admin"] and uid in [ADMIN_ID, CREATOR_ID]:
        await send_admin_menu(uid)
    
    elif text in [BTN_ROCK, BTN_PAPER, BTN_SCISSORS]:
        choice_map = {BTN_ROCK: "rock", BTN_PAPER: "paper", BTN_SCISSORS: "scissors"}
        await handle_rock_paper_scissors(uid, choice_map[text])
    
    elif text in [BTN_EVEN, BTN_ODD]:
        bet_type = "even" if text == BTN_EVEN else "odd"
        DB["user_info"][uid]["waiting_for"] = "dice_bet_amount"
        DB["user_info"][uid]["dice_bet_type"] = bet_type
        await bot.send_message(uid, f"💰 لطفاً مبلغ شرط خود را وارد کنید (حداقل 10,000 تومان):")
    
    elif text == BTN_BUY_10K:
        shop_text = """برای خرید سکه 10,000 تومانی به مبلغ 7,000 تومان لطفاً به شماره کارت زیر واریز کنید:

💳 شماره کارت:
5859831220064637

📸 سپس اسکرین شات را به این ایدی ارسال کنید:
@Samyar86gd"""
        await bot.send_message(uid, shop_text)
    
    elif text == BTN_BUY_20K:
        shop_text = """برای خرید سکه 20,000 تومانی به مبلغ 15,000 تومان لطفاً به شماره کارت زیر واریز کنید:

💳 شماره کارت:
5859831220064637

📸 سپس اسکرین شات را به این ایدی ارسال کنید:
@Samyar86gd"""
        await bot.send_message(uid, shop_text)
    
    elif text == BTN_1GB:
        await handle_internet_request(uid, "1gb")
    
    elif text == BTN_1_5GB:
        await handle_internet_request(uid, "1.5gb")
    
    elif text == BTN_BROADCAST and uid in [ADMIN_ID, CREATOR_ID]:
        DB["user_info"][uid]["waiting_for"] = "broadcast_message"
        await bot.send_message(uid, "📢 لطفاً پیام همگانی خود را وارد کنید:")
    
    elif text == BTN_USER_COUNT and uid in [ADMIN_ID, CREATOR_ID]:
        user_count = len(DB["user_info"])
        await bot.send_message(uid, f"👥 تعداد کاربران ربات: {user_count} نفر")
    
    elif text == BTN_CREATE_SERIAL and uid in [ADMIN_ID, CREATOR_ID]:
        DB["user_info"][uid]["waiting_for"] = "serial_code_amount"
        await bot.send_message(uid, "💰 لطفاً مبلغ کد سریال را وارد کنید (مثلاً 20000):")
    
    elif text == BTN_MASS_CREDIT and uid in [ADMIN_ID, CREATOR_ID]:
        DB["user_info"][uid]["waiting_for"] = "mass_credit_amount"
        await bot.send_message(uid, "💰 لطفاً مبلغ افزایش اعتبار را وارد کنید (مثلاً 10000):")

async def main():
    load_db()
    await set_commands()
    
    asyncio.create_task(daily_reset_task())
    
    print("🤖 ربات بازی در حال اجرا است...")
    print(f"👑 ادمین: {ADMIN_ID}")
    print(f"👤 سازنده: {CREATOR_ID}")
    print(f"👥 تعداد کاربران: {len(DB['user_info'])}")
    
    await bot.run()

async def daily_reset_task():
    while True:
        await asyncio.sleep(3600)
        reset_daily_stats()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ خروج از برنامه...")
        save_db()
        print("💾 اطلاعات ذخیره شد.")
        print("👋 خداحافظ!")