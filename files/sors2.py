from pyrubi import Client as Xpythondev
from pyrubi.types import Message

client = Xpythondev("TenTa")

JoinE = {
    "link": "https://rubika.ir/@gameingeom",
    "guid": "c0CcOSt05c61a8c78ca9d6bcfe47eff8"
}

def is_user_joined(user_guid):
    return client.check_join(object_guid=JoinE["guid"], user_guid=user_guid)

@client.on_message()
def LaKi(message: Message):
    if message.is_user:
        if not is_user_joined(message.author_guid):
            message.reply(f"""**👋 سلام دوست عزیز!

❌ **شما هنوز عضو کانال نیستید. خواهشمندیم ابتدا به کانال زیر بپیوندید:

1⃣** @@channel ✦@@({JoinE["link"]})

😊 منتظر حضور شما هستیم!
@gameingeom""")
            return
        else:
            message.reply(f"✅ شما عضو کانال شدید! به ربات خوش آمدید! هر سوالی دارید بپرسید.")

client.run()