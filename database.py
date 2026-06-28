import sqlite3

def init_db():
    # banka.db dosyası yoksa oluşturur, varsa bağlanır
    conn = sqlite3.connect('banka.db')
    cursor = conn.cursor()
    
    # Kullanıcılar tablosunu oluşturuyoruz
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, 
                       bakiye INTEGER DEFAULT 0, 
                       ses_suresi INTEGER DEFAULT 0)''')
    
    conn.commit()
    conn.close()
    print("Veritabanı başarıyla oluşturuldu!")

if __name__ == "__main__":
    init_db()