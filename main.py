import configparser
from telegram import Update, Bot
import time
from urllib.request import urlopen
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

dataPath = "../cacarankingbot-data/"

config = configparser.ConfigParser()
config.read(dataPath + "config.txt")
token = config["Telegram"]["token"]

def readData(chatId: str) -> configparser.ConfigParser:
    parser = configparser.ConfigParser()
    parser.read(dataPath + chatId)
    return parser

def increment(data: configparser.ConfigParser, chatId: str, userId: str, userName: str) -> None:
    if not data.has_section(userId):
        data.add_section(userId)
    data.set(userId, "name", userName)
    currentScore = int(data.get(userId, "score", fallback="0"))
    data.set(userId, "score", str(currentScore + 1))
    with open(dataPath + chatId, 'w') as file:
        data.write(file)

def beautifyData(data: configparser.ConfigParser) -> str:
    dataText = ""
    dataList: list[(str, int)] = []
    for section in data.sections():
        dataList.append((data[section]["name"], data[section]["score"]))
    dataList.sort(key=lambda x: x[1])
    for i in range(len(dataList)):
        dataText += f"{medal(i)} {dataList[i][0]} ({dataList[i][1]})\n"
    return dataText

def medal(position: int) -> str:
    if(position == 0):
        return "🥇"
    elif(position == 1):
        return "🥈"
    elif(position == 2):
        return "🥉"
    else:
        return "💩"


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chatId = str(update.effective_chat.id)
    userId = str(update.effective_user.id)
    userFullName = update.effective_user.full_name

    data = readData(chatId)
    increment(data, chatId, userId, userFullName)
    await update.message.reply_text(f"👏¡¡¡{userFullName} ha cagado!!!👏\n\nRanking actual:\n{beautifyData(data)}")
    
internet = False
while not internet:
    try:
        urlopen("http://www.google.com/").read()
        internet = True
    except Exception as e:
        print(e)
        time.sleep(1)
        pass

app = ApplicationBuilder().token(token).build()
app.add_handler(MessageHandler(filters.Regex("💩"), messageHandler, True))

print("Polling...")
app.run_polling()
