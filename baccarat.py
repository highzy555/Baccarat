import discord
from discord.ext import commands
import random
from flask import Flask, render_template
from threading import Thread
from dotenv import load_dotenv
app = Flask('')
@app.route('/')
def home():
  return "bot python is online!"
def index():
  return render_template("index.html")
def run():
  app.run(host='0.0.0.0', port=8080)
def high():
  t = Thread(target=run)
  t.start()

bot = commands.Bot(
    command_prefix='!',
    help_command=None,
    intents=discord.Intents.all(),
    strip_after_prefix=True,
    case_insensitive=True, 
)
bot_key = os.environ['bot']
token = bot_key
high()

@bot.command()
async def baccarat(ctx):
    player_hand = []
    banker_hand = []
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # List of card values

    # Deal initial cards
    for _ in range(2):
        player_hand.append(random.choice(deck))
        banker_hand.append(random.choice(deck))
        deck.remove(player_hand[-1])
        deck.remove(banker_hand[-1])

    # Calculate hand values (hidden from the user)
    player_total = sum([card if card < 10 else 0 for card in player_hand]) % 10
    banker_total = sum([card if card < 10 else 0 for card in banker_hand]) % 10

    # Draw additional cards based on the rules (hidden from the user)
    while player_total < 8:
        player_hand.append(random.choice(deck))
        player_total = sum([card if card < 10 else 0 for card in player_hand]) % 10
        deck.remove(player_hand[-1])

    while banker_total < 8 and banker_total < player_total:
        banker_hand.append(random.choice(deck))
        banker_total = sum([card if card < 10 else 0 for card in banker_hand]) % 10
        deck.remove(banker_hand[-1])

    # Determine the winner
    if player_total > banker_total:
        winner = "เพลเยอร์"
    elif player_total < banker_total:
        winner = "แบงค์เกอร์"
    else:
        winner = "เสมอ"

    # Create an Embed message without showing the hands and totals
    embed = discord.Embed(title="**Baccarat Game**", description="**ให้ทายว่าฝั่งไหนจะชนะ\nระหว่าง __เพลเยอร์__ หรือ __แบงค์เกอร์__ และ __เสมอ__**",color=0x00ff00)

    # Ask for the user's guess
    await ctx.send(embed=embed)
    await ctx.send("** # __ให้เวลาทาย 30วิ__ **")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except:
        await ctx.send("หมดเวลาการทาย เกิน30วิ แล้วครับ")
        return

    user_guess = msg.content.lower()

    if user_guess == winner.lower():
        result = "คุณทายถูก✅"
    else:
        result = f"คุณทายผิด ฝั่งที่ชนะคือ {winner}"

    # Add the hands and totals to the Embed message
    embed.add_field(name="แต้มของเพลเยอร์", value=", ".join(str(card) for card in player_hand) + f" (แต้มรวม: {player_total})", inline=False)
    embed.add_field(name="แต้มของแบงค์เกอร์", value=", ".join(str(card) for card in banker_hand) + f" (แต้มรวม: {banker_total})", inline=False)
    embed.add_field(name="ผลลัพธ์", value=result, inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1179255248787873953/1235275778267152496/1663773122628.jpg?ex=6633c7b7&is=66327637&hm=608409e5436a52e229331f6232217371d04f09afeed6d28212d96c0fe68acc78&")
    embed.set_footer(text="Baccarat Game",icon_url='https://cdn.discordapp.com/attachments/1179255248787873953/1235275778267152496/1663773122628.jpg?ex=6633c7b7&is=66327637&hm=608409e5436a52e229331f6232217371d04f09afeed6d28212d96c0fe68acc78&')
    await ctx.send(embed=embed)

bot.run(token)