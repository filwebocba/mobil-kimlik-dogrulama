
---

# PRD: Kimlik Onay Sistemi (KYC Projesi)

**Versiyon:** 1.0

## 1. Giriş ve Amaç 🎯

Bu doküman, kullanıcıların kimlik bilgilerini ve görsellerini güvenli bir şekilde göndererek hesaplarını doğrulatabilecekleri, mobil öncelikli bir web uygulamasının gereksinimlerini tanımlar. Projenin temel amacı; kullanıcıdan alınan verileri (kişisel bilgiler, kimlik görseli, selfie) güvenli bir veritabanına kaydetmek, bu talepleri gerçek zamanlı bir admin panelinde görüntülemek ve admin onayı ile kullanıcı hesabının durumunu güncellemektir.

## 2. Kullanıcı Hikayeleri 📖

- **Kullanıcı Olarak:**
    - Mobil cihazımdan sisteme girdiğimde, kullanıcı adı, ad, soyad, e-posta ve telefon bilgilerimi girebileceğim bir form görmek istiyorum.
    - Kimliğimin ön yüzünün fotoğrafını çekmek için "Kimlik Yükle" butonuna bastığımda doğrudan cihazımın arka kamerasının açılmasını istiyorum.
    - Kimliğimle birlikte selfie çekmek için "Selfie Yükle" butonuna bastığımda doğrudan cihazımın ön kamerasının açılmasını istiyorum.
    - Galerimden fotoğraf seçme seçeneğimin olmamasını istiyorum.
    - Formu gönderdiğimde bilgilerimin onaya gönderildiğine dair bir bildirim almak istiyorum.
    - Masaüstü bir tarayıcıdan siteye girdiğimde, "Lütfen mobil cihaz kullanın" uyarısıyla karşılaşmak istiyorum.

- **Admin Olarak:**
    - Web tabanlı (masaüstü uyumlu) bir admin paneline giriş yapmak istiyorum.
    - Yeni bir kimlik onay talebi geldiğinde panelin anında (real-time) güncellenmesini istiyorum.
    - Onay bekleyen tüm kullanıcıların listesini, bilgilerini ve yükledikleri görselleri (kimlik ve selfie) görüntüleyebilmek istiyorum.
    - Her bir talep için "Onayla" veya "Reddet" butonlarını kullanarak işlemi tamamlayabilmek istiyorum.
    - Verdiğim onayın anında veritabanına işlenmesini ve kullanıcının durumunun güncellenmesini istiyorum.

## 3. Teknik Mimari ve Teknoloji Yığını 🏗️

Proje, **Headless (ayrık)** bir mimari üzerine kurulacaktır. Frontend (kullanıcı arayüzü) ve Backend (sunucu mantığı) birbirinden tamamen bağımsız geliştirilecek ve API'lar aracılığıyla haberleşecektir. Bu, esneklik, ölçeklenebilirlik ve bakım kolaylığı sağlar.

### **Teknoloji Yığını:**

* **Frontend:** **React** (Vite ile oluşturulmuş)
    * **UI Kütüphanesi:** **Material-UI (MUI)** - Kapsamlı bileşen seti ve mobil uyumlu tasarımı hızlandırması için tercih edilmiştir.
    * **Form Yönetimi:** **React Hook Form** - Performanslı ve kolay doğrulanabilir formlar oluşturmak için.
* **Backend:** **Python (FastAPI)**
    * **Asenkron Sunucu:** **Uvicorn**
    * **Veri Doğrulama:** **Pydantic** - Gelen API isteklerinin güvenliğini ve doğruluğunu sağlamak için.
* **Veritabanı, Depolama ve Auth:** **Supabase**
    * **Veritabanı:** Supabase
    * **Dosya Depolama:** Supabase Storage - Kimlik ve selfie görsellerini saklamak için.
    * **Real-time:** Supabase Realtime - Admin panelini anlık güncellemek için.
    * **Auth:** Supabase Auth - Admin paneli kullanıcı yönetimi için.
* **Deployment:** **Vercel**

---

## 4. Vercel için Dosya Yapısı ve Deployment Stratejisi 📁

Vercel, bu teknoloji yığını için mükemmel bir platformdur ve **monorepo** (tek bir kod deposu) yapısını destekler. Bu sayede hem frontend'i hem de backend'i aynı projede yönetebiliriz.



### **Önerilen Dosya Yapısı:**

```
kyc-project/
├── api/                  # 👈 FastAPI backend kodu buraya gelecek
│   ├── __init__.py
│   └── index.py          # Ana FastAPI uygulaması
├── src/                  # 👈 React frontend kodu buraya gelecek
│   ├── components/
│   ├── pages/
│   └── App.jsx
├── public/
├── package.json          # React'in bağımlılıkları
├── requirements.txt      # Python'un (FastAPI) bağımlılıkları
└── vercel.json           # Vercel yapılandırma dosyası
```

### **Deployment Süreci:**

1.  **Vercel Yapılandırması (`vercel.json`):** Vercel'e projenin nasıl derleneceğini ve yönlendirileceğini bu dosya ile anlatırız.
    ```json
    {
      "builds": [
        {
          "src": "requirements.txt",
          "use": "@vercel/python"
        },
        {
          "src": "package.json",
          "use": "@vercel/node",
          "config": { "installCommand": "npm install" }
        }
      ],
      "routes": [
        {
          "src": "/api/(.*)",
          "dest": "/api/index.py"
        },
        {
          "src": "/(.*)",
          "dest": "/"
        }
      ]
    }
    ```
    * `builds` bölümü, Vercel'e hem Python (`@vercel/python`) hem de Node.js (`@vercel/node`) ortamlarını kurmasını söyler.
    * `routes` bölümü, `/api/` ile başlayan tüm istekleri FastAPI uygulamasına (`/api/index.py`), diğer tüm istekleri ise React uygulamasına yönlendirir.

2.  **Backend (`/api/index.py`):** FastAPI kodunuz Vercel'de **Serverless Function** olarak çalışacaktır.
3.  **Frontend (`/src`):** React kodunuz Vercel tarafından otomatik olarak build edilir ve statik olarak sunulur.
4.  **Ortam Değişkenleri (Environment Variables):** Supabase URL ve anahtarları gibi hassas bilgileri doğrudan Vercel projenizin ayarlarından "Environment Variables" bölümüne eklemelisiniz. Kod içerisine asla bu bilgileri yazmayın.

---

## 5. Supabase Entegrasyonu (Modern Yöntemler) ⚡

Supabase ile entegrasyon, projenin bel kemiğini oluşturur.

### **Veritabanı İşlemleri:**

* **Tablo Yapısı:** `verification_requests` tablosu `2. Kullanıcı Hikayeleri` bölümünde belirtilen alanlara ek olarak `status` için `ENUM` ('pending', 'approved', 'rejected') tipi kullanılarak oluşturulmalıdır. Bu, veri bütünlüğünü sağlar.
* **Güvenlik (RLS - Row Level Security):** Supabase'in en güçlü özelliğidir. **Mutlaka etkinleştirilmelidir.**
    * **Kural 1:** Kullanıcıların hiçbir veriyi okuyamaması (çünkü veriler sadece admin paneline gidecek).
    * **Kural 2:** Sadece "service\_role\_key" kullanan backend'in (FastAPI) tabloya veri yazabilmesi.
    * **Kural 3:** Sadece "admin" rolüne sahip kullanıcıların (eğer Supabase Auth kullanılırsa) verileri okuyabilmesi.

### **Görsel Yükleme (Secure File Uploads):**

En güvenli yöntem, görselleri doğrudan tarayıcıdan Supabase'e yüklemek yerine, bir **aracı (proxy)** olarak backend'i kullanmaktır.

1.  **Kullanıcı (React):** Çektiği fotoğrafı `FormData` ile FastAPI'deki `/api/verification` endpoint'ine gönderir.
2.  **Backend (FastAPI):**
    * Gelen dosyayı alır.
    * Gerekirse `Pillow` kütüphanesi ile görseli optimize eder (boyut küçültme, sıkıştırma).
    * Supabase'in **service\_role\_key**'ini kullanarak (bu anahtar RLS kurallarını atlama yetkisine sahiptir) görseli Supabase Storage'daki güvenli bir "bucket"a yükler.
    * Yükleme sonrası aldığı `public URL`'i, diğer form verileriyle birlikte Supabase veritabanına kaydeder.

Bu yöntem, Supabase anahtarlarınızın tarayıcıda ifşa olmasını engeller ve size görseller üzerinde tam kontrol sağlar.

### **Real-time Admin Paneli:**

* Admin panelinin React uygulamasında, Supabase'in JavaScript kütüphanesi (`@supabase/supabase-js`) kullanılarak `verification_requests` tablosundaki `INSERT` olayları dinlenir.
    ```javascript
    // Admin panelindeki bir React bileşeninde
    useEffect(() => {
      const channel = supabase
        .channel('db-verification-requests')
        .on(
          'postgres_changes',
          { event: 'INSERT', schema: 'public', table: 'verification_requests' },
          (payload) => {
            console.log('Yeni talep geldi!', payload.new);
            // Gelen yeni talebi state'e ekleyerek UI'ı güncelle
          }
        )
        .subscribe();
    
      return () => {
        supabase.removeChannel(channel);
      };
    }, []);
    ```
    Bu kod parçası, veritabanına yeni bir kayıt eklendiği anda sayfayı yenilemeden arayüzü güncelleyerek istenen gerçek zamanlı deneyimi sağlar.

// ... existing code ...

## 6. Mobil Zorlama, Kamera Erişimi ve Form Doğrulama 📱📸

### 6.1 Mobil Zorlaması
1. `window.matchMedia('(max-width:768px)')` ve **user-agent** kontrolleriyle cihaz tipi belirlenir.  
2. Masaüstü tespitinde kullanıcı `mobile-only.html` sayfasına yönlendirilir; form bileşenleri render edilmez.

### 6.2 Kamera Zorlaması
- Kimlik: `<input type="file" accept="image/*" capture="environment">`
- Selfie: `<input type="file" accept="image/*" capture="user">`
- Galeri seçimi devre dışıdır; yalnızca kamera açılır.  
- Maksimum dosya boyutu **20 MB**, uzantı `image/jpeg | image/png`.  
- Hata/iptal durumunda toast: **“İşlem başarısız, lütfen tekrar deneyiniz.”**

### 6.3 Form Alan Doğrulama
- Kullanıcı Adı → benzersizlik kontrolü (DB sorgusu).  
- E-posta → RFC 5322 regex, lowercase.  
- Telefon → `libphonenumber-js` (E.164).  
- Ad/Soyad → alfabetik (TR karakter destekli), min 2 karakter.  
- Kurallar `react-hook-form` + MUI `helperText` ile anlık gösterilir.

### 6.4 Hata & Yeniden Deneme
Form state korunur; yalnızca hatalı adım tekrar edilir.

---

## 7. Veritabanı Şeması 🗄️

`verification_requests` ek sütunları:  

| Alan        | Tip          | Açıklama                 |
|-------------|--------------|--------------------------|
| created_at  | timestamptz  | `now()` varsayılan       |
| updated_at  | timestamptz  | trigger ile              |
| reviewed_by | uuid         | admin ID                 |
| reviewed_at | timestamptz  |                          |

Not: Başvurular onay/ret işleminden sonra gerektiğinde manuel olarak silinebilir; uzun süreli saklama zorunluluğu yoktur.

---

## 8. Admin Paneli 🛠️

- **Auth:** Supabase e-posta/şifre. Hesaplar yalnızca **süper admin** tarafından oluşturulur; self-signup kapalı.  
- **Filtreler:**  
  • Durum (pending / approved / rejected)  
  • Tarih aralığı (`created_at`)  
  • Arama (username, e-mail, phone)  
- “Onayla” ve “Reddet” aksiyon metinleri ileride geri alınabilir (undo) desteği için esnek tutulur.

---

## 9. Ortam Değişkenleri (.env) ⚙️
    SUPABASE_URL=
    SUPABASE_SERVICE_ROLE_KEY=
    SUPABASE_ANON_KEY=

Vercel’de aynı adlarla tanımlanır; istemciye yalnız `VITE_` önekli değişkenler sızdırılır.

---

## 10. Güvenlik Sertleştirmeleri 🔐

- **HTTPS** zorunlu + HSTS (`max-age=63072000; includeSubDomains`).  
- **CSP:** `default-src 'self'; img-src https://*.supabase.co data:;`.  
- SameSite=Lax, Secure cookie.  
- Supabase **signed URL**; public bucket yok.  
- API rate-limit: 10 req / min / IP (Edge Function).  
- Sunucu tarafında MIME & boyut kontrolü (20 MB üstü reddedilir).

---

## 11. Test & İzleme ⏭️

Bu sürümde **otomatik test** bulunmamaktadır.  
İzleme: Supabase Log Explorer + Vercel Monitoring.

