# Ben Body AI (Body-AI-Fitness-Assistant)

Kullanıcı profiline ve hedeflerine göre kişiselleştirilmiş AI destekli antrenman planları ve sohbet asistanı sunan bir Django web uygulaması.

## Ana Özellikler

* AI ile kişiselleştirilmiş antrenman planı oluşturma.
* Fitness odaklı, hafızalı AI sohbet asistanı.
* Kullanıcı profili yönetimi (Hedef, yaş, kilo, boy).
* Oluşturulan/alınan programları kaydetme, listeleme, silme ve tamamlama durumu takibi ("Programlarım").
* Temel istatistikler için Kontrol Paneli.

## Teknolojiler

* Python / Django
* Google Gemini API
* HTML / CSS / Bootstrap 5 / JavaScript
* SQLite / python-dotenv / markdown2 / marked.js

## Kurulum ve Çalıştırma

1.  **Projeyi Klonla:**
    ```bash
    git clone [https://github.com/fillopisyu/body-ai-fitness-assistant.git](https://github.com/fillopisyu/body-ai-fitness-assistant.git)
    cd body-ai-fitness-assistant
    ```
    *(URL'i kendi reponuzla değiştirin)*

2.  **Sanal Ortam Oluştur ve Aktifleştir:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate
    ```

3.  **Gereksinimleri Yükle:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Not: Eğer `requirements.txt` dosyanız yoksa, aktif sanal ortamda önce `pip freeze > requirements.txt` komutunu çalıştırın)*

4.  **API Anahtarını Ayarla (`.env`):**
    * Proje ana dizininde `.env` dosyası oluşturun.
    * İçine `GEMINI_API_KEY=SENIN_API_ANAHTARIN` satırını ekleyin.
    * `.env` dosyasının `.gitignore` içinde olduğundan emin olun!

5.  **Veritabanı Migration:**
    ```bash
    python manage.py migrate
    ```

6.  **Sunucuyu Başlat:**
    ```bash
    python manage.py runserver
    ```

7.  Tarayıcıda `http://127.0.0.1:8000/` adresine gidin. Admin paneli için (`/admin/`) `python manage.py createsuperuser` ile kullanıcı oluşturabilirsiniz.

## Lisans

[MIT Lisansı] *(Eğer MIT seçtiysen veya uygun olanı buraya yaz)*
