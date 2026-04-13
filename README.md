# Premier League Database System

Premier League Database System, 2015/16-2024/25 sezon araligindaki Premier League verilerini MySQL uzerinde tutan ve Flask tabanli bir web arayuzu ile gosteren bir veritabani projesidir.

Proje yalnizca bir web arayuzu degildir. Ayni zamanda:
- veritabani semasi kurulumunu,
- tarihsel ve ornek veri yuklemeyi,
- dis kaynaklardan veri toplamayi,
- eksik verileri temizlemeyi ve birlestirmeyi,
- oyuncu istatistikleri gibi turetilmis verileri olusturmayi
amaclayan yardimci Pythn scriptlerini de icerir.

## 1. Proje Amaci

Bu projenin amaci Premier League ile ilgili temel varliklari iliskisel bir veritabani uzerinde modellemek ve bu verileri hem SQL sorgulari hem de bir web arayuzu ile analiz edilebilir hale getirmektir.

Projede su alanlar tutulur:
- kulupler,
- teknik direktorler,
- oyuncular,
- maclar,
- oyuncu istatistikleri,
- transferler,
- sakatliklar,
- sezonluk puan durumlari.

## 2. Kullanilan Teknolojiler

- Python
- Flask
- MySQL
- mysql-connector-python
- Bootstrap 5
- Jinja2 templates

Veri toplama scriptlerinde ek olarak:
- requests
- BeautifulSoup

## 3. Sistem Mimarisi

Sistem uc ana katmandan olusur:

### 3.1 Veritabani Katmani

Ana veri modeli `schema.sql` icinde tanimlidir.

Bu katmanda:
- tablolar,
- foreign key iliskileri,
- view'lar,
- stored procedure'lar,
- trigger'lar
yer alir.

Temel tablo yapisi:
- `Club`
- `Coach`
- `Player`
- `Match`
- `PlayerStatistics`
- `Transfer`
- `Injury`
- `LeagueStandings`

### 3.2 Uygulama Katmani

`app.py`, Flask tabanli web uygulamasidir. Bu dosya:
- veritabanina baglanir,
- SQL sorgularini calistirir,
- HTML template'lerini render eder,
- kullanicidan gelen form verilerini kaydeder.

Uygulama server-side rendering kullanir. Yani arayuz ayri bir frontend framework ile degil, Flask + Jinja ile uretilir.

### 3.3 Veri Toplama ve Veri Hazirlama Katmani

Repo icindeki bircok Python scripti veri uretmek veya veriyi temizlemek icin kullanilir. Bu scriptler:
- dis kaynaklardan veri cekme,
- duplicate kayitlari birlestirme,
- piyasa degeri doldurma,
- forma numarasi guncelleme,
- oyuncu istatistigi uretme
gibi isleri yapar.

## 4. Dosya Yapisi

### 4.1 Ana Uygulama Dosyalari

- `app.py`
  Flask uygulamasi ve tum route'lar burada yer alir.

- `schema.sql`
  Veritabani semasi, view, procedure ve trigger tanimlari burada bulunur.

- `historical_data.sql`
  10 sezonluk tarihsel seed veri yuklemesi.

- `sample_data.sql`
  Daha kucuk ornek veri seti.

- `queries.sql`
  Analitik SQL sorgulari.

- `config.example.py`
  Veritabani baglantisi ve Flask `SECRET_KEY` ornegi.

### 4.2 Veri Toplama / Veri Duzeltme Scriptleri

- `fetch_data.py`
  Mac ve guncel kadro verilerini OpenFootball ve football-data.org uzerinden toplar.

- `fetch_historical_squads.py`
  Transfermarkt uzerinden tarihsel kadrolari cekmeye calisir.

- `fetch_missing_squads.py`
  Eksik kalan takim kadrolarini tamamlar.

- `fetch_jersey_numbers.py`
  Forma numaralarini gunceller.

- `fetch_tm_values.py`
  Transfermarkt verisine gore piyasa degerlerini doldurur.

- `set_market_values.py`
  Bilinen oyuncular icin elle belirlenmis veya kural tabanli market value atamasi yapar.

- `populate_stats.py`
  Oyuncu istatistiklerini, transferleri ve sakatlik kayitlarini doldurur.

- `regen_historical_stats.py`
  Tarihsel oyuncu istatistiklerini yeniden uretir.

- `regen_2425_stats.py`
  2024/25 sezonu oyuncu istatistiklerini yeniden uretir.

- `fix_clubs.py`
  Duplicate kulup kayitlarini merge eder ve iliskili kayitlari canonical club id'lere tasir.

### 4.3 Arayuz Dosyalari

- `templates/`
  Flask template dosyalari.

- `static/style.css`
  Arayuz stilleri.

## 5. Veritabani Nesneleri

### 5.1 Tablolar

- `Club`: kulup temel bilgileri
- `Coach`: teknik direktor bilgileri
- `Player`: oyuncu temel bilgileri
- `Match`: mac sonucu ve sezon bilgileri
- `PlayerStatistics`: oyuncu bazli mac istatistikleri
- `Transfer`: transfer kayitlari
- `Injury`: sakatlik kayitlari
- `LeagueStandings`: sezonluk puan durumu

### 5.2 View'lar

`schema.sql` icinde tanimli view'lar:
- `v_league_table`
- `v_top_scorers`
- `v_player_profile`
- `v_match_results`
- `v_active_injuries`

Bu view'lar raporlama ve dashboard gosterimleri icin kullanilir.

### 5.3 Stored Procedure'lar

- `sp_update_standings`
  Yeni bir mac eklendiginde puan durumunu gunceller.

- `sp_player_season_stats`
  Oyuncunun belirli bir sezondaki toplu istatistiklerini getirir.

- `sp_head_to_head`
  Iki kulup arasindaki mac gecmisini getirir.

### 5.4 Trigger'lar

- `trg_transfer_update_club`
  Yeni transfer kaydi olustugunda oyuncunun mevcut kulubunu gunceller.

- `trg_prevent_double_booking`
  Ayni tarihte ayni takima ikinci bir mac yazilmasini engeller.

## 6. Web Arayuzu ve Endpointler

Tum endpointler `app.py` icinde tanimlidir.

- `/`
  Dashboard

- `/clubs`
  Kulup listesi

- `/clubs/<club_id>`
  Kulup detay sayfasi

- `/players`
  Oyuncu listesi

- `/players/<player_id>`
  Oyuncu detay sayfasi

- `/players/add`
  Yeni oyuncu ekleme formu

- `/matches`
  Mac listesi

- `/matches/add`
  Yeni mac ekleme formu

- `/statistics`
  Sezonluk oyuncu ve kulup istatistikleri

- `/transfers`
  Transfer listesi

- `/transfers/add`
  Transfer ekleme islemi

- `/injuries`
  Sakatlik listesi

- `/injuries/add`
  Sakatlik ekleme islemi

- `/queries`
  Analitik sorgu sonuclarini gosteren sayfa

## 7. Kurulum

### 7.1 Gereksinimler

- Python 3.x
- MySQL Server

### 7.2 Python Paketleri

Minimum:

```bash
pip install -r requirements.txt
```

Scraper scriptleri icin ayrica gerekli olabilir:

```bash
pip install requests beautifulsoup4
```

### 7.3 Konfigurasyon

`config.example.py` dosyasini `config.py` olarak kopyalayin ve duzenleyin:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'database': 'premier_league_db',
}

SECRET_KEY = 'your-secret-key-here'
```

### 7.4 Veritabani Kurulumu

1. `schema.sql` calistirilir.
2. Istega bagli olarak `historical_data.sql` veya `sample_data.sql` yuklenir.
3. Gerekirse yardimci scriptler calistirilir.

## 8. Uygulamayi Calistirma

```bash
python app.py
```

Varsayilan baglanti:

```text
http://localhost:5000/
```

## 9. Veri Akisi

Tipik veri akisi su sekildedir:

1. Veritabani `schema.sql` ile olusturulur.
2. Tarihsel veri `historical_data.sql` ile yuklenir.
3. Eksik veya guncel veri icin fetch scriptleri calistirilir.
4. Duplicate kulup varsa `fix_clubs.py` ile birlestirilir.
5. Oyuncu istatistikleri `populate_stats.py` veya `regen_*` scriptleri ile uretilir.
6. Flask uygulamasi bu verileri arayuzde gosterir.

## 10. Bilinen Sinirlamalar ve Teknik Notlar

Bu proje ders/term project mantiginda oldukca iyi bir kapsam sunar; ancak teknik olarak bazi kisitlari vardir:

- Oyuncunun mevcut kulubu `Player.club_id` alaninda tutulur.
- Transfer trigger'i oyuncunun kulubunu gunceller.
- Bu nedenle tarihsel sezondaki bazi oyuncu-kulup iliskileri bugune kaymis gorunebilir.
- `PlayerStatistics` tablosunda oyuncunun mac sirasindaki kulubu ayrica tutulmadigi icin tarihsel analizlerde dogruluk kaybi olabilir.
- Veri setinin bir kismi scrape edilmis, bir kismi scriptler ile tahmini olarak uretilmistir.
- Bazi scriptler icinde sabit veritabani sifresi ve API key benzeri hardcoded alanlar bulunur; bunlar production icin uygun degildir.
- Repo icindeki encoding bazi dosyalarda bozulmus gorunebilir.

## 11. Guclu Yonler

- Iliskisel model acik ve anlasilir.
- Web arayuzu ile SQL modeli birbirine iyi baglanmis.
- View, trigger ve stored procedure kullanimi sayesinde veritabani tarafinda da anlamli bir is mantigi bulunuyor.
- Veri toplama ve veri duzeltme scriptleri sayesinde proje kapsamli bir ekosistem haline gelmis.

## 12. Gelistirme Onerileri

- `PlayerStatistics` tablosuna `club_id` eklenerek tarihsel dogruluk artirilabilir.
- API key ve DB sifreleri `env` dosyalarina tasinabilir.
- `requirements.txt` scraper bagimliliklariyla genisletilebilir.
- Ayrica bir `docs/` klasoru acilarak:
  - teknik mimari,
  - ER diyagrami,
  - kullanim senaryolari,
  - veri toplama akisi
  ayri dokumanlar halinde yazilabilir.

## 13. Ozet

Bu proje, Premier League verisini iliskisel veritabani mantigi ile modelleyen, SQL raporlama ve Flask arayuzu ile sunan, yardimci scriptlerle veri toplayan ve temizleyen kapsamli bir veritabani sistemidir.

Ozellikle:
- veritabani tasarimi,
- sorgu mantigi,
- veri butunlugu,
- web uzerinden veri sunumu
acisindan guclu bir ders projesi tabani sunmaktadir.
