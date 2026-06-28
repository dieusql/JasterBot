import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

# Botun yetkilerini tanımlıyoruz
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} sisteme giriş yaptı ve komutlar senkronize edildi!')

# Bakiye komutu: Veritabanından veriyi çeker
@bot.tree.command(name="bakiye", description="Cüzdanındaki Jaster-Coin miktarını gösterir.")
async def bakiye(interaction: discord.Interaction):
    user_id = interaction.user.id
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    
    # Kullanıcıyı kontrol et, yoksa 0 bakiye ile ekle
    cursor.execute("SELECT bakiye FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute("INSERT INTO users (user_id, bakiye) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        bakiye = 0
    else:
        bakiye = row[0]
        
    await interaction.response.send_message(f"💰 Cüzdanında **{bakiye} Jaster-Coin** var!")
    conn.close()

# Token'ını buraya gir!
token = os.environ.get('MTUyMDcxMzM5NjIyMjMwMDI0MA.GiM0Ac.5yFKe4kW8Ef2l-rD6LDxYbcSL5iuhG47mTD6d4')
if __name__ == "__main__":
    bot.run(token)
