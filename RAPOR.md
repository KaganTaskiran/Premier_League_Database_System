# Premier League Database System
## Sistem Analizi ve Teknik Rapor

## 1. Giris

Bu proje, Premier League verilerinin iliskisel veritabani mantigi ile modellenmesi, saklanmasi, sorgulanmasi ve web arayuzu uzerinden sunulmasi amaciyla gelistirilmis bir veritabani sistemidir. Sistem, 2015/16 ile 2024/25 sezonlari arasindaki tarihsel ve guncel verileri bir arada ele almayi hedeflemektedir.

Proje kapsaminda kulup, oyuncu, teknik direktor, mac, oyuncu istatistikleri, transfer, sakatlik ve puan durumu gibi futbol odakli temel varliklar modellenmistir. Bu veriler MySQL uzerinde tutulmakta, Flask tabanli bir web arayuzu ile son kullaniciya gosterilmektedir. Buna ek olarak, cesitli Python scriptleri kullanilarak farkli veri kaynaklarindan veri cekilmekte, eksik veriler tamamlanmakta ve turetilmis istatistiksel kayitlar olusturulmaktadir.

## 2. Projenin Amaci

Bu projenin temel amaci, bir spor verisi alaninda iliskisel veritabani tasarimi yaparak bu tasarimi calisan bir uygulama ile desteklemektir. Bu kapsamda proje su hedeflere yoneliktir:

- Premier League ile ilgili temel varliklari duzgun sekilde modellemek,
- tablo iliskileri, foreign key yapilari ve veri butunlugu kurallarini uygulamak,
- SQL sorgulari ile anlamli raporlar uretebilmek,
- kullanicinin web arayuzu uzerinden verileri incelemesini saglamak,
- veri toplama ve veri temizleme sureclerini otomatiklestirmek.

## 3. Kullanilan Teknolojiler

Proje icinde kullanilan temel teknolojiler asagidadir:

- Python
- Flask
- MySQL
- mysql-connector-python
- Jinja2
- Bootstrap 5

Veri toplama ve scraping amacli scriptlerde ayrica su kutuphaneler kullanilmistir:

- requests
- BeautifulSoup

Bu teknoloji secimi sayesinde hem veritabani odakli hem de arayuz destekli bir sistem kurulmustur.

## 4. Sistem Mimarisi

Sistem genel olarak uc katmanli bir yapida dusunulebilir:

### 4.1 Veritabani Katmani

Veritabani katmani, tum ana veri modelini ve veri butunlugu kurallarini icerir. Bu katmanda tablolar, view'lar, stored procedure'lar ve trigger'lar tanimlanmistir. Sistem icindeki asil mantik merkezlerinden biri bu katmandir.

Ana veritabani tanimi `schema.sql` dosyasi icinde yer almaktadir.

### 4.2 Uygulama Katmani

Uygulama katmani `app.py` dosyasi icinde gelistirilmistir. Flask framework'u kullanilarak olusturulan bu katman:

- veritabanina baglanir,
- SQL sorgularini calistirir,
- HTML template'lerini render eder,
- form verilerini alarak yeni kayitlar ekler,
- kullaniciya sayfa bazli bir gezinme deneyimi sunar.

Bu yapi REST API merkezli degil, server-side rendered bir web uygulamasidir.

### 4.3 Veri Toplama ve Veri Hazirlama Katmani

Bu katman, farkli Python scriptlerinden olusur. Scriptlerin amaci:

- dis kaynaklardan veri cekmek,
- eksik kayitlari tamamlamak,
- duplicate verileri duzeltmek,
- piyasa degeri, forma numarasi ve istatistik gibi alanlari doldurmak,
- tarihsel ve guncel veri setini zenginlestirmektir.

Bu nedenle proje, sadece sabit SQL dosyalarindan olusan bir veritabani odevi degil; ayni zamanda veri hazirlama sureci iceren daha genis kapsamli bir sistem haline gelmistir.

## 5. Veritabani Tasarimi

Projedeki temel tablolar su sekildedir:

### 5.1 Club

Bu tablo kulup bilgilerini tutar. Kulup adi, sehir, stadyum, kapasite ve kurulus yili gibi alanlari icerir.

### 5.2 Coach

Teknik direktor bilgileri bu tabloda tutulur. Teknik direktorun adi, milliyeti, dogum tarihi, bagli oldugu kulup ve kontrat tarihleri bulunur.

### 5.3 Player

Oyuncu tablosu sistemin en temel tablolarindan biridir. Oyuncularin ad, soyad, milliyet, dogum tarihi, pozisyon, forma numarasi, mevcut kulup, market value ve kontrat bitis bilgileri burada saklanir.

### 5.4 Match

Mac tablosu, ic saha ve dis saha kulubu, skor, mac tarihi, sezon ve hafta bilgilerini icerir.

### 5.5 PlayerStatistics

Oyuncu bazli mac istatistikleri bu tabloda tutulur. Gol, asist, sari kart, kirmizi kart, sure ve sut gibi alanlar bu tabloda yer alir.

### 5.6 Transfer

Oyuncularin kulup degisimleri, transfer tarihi ve transfer ucreti bilgileri bu tabloda saklanir.

### 5.7 Injury

Oyuncularin sakatlik turu, baslangic ve bitis tarihi ile kac mac kacirdigi bilgileri burada tutulur.

### 5.8 LeagueStandings

Sezonluk puan durumu bilgileri bu tabloda yer alir. Oynanan mac sayisi, galibiyet, beraberlik, maglubiyet, atilan ve yenilen gol gibi istatistikler burada tutulur.

## 6. Veritabani Uzerindeki Ek Nesneler

Veritabani yalnizca tablolardan olusmamaktadir. Sistem icinde raporlama ve veri butunlugu icin ek nesneler de tanimlanmistir.

### 6.1 View'lar

Sistemde su view'lar tanimlanmistir:

- `v_league_table`
- `v_top_scorers`
- `v_player_profile`
- `v_match_results`
- `v_active_injuries`

Bu view'lar sayesinde karmasik sorgular uygulama katmaninda tekrar tekrar yazilmak zorunda kalmadan kullanilabilir hale gelmistir.

### 6.2 Stored Procedure'lar

Sistemde asagidaki procedure'lar bulunmaktadir:

- `sp_update_standings`
- `sp_player_season_stats`
- `sp_head_to_head`

Ozellikle `sp_update_standings`, yeni bir mac eklendiginde sezon puan durumunun otomatik olarak guncellenmesini saglayarak uygulama tarafindaki is yukunu azaltmaktadir.

### 6.3 Trigger'lar

Sistemde asagidaki trigger'lar yer almaktadir:

- `trg_transfer_update_club`
- `trg_prevent_double_booking`

Bu trigger'lar veri butunlugunu desteklemektedir. Ornegin bir transfer eklendiginde oyuncunun kulubu otomatik olarak degistirilmekte, ayni tarihte ayni takim icin ikinci bir mac olusturulmasi ise engellenmektedir.

## 7. Web Uygulamasi ve Kullanici Arayuzu

Web uygulamasi Flask kullanilarak gelistirilmistir. Arayuz tarafinda Jinja template sistemi ve Bootstrap kullanilmistir. Bu nedenle arayuz dinamik ancak yapisal olarak sade ve anlasilir bir mimariye sahiptir.

Uygulamada yer alan temel sayfalar su sekildedir:

- Ana sayfa ve dashboard
- Kulup listesi
- Kulup detay sayfasi
- Oyuncu listesi
- Oyuncu detay sayfasi
- Mac listesi
- Istatistik sayfasi
- Transfer sayfasi
- Sakatlik sayfasi
- Analitik sorgular sayfasi

Bu sayfalar sayesinde kullanici sistemdeki ana verileri tarayabilir, filtreleyebilir ve belirli alanlarda yeni kayit ekleyebilir.

## 8. Uygulama Endpointleri

Uygulama icindeki temel route yapilari asagidaki gibidir:

- `/`
- `/clubs`
- `/clubs/<club_id>`
- `/players`
- `/players/<player_id>`
- `/players/add`
- `/matches`
- `/matches/add`
- `/statistics`
- `/transfers`
- `/transfers/add`
- `/injuries`
- `/injuries/add`
- `/queries`

Bu endpointler JSON tabanli bir API sunmaktan cok, kullaniciya HTML sayfalari gosteren bir web uygulamasi mantiginda calismaktadir.

## 9. Veri Toplama ve Yardimci Scriptler

Projede birden fazla yardimci script yer almaktadir. Bu scriptler, sistemin veri kalitesini ve veri kapsamini artirmak icin kullanilmaktadir.

### 9.1 fetch_data.py

Mac verilerini ve guncel kadrolari dis kaynaklardan toplamak icin kullanilir. OpenFootball ve football-data.org kaynaklarindan yararlanir.

### 9.2 fetch_historical_squads.py

Transfermarkt kaynakli tarihsel kadro verilerini toplamayi amaclar. Ayrica tarihsel sezondaki oyuncu istatistiklerini olusturmak icin de kullanilir.

### 9.3 fetch_missing_squads.py

Eksik kalan takimlarin kadrolarini tamamlamak ve bazi null alanlari doldurmak icin kullanilir.

### 9.4 fetch_jersey_numbers.py

2024/25 sezonu icin forma numarasi bilgilerini gunceller.

### 9.5 fetch_tm_values.py

Oyuncu piyasa degerlerini Transfermarkt uzerinden cekmeye ve veritabani ile eslestirmeye calisir.

### 9.6 set_market_values.py

Verisi eksik olan oyuncular icin manuel veya kural tabanli market value atamasi yapar.

### 9.7 populate_stats.py

Oyuncu istatistikleri, transferler ve sakatliklar gibi ek verileri sisteme doldurur.

### 9.8 fix_clubs.py

Duplicate kulup kayitlarini merge ederek veri tutarliligi saglamayi hedefler. Bu script, kulup id'lerine bagli diger tablolari da guncelledigi icin kritik bir migration gorevi gorur.

## 10. Kurulum ve Calistirma

Projeyi calistirmak icin once Python ve MySQL ortamlarinin hazir olmasi gerekir.

Izlenecek genel adimlar su sekildedir:

1. Python bagimliliklari kurulur.
2. `config.example.py` dosyasi `config.py` olarak kopyalanir.
3. Veritabani baglanti bilgileri duzenlenir.
4. `schema.sql` calistirilir.
5. Gerekirse `historical_data.sql` veya `sample_data.sql` ile veri yuklenir.
6. Flask uygulamasi `python app.py` komutu ile baslatilir.

Uygulama varsayilan olarak su adreste calismaktadir:

`http://localhost:5000/`

## 11. Sistemin Guclu Yonleri

Bu projenin guclu yonleri su sekilde ozetlenebilir:

- Iliskisel veri modeli acik ve kapsamli bir sekilde kurulmustur.
- Veritabani tarafinda sadece tablo degil, view, procedure ve trigger kullanimi da vardir.
- Flask arayuzu sayesinde veri kullaniciya anlamli bir sekilde sunulmaktadir.
- Veri toplama ve veri temizleme scriptleri projeyi daha kapsamli hale getirmektedir.
- Analitik sorgu mantigi proje icinde belirgin bir yer tutmaktadir.

## 12. Sistemin Sinirlamalari

Projede teknik olarak gelistirilebilecek bazi noktalar vardir.

Ilk olarak, oyuncunun mevcut kulubu `Player.club_id` alaninda tutulmakta ve transfer trigger'i ile guncellenmektedir. Ancak `PlayerStatistics` tablosunda oyuncunun o maca ait kulubu tutulmamaktadir. Bu durum, tarihsel veriler uzerinde yapilan bazi analizlerde oyuncunun gecmis sezondaki kulubunun yanlis gorunmesine neden olabilir.

Ikinci olarak, repo icinde bazi scriptlerde sabit sifre ve API key bilgileri bulunmaktadir. Bu yapi ders projesi icin kabul edilebilir olsa da guvenlik ve tasinabilirlik acisindan dogru bir yaklasim degildir.

Ucuncu olarak, verilerin bir kismi gercek kaynaklardan scrape edilmis olsa da bir kismi tahmine dayali ya da sentetik olarak uretilmistir. Bu nedenle sistemdeki her veri mutlak gercek veri olarak dusunulmemelidir.

Son olarak, bagimlilik listesi `requirements.txt` icinde yalnizca web uygulamasi icin gerekli paketleri icermektedir. Scraping scriptleri icin gereken ek kutuphaneler ayri olarak kurulmalidir.

## 13. Gelistirme Onerileri

Projenin daha saglam ve surdurulebilir hale gelmesi icin su gelistirmeler onerilebilir:

- `PlayerStatistics` tablosuna oyuncunun maca ciktigi kulubu gosteren bir alan eklenmesi,
- hassas bilgilerin `.env` veya cevre degiskenlerine tasinmasi,
- tum script bagimliliklarinin tek bir bagimlilik listesinde toplanmasi,
- proje icin ayri bir `docs/` klasoru ile teknik dokuman seti olusturulmasi,
- ER diyagrami ve veri akis diyagraminin eklenmesi,
- veri uretim scriptlerinin daha moduler hale getirilmesi.

## 14. Sonuc

Premier League Database System, iliskisel veritabani tasarimi ile uygulama gelistirmeyi bir araya getiren kapsamli bir projedir. Sistem; veri modelleme, veri butunlugu, SQL tabanli analiz, web arayuzu ile gosterim ve veri hazirlama sureclerini ayni cati altinda toplamistir.

Bu yonuyle proje, bir veritabani dersi kapsaminda hem teorik hem de uygulamali acidan basarili bir calisma zemini sunmaktadir. Bununla birlikte, tarihsel veri dogrulugu ve konfigurasyon yonetimi gibi alanlarda daha ileri seviye iyilestirmelerle sistem daha profesyonel bir yapiya donusturulebilir.
