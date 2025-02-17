from bale import Bot,Message,Update,MenuKeyboardButton,InputFile,MenuKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,LabeledPrice,CallbackQuery
from random import randint, choice
import string
import sqlite3
from json import loads, dumps

# database

users = {}

with sqlite3.connect('UserInfo.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, chat_id INTEGER, name TEXT, referrals TEXT, total_playes INTEGER, coin INTEGER)''')
    conn.commit()

with sqlite3.connect('GiftCode.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS codes(id INTEGER PRIMARY KEY, code_id TEXT, user_id INTEGER)''')
    conn.commit()

def add_user_to_db(chat_id, name):
    with sqlite3.connect('UserInfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,))
        fetch = cursor.fetchone()
        if fetch is None:
            cursor.execute('''INSERT INTO users(chat_id, name, referrals, total_playes, coin) VALUES (?, ?, ?, ?, ?)''', (chat_id, name, dumps([]), 0, 0))
            conn.commit()
            return True
        return False

def get_user_data(chat_id):
    with sqlite3.connect('UserInfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE chat_id = ?''', (chat_id,))
        fetch = cursor.fetchone()
        if fetch:
            return fetch

def edit_coins(chat_id):
    with sqlite3.connect('UserInfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT coin FROM users WHERE chat_id = ?''', (chat_id,))
        coins = cursor.fetchone()
        if coins:
            cursor.execute('''UPDATE users SET coin = ? WHERE chat_id = ?''', (coins[0] + 1, chat_id))
            conn.commit()

def zero_coins(chat_id):
    with sqlite3.connect('UserInfo.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT coin FROM users WHERE chat_id = ?''', (chat_id,))
        coins = cursor.fetchone()
        if coins:
            cursor.execute('''UPDATE users SET coin = ? WHERE chat_id = ?''', (0, chat_id))
            conn.commit()

def create_GiftCode(code_id, user_id):
    with sqlite3.connect('GiftCode.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO codes(code_id, user_id) VALUES (?, ?)''', (code_id, user_id))
        conn.commit()

def gen_random_code(length=8):
    char = string.ascii_letters + string.digits
    random_code = ''.join(choice(char) for _ in range(length))
    return random_code

# end database
x = input("pleas write your token bale bot = ")
bot = Bot(token=x) # your token

@bot.event 
async def on_ready():
    print(bot.user.username,"is Ready")

@bot.event
async def on_message(message:Message):
    if message.content == "/start" :
        if add_user_to_db(message.chat.id,message.author.first_name) == True:
            await message.reply("سلام برای اولین بار به رباتمون خوش اومدید")

        button  = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🎮بازی🎮",callback_data="game"),row=1)
        button.add(InlineKeyboardButton(text="🎁کد تخفیف🎁",callback_data="gift"),row=2)
        button.add(InlineKeyboardButton(text="👤حساب کاربری👤",callback_data="user"),row=4)
        await message.reply("😉بازی کن و کد تخفیف بگیر😉",components=button)


@bot.event
async def on_callback(callback:CallbackQuery):
    global users
    if str(callback.user.id) in users.keys() and users[str(callback.user.id)] == "gaming":
        return await callback.message.reply("you cannot interact with buttons while in game")
    if callback.data == "game":
        button2 = InlineKeyboardMarkup()
        button2.add(InlineKeyboardButton(text="🔙بازگشت 🔙",callback_data="back"))
        await callback.message.reply("بازی حدس عدد شروع شد🌹\nلطفا عدد بین 0 تا 100 حدس بزنید😉",components=button2)
        code = randint(0,100)
        print(code)
        def answer_checker(m: Message):
            return callback.user == m.author and bool(m.text)
        answer_obj: Message = await bot.wait_for('message', check=answer_checker)
        try:
            int(answer_obj.text)
        except Exception:
                await answer_obj.reply("پیام نباید شامل حروف شود!",components=button2)


        users[str(callback.user.id)] = "gaming"

        while True :
            if int(answer_obj.text) > code :
                await answer_obj.reply("عدد شما بزرگتر از عدد مدنظر است⬆️")
            elif int(answer_obj.text) < code:
                await answer_obj.reply("عدد شما کوچتر از عدد مدنظر است ⬇️")
            else:
                await answer_obj.reply("تبریک میگم برنده شدی و یک امتیاز به شما اضافه شد 🥳",components=button2)
                print(edit_coins(answer_obj.chat_id))
                del users[str(callback.user.id)]
                return
            def answer_checker(m: Message):
                return callback.user == m.author and bool(m.text)
            answer_obj: Message = await bot.wait_for('message', check=answer_checker)
@bot.event
async def on_callback(callback:CallbackQuery):
    if str(callback.user.id) in users.keys():
        return await callback.message.reply("you cannot interact with buttons while in game")
    
    if callback.data == "gift":
        button2 = InlineKeyboardMarkup()
        button2.add(InlineKeyboardButton(text="🔙بازگشت 🔙",callback_data="back"))
        if get_user_data(callback.user.id)[5] < 3:
            coin = get_user_data(callback.user.id)
            await callback.message.reply(f"تعداد سکه های شما کم می باشد\n\nبرای گرفتن کد تخفیف به 3 سکه نیاز مندید \n\nسکه های شما 🪙: {coin[5]}",components=button2)
        else:
            code = gen_random_code()
            create_GiftCode(code, callback.user.id)
            zero_coins(callback.user.id)
            await callback.message.reply(f'گیفت کد شما: {code}')


@bot.event
async def on_callback(callback:CallbackQuery):
    if str(callback.user.id) in users.keys():
        return await callback.message.reply("you cannot interact with buttons while in game")
    
    s = get_user_data(callback.user.id)
    if callback.data == "user":
        button2 = InlineKeyboardMarkup()
        button2.add(InlineKeyboardButton(text="🔙بازگشت 🔙",callback_data="back"))
        text = f'''\
🆔نام کاربری : {'@'+callback.user.username}
✅نام : {s[2]}
🪙سکه ها : {s[5]}
✴️چت آیدی : {s[1]}
'''
        await callback.message.reply(text,components=button2)
    
@bot.event
async def on_callback(callback:CallbackQuery):
    if callback.data == "back":
        if add_user_to_db(callback.message.chat.id,callback.message.author.first_name) == True:
            await callback.message.reply("سلام برای اولین بار به رباتمون خوش اومدید")

        button  = InlineKeyboardMarkup()
        button.add(InlineKeyboardButton(text="🎮بازی🎮",callback_data="game"),row=1)
        button.add(InlineKeyboardButton(text="🎁کد تخفیف🎁",callback_data="gift"),row=2)
        button.add(InlineKeyboardButton(text="👤حساب کاربری👤",callback_data="user"),row=4)
        await callback.message.reply("😉بازی کن و کد تخفیف بگیر😉",components=button)
    
bot.run()
