Eye Dashboard (Docker Version)
==============================

**Eye** on minimalistlik ja kiire reaalajas kaamerate vaatepaneel, mis on ehitatud go2rtc striimide kuvamiseks. See on spetsiaalselt optimeeritud kasutamiseks telerites (Google TV / Fully Kiosk), tahvelarvutites ja nutitelefonides (iOS/Android).

Peamised omadused
-----------------

*   **TV-sõbralik**: Täielik navigeerimine nooleklahvidega ja puldi toetus.
    
*   **PWA valmidus**: Saab installida koduekraanile kui eraldi äpi (ilma brauseri aadressiribata).
    
*   **Turvaline**: Token-põhine ligipääs, mida hallatakse keskkonnamuutujatega (.env).
    
*   **Kerge**: Dockeril põhinev Flask backend ja puhas JavaScript frontend.
    

Paigaldamine
------------

### 1. Ettevalmistus

Klooni repositoorium ja loo vajalikud failid:

```bash
# Loo koopia näidiskonfiguratsioonist
cp go2rtc.yaml.example go2rtc.yaml
```

### 2. Pääsukoodide (tokenite) loomine

Kasuta kaasasolevat skripti, et genereerida turvalised koodid:

```bash
python3 generate_tokens.py   `
```

### 3. Keskkonnamuutujate seadistamine

Loo projekti juurkataloogi fail nimega .env ja lisa sinna oma andmed:

```bash
# .env faili sisu
ACCESS_TOKENS=sinu_genereeritud_kood1,kood2,kood3
GO2RTC_API=http://127.0.0.1:1984/api/streams
```

### 4. Käivitus Dockeriga

```bash
docker compose up -d --build
```

Kasutamine
----------

Pärast käivitamist on vaatepaneel kättesaadav järgmisel aadressil:http://:8080?token=

**Märkus:** Kui avate lehe ilma õige tokenita, kuvatakse viga "Unauthorized".

### Google TV ja Fully Kiosk

1.  Sisestage Fully Kioski seadetes **Start URL** kujul: http://192.168.x.x:8080?token=sinu_kood.
    
2.  Seadistage navigatsiooniriba peidetuks, et saavutada täisekraani kogemus.
    

Projekti ülesehitus
-------------------

*   app/main.py: Flask backend, mis tegeleb autoriseerimise ja go2rtc API-ga.
    
*   www/index.html: Dünaamiline grid-liides (CSS/JS).
    
*   www/video-stream.js: Modifitseeritud go2rtc komponent.
    
*   generate_tokens.py: Abivahend turvaliste tokenite loomiseks.
    
*   docker-compose.yml: Stacki definitsioon (Eye + go2rtc).
    

Autorid ja litsents
-------------------

*   Ikooni autor: [Security Camera Vectors by Vecteezy](https://www.vecteezy.com/free-vector/security-camera)
    
*   Projekti sisu: MIT litsents
