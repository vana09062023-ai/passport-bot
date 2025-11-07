import discord
from discord.ext import commands
import random
import json
import os

# --- НАСТРОЙКИ ---
HELPER_ROLE_ID = 1389535976967114762  # ID роли хелпера
DATA_FILE = "passports.json"  # файл для хранения паспортов

# --- НАСТРОЙКА БОТА ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- ЗАГРУЗКА ПАСПОРТОВ ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        passports = json.load(f)
else:
    passports = {}

# --- СОБЫТИЕ ЗАПУСКА ---
@bot.event
async def on_ready():
    game = discord.Game("Ri Blox Studio")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'✅ Бот {bot.user} запущен и готов к выдаче паспортов!')

# --- КОМАНДА ВЫДАЧИ ПАСПОРТА ---
@bot.command()
async def паспорт(ctx):
    # Проверяем, есть ли у пользователя нужная роль
    if not any(role.id == HELPER_ROLE_ID for role in ctx.author.roles):
        await ctx.reply("❌ У вас нет доступа к этой команде.")
        return

    # Проверяем, что сообщение — это ответ
    if not ctx.message.reference:
        await ctx.reply("⚠️ Ответьте на сообщение пользователя, чтобы выдать паспорт.")
        return

    # Получаем сообщение, на которое ответил хелпер
    replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    target_user = replied_message.author

    # Проверяем, есть ли у пользователя паспорт
    if str(target_user.id) in passports:
        await ctx.reply(f"📄 У {target_user.mention} уже есть паспорт с ID: {passports[str(target_user.id)]}")
        return

    # Генерируем случайный 4-значный ID
    passport_id = random.randint(1000, 9999)
    passports[str(target_user.id)] = passport_id

    # Сохраняем в файл
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(passports, f, ensure_ascii=False, indent=4)

    # Бот отвечает, что паспорт выдан
    await ctx.reply(f"🪪 Паспорт выдан человеку {target_user.mention} `{passport_id}`")

    # Добавляем реакцию ✅ хелперу
    await ctx.message.add_reaction("✅")

# --- КОМАНДА ПРОСМОТРА ПАСПОРТА ---
@bot.command(name="pass")
async def show_passport(ctx, member: discord.Member = None):
    if member is None:
        await ctx.reply("⚠️ Укажите пользователя: `!pass @username`")
        return

    user_id = str(member.id)
    if user_id in passports:
        await ctx.reply(f"🪪 ID пользователя {member.mention}: `{passports[user_id]}`")
    else:
        await ctx.reply(f"❌ У пользователя {member.mention} нет паспорта.")

# --- ЗАПУСК БОТА ---
bot.run("MTQzNjM3MDAwMDg5MjkyMzkyNQ.G8hTyL.12vOzF81Qe7bsJbi1x2VWEUFv53vqGw8TOr-ak")
