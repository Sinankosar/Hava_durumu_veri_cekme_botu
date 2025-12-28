import requests
from bs4 import BeautifulSoup
import mysql.connector

connector = mysql.connector.connect(
    host ="localhost",
    user="root",
    password = "mysql123",
    database ="hava_durumu"
    
)
cursor = connector.cursor()


citys = [
    "adana", "adıyaman", "afyonkarahisar", "ağrı", "amasya",
    "ankara", "antalya", "artvin", "aydın", "balıkesir",
    "bilecik", "bingöl", "bitlis", "bolu", "burdur",
    "bursa", "çanakkale", "çankırı", "çorum", "denizli",
    "diyarbakır", "edirne", "elazığ", "erzincan", "erzurum",
    "eskişehir", "gaziantep", "giresun", "gümüşhane", "hakkari",
    "hatay", "ısparta", "mersin", "istanbul", "izmir",
    "kars", "kastamonu", "kayseri", "kırklareli", "kırşehir",
    "kocaeli", "konya", "kütahya", "malatya", "manisa",
    "kahramanmaraş", "mardin", "muğla", "muş", "nevşehir",
    "niğde", "ordu", "rize", "sakarya", "samsun",
    "siirt", "sinop", "sivas", "tekirdağ", "tokat",
    "trabzon", "tunceli", "şanlıurfa", "uşak", "van",
    "yozgat", "zonguldak", "aksaray", "bayburt", "karaman",
    "kırıkkale", "batman", "şırnak", "bartın", "ardahan",
    "iğdır", "yalova", "karabük", "kilis", "osmaniye",
    "düzce"
]

try:
    city = input("Şehir giriniz: ").strip().lower()

    while city not in citys:
        city = input("Hatalı şehir girdiniz. Lütfen şehir giriniz: ").strip().lower()

    
    day = int(input("Kaç günlük veri istediğinizi giriniz (7,10,15,20,25,30,40,45,90) : "))
    while day not in [7, 10, 15, 20, 25, 30, 40, 45, 90]:
        day = int(input("Geçersiz gün sayısı girdiniz. Lütfen kaç günlük veri istediğinizi giriniz (7,10,15,20,25,30,40,45,90) : "))
        
        
    print(f"İstenilen şehir : {city.upper()}. \n{day} Günlük veri istenilmiştir.")
    
    url = f"https://havadurumu15gunluk.xyz/havadurumu30gunluk/630/{city}-hava-durumu-{str(day)}-gunluk.html"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")    
    rows = soup.find_all("tr")
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{city}` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50),
    tarih VARCHAR(255),
    durum VARCHAR(255),
    gunduz VARCHAR(10),
    gece VARCHAR(10)
    ) ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_turkish_ci;
    """

    cursor.execute(create_table_query)
    connector.commit()
    insert_query = f"""
    INSERT INTO `{city}` (city, tarih, durum, gunduz, gece)
    VALUES (%s, %s, %s, %s, %s)
    """

    for i in rows[1:]:
        tarih = i.find_all("td")[0].text
        hava_durumu_yorumu = i.find_all("td")[1].text
        gunduz = i.find_all("td")[3].text
        gece = i.find_all("td")[4].text
        cursor.execute(
        insert_query,
        (city, tarih, hava_durumu_yorumu, gunduz, gece)
        )

        connector.commit()
     
        
        
        
except ValueError:
    print("Geçersiz karakter girdiniz.")
    
except Exception as e:
    print(f"Hata : {e}")

finally:
    connector.close()
    print("Database kaydı başarılı.")