# 1. Proje Adı

**Premier League Data Management System**

# 2. Proje Amacı

Bu proje, Premier League kapsamında kulüp, oyuncu, teknik direktör, maç, oyuncu istatistikleri, transfer, sakatlık ve puan durumu verilerini ilişkisel bir veritabanı yapısı içerisinde düzenli biçimde saklamak, yönetmek ve kullanıcıya bir arayüz üzerinden sunmak amacıyla tasarlanmıştır. Projenin temel hedefi, futbol verisini yalnızca depolayan bir sistem kurmak değil; aynı zamanda bu veriler üzerinden filtreleme, karşılaştırma ve analitik sorgulama yapılabilen bütünleşik bir yapı oluşturmaktır. Repo içeriğinde yer alan `schema.sql`, `sample_data.sql`, `historical_data.sql`, `queries.sql` ve Python tabanlı veri toplama dosyaları, sistemin hem veri üretimi hem de veri sunumu açısından çok katmanlı olarak planlandığını göstermektedir.

# 3. Veritabanı Tasarımı

Projede veritabanının çekirdeğini **8 ana tablo** oluşturmaktadır: `Club`, `Coach`, `Player`, `Match`, `PlayerStatistics`, `Transfer`, `Injury` ve `LeagueStandings`. `Club` tablosunda `club_id`, `name`, `city`, `stadium`, `capacity` ve `founded` gibi kulübe ait temel bilgiler tutulacaktır. `Coach` tablosunda `coach_id`, `first_name`, `last_name`, `nationality`, `date_of_birth`, `club_id`, `contract_start` ve `contract_end` alanları ile teknik direktör bilgileri saklanacaktır. `Player` tablosunda `player_id`, `first_name`, `last_name`, `nationality`, `date_of_birth`, `position`, `jersey_number`, `club_id`, `market_value` ve `contract_end` alanları bulunacaktır.

`Match` tablosu her karşılaşma için `match_id`, `home_club_id`, `away_club_id`, `match_date`, `home_score`, `away_score`, `season` ve `gameweek` bilgilerini içerecektir. `PlayerStatistics` tablosu oyuncu ile maçı ilişkilendiren ana performans tablosudur; burada `player_id`, `match_id`, `goals`, `assists`, `yellow_cards`, `red_cards`, `minutes_played`, `shots_on_target` ve `passes_completed` gibi veriler tutulacaktır. `Transfer` tablosunda oyuncuların kulüpler arası geçişleri için `player_id`, `from_club_id`, `to_club_id`, `transfer_date`, `transfer_fee` ve `season` alanları yer alacaktır. `Injury` tablosu `player_id`, `injury_type`, `start_date`, `end_date` ve `matches_missed` verilerini saklayacaktır. `LeagueStandings` tablosu ise sezon bazlı lig tablosunu üretmek için `club_id`, `season`, `played`, `won`, `drawn`, `lost`, `goals_for` ve `goals_against` alanlarını içerecektir.

Tablolar arasındaki ilişkiler foreign key yapıları ile kurulacaktır. Bir kulübün birden fazla oyuncusu ve teknik direktörü olabilir; bu nedenle `Club` tablosu `Player` ve `Coach` tabloları ile ilişkilidir. `Match` tablosu iki farklı kulübü bağlar ve `PlayerStatistics` tablosu üzerinden oyuncu ile maç arasında çoktan çoğa ilişki kurulmuş olur. `Transfer` ve `Injury` tabloları doğrudan `Player` tablosuna bağlıdır. `LeagueStandings` tablosu ise kulüp ve sezon bazında özet performans verisini tutar. Ayrıca, şemada tanımlı `v_league_table`, `v_top_scorers`, `v_player_profile` ve `v_match_results` gibi view yapıları sorgu performansını ve raporlamayı kolaylaştıracaktır. **ER diyagramı proje dokümanının bir sonraki aşamasında ayrıca hazırlanacaktır.**

# 4. Arayüz Tasarımı

Projede veritabanına bağlı çalışan bir web arayüzü bulunacaktır. Repo içeriğindeki `app.py` dosyası ve `templates/` klasörü, bu arayüzün Python Flask tabanlı olarak geliştirildiğini göstermektedir. Arayüz; öğretim elemanı, proje grubu üyeleri ve sistemi inceleyen son kullanıcılar tarafından kullanılabilecek şekilde tasarlanacaktır. Kullanıcılar bu arayüz üzerinden kulüp listelerini görüntüleyebilecek, kulüp detaylarına erişebilecek, oyuncuları filtreleyebilecek, maç sonuçlarını inceleyebilecek, transfer ve sakatlık kayıtlarını görebilecek ve sezon bazlı istatistikleri takip edebilecektir.

Ayrıca mevcut yapı, belirli veri giriş işlemlerini de desteklemektedir. Örneğin kullanıcılar yeni oyuncu ekleyebilecek, maç kaydı oluşturabilecek, transfer girişi yapabilecek ve sakatlık kaydı ekleyebilecektir. Böylece arayüz yalnızca raporlama amacıyla değil, temel veri yönetim işlemleri için de kullanılacaktır. `base.html` ve diğer sayfa şablonları üzerinden dashboard, kulüpler, oyuncular, maçlar, istatistikler, transferler, sakatlıklar ve analitik sorgular için ayrı ekranlar sunulacaktır.

# 5. Sorgular ve Filtreleme

Arayüz üzerinden kullanıcıların özellikle sezon, kulüp, oyuncu adı ve pozisyon bazında filtreleme yapabilmesi planlanmaktadır. Örneğin oyuncular sayfasında pozisyona veya kulübe göre listeleme yapılabilecek; maçlar sayfasında sezon seçilebilecek; kulüp detay ekranında ilgili sezonun kadrosu ve maçları ayrı olarak görüntülenebilecektir. Bu yapı, repo içindeki `app.py` dosyasında bulunan `request.args.get(...)` tabanlı filtreleme mantığı ile uyumludur.

Sistem, SQL Query Lab mantığına benzer biçimde aşağıdaki soru türlerine cevap verecek şekilde tasarlanmıştır:

1. Belirli bir sezonda lig şampiyonu hangi takım olmuştur ve kaç puan toplamıştır?
2. Bir sezonda en çok gol atan oyuncular kimlerdir?
3. Kulüplerin toplam piyasa değeri ile sezon performansı arasında nasıl bir ilişki vardır?
4. En pahalı transferler hangi oyuncular için gerçekleşmiştir?
5. Hangi kulüpler en fazla sakatlık yaşamıştır ve toplam kaç maç kaybı oluşmuştur?
6. Belirli bir oyuncunun sezon bazlı gol, asist ve dakika istatistikleri nelerdir?
7. İki kulüp arasındaki head-to-head maç sonuçları nasıldır?

Bu kapsamda örnek sorgu tipleri olarak; sezon bazlı puan durumu sorgusu, gol krallığı sorgusu, kulüp performans karşılaştırması, oyuncu kariyer özeti, transfer analizi, sakatlık yoğunluğu analizi ve maç sonuç dağılımı sorguları kullanılacaktır. Repo içindeki `queries.sql` dosyası, all-time champions, top scorers, club performance, most expensive signings, injury analysis ve view tabanlı sezon sıralamaları gibi sorguların bu sistemde uygulanacağını göstermektedir. Bu nedenle veritabanı, hem operasyonel veri yönetimine hem de analitik raporlamaya cevap verecek yapıdadır.

# 6. Grup Üyeleri

- Ad Soyad
- Ad Soyad
- Ad Soyad
- Ad Soyad
- Ad Soyad

# 7. Sonuç

Sonuç olarak bu proje, Premier League verilerinin ilişkisel veritabanı mantığıyla modellenmesi, dış kaynaklardan veri toplanması, kullanıcı dostu bir arayüz ile sunulması ve analitik sorgularla anlamlı bilgi üretilmesi amacıyla bütüncül biçimde tasarlanmıştır. Mevcut repo yapısı incelendiğinde, projenin hem veritabanı dersi gerekliliklerini karşılayan hem de gerçek veriyle çalışan teknik bir uygulama olarak geliştirildiği anlaşılmaktadır. Bu yönüyle proje; veri modelleme, sorgulama, filtreleme ve arayüz entegrasyonunu bir araya getiren tutarlı bir dönem projesi niteliğindedir.
