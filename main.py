import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import os
import sys

# Token kontrolü
TOKEN = os.environ.get('MTUyMDcxMzM5NjIyMjMwMDI0MA.GiM0Ac.5yFKe4kW8Ef2l-rD6LDxYbcSL5iuhG47mTD6d4')
if not TOKEN:
    print("HATA: DISCORD_TOKEN çevresel değişkeni bulunamadı!")
    sys.exit(1)

# Bot kurulumu
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Veritabanını kontrol et
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, bakiye INTEGER DEFAULT 0, ses_suresi INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()
    
    await bot.tree.sync()
    print(f'Bot {bot.user} ismiyle başarıyla giriş yaptı ve hazır!')

@bot.tree.command(name="bakiye", description="Cüzdanındaki Jaster-Coin miktarını gösterir.")
async def bakiye(interaction: discord.Interaction):
    user_id = interaction.user.id
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    
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

# Botu çalıştır
if __name__ == "__main__":
    bot.run(TOKEN)
