# 📱 Mobil Kimlik Doğrulama - Vercel Kurulum Rehberi

## 🚀 Detaylı Vercel Kurulum Adımları

### 1. Ön Hazırlıklar (Tamamlandı ✅)

#### Dosya Yapısı:
```
mobil-kimlik-dogrulama/
├── api/
│   └── index.py          # FastAPI backend
├── src/
│   ├── App.jsx          # React frontend
│   ├── components/      # React bileşenleri
│   └── styles/          # CSS dosyaları
├── public/
│   └── index.html       # Ana HTML dosyası
├── package.json         # Node.js bağımlılıkları
├── requirements.txt     # Python bağımlılıkları
├── vercel.json         # Vercel yapılandırması (Python 3.10)
├── .gitignore          # Git ignore dosyası
└── README.md           # Proje dokümantasyonu
```

### 2. Python 3.10 Runtime Ayarları ✅

`vercel.json` dosyasında Python 3.10 runtime'ı belirtildi:

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.10"
      }
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "runtime": "python3.10"
    }
  }
}
```

### 3. GitHub Repository Oluşturma

#### Adım 1: GitHub'da Yeni Repository
1. https://github.com adresine gidin
2. "New repository" butonuna tıklayın
3. Repository adı: `mobil-kimlik-dogrulama`
4. Public olarak ayarlayın
5. README, .gitignore ve license eklemeyin (zaten var)
6. "Create repository" butonuna tıklayın

#### Adım 2: Yerel Git Repository'yi GitHub'a Bağlama
Terminal'de şu komutları çalıştırın:

```powershell
# Git repository'sini başlat
git init

# Dosyaları ekle
git add .

# İlk commit
git commit -m "İlk commit: Mobil kimlik doğrulama sistemi"

# GitHub repository'sini remote olarak ekle
git remote add origin https://github.com/KULLANICI_ADINIZ/mobil-kimlik-dogrulama.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a push et
git push -u origin main
```

### 4. Vercel Hesabı ve Proje Kurulumu

#### Adım 1: Vercel Hesabı
1. https://vercel.com adresine gidin
2. "Sign Up" butonuna tıklayın
3. GitHub hesabınızla giriş yapın
4. Gerekli izinleri verin

#### Adım 2: Proje Import Etme
1. Vercel dashboard'da "New Project" butonuna tıklayın
2. GitHub'dan `mobil-kimlik-dogrulama` repository'sini seçin
3. "Import" butonuna tıklayın

#### Adım 3: Proje Ayarları
1. **Framework Preset**: "Other" seçin
2. **Root Directory**: Boş bırakın (root)
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`
5. **Install Command**: `npm install`

### 5. Environment Variables (Çevre Değişkenleri)

Vercel'de projenizin ayarlarından Environment Variables bölümüne gidin ve şu değişkenleri ekleyin:

#### Production Environment:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
```

#### Development ve Preview Environment:
Aynı değerleri Development ve Preview ortamları için de ekleyin.

### 6. Supabase Ayarları

#### Supabase Dashboard:
1. https://supabase.com/dashboard adresine gidin
2. Projenizin ayarlarına gidin
3. API sekmesinden şu bilgileri alın:
   - **Project URL**: `SUPABASE_URL` için
   - **anon public**: `SUPABASE_KEY` için
   - **service_role**: `SUPABASE_SERVICE_KEY` için

#### Supabase URL Settings:
1. Authentication > URL Configuration
2. **Site URL**: `https://your-vercel-app.vercel.app`
3. **Redirect URLs**: `https://your-vercel-app.vercel.app/**`

### 7. Deploy İşlemi

#### Otomatik Deploy:
- GitHub'a her push işleminde Vercel otomatik olarak deploy yapacak
- Production branch: `main`
- Preview branch: Diğer tüm branch'ler

#### Manuel Deploy:
```powershell
# Vercel CLI kurulumu (opsiyonel)
npm i -g vercel

# Manuel deploy
vercel --prod
```

### 8. Domain Ayarları (Opsiyonel)

#### Custom Domain:
1. Vercel dashboard'da projenizi seçin
2. "Settings" > "Domains" bölümüne gidin
3. Kendi domain'inizi ekleyin
4. DNS ayarlarını güncelleyin

### 9. SSL ve Güvenlik

#### Otomatik SSL:
- Vercel otomatik olarak SSL sertifikası sağlar
- HTTPS zorunlu
- HTTP trafiği otomatik olarak HTTPS'e yönlendirilir

#### Güvenlik Headers:
`vercel.json` dosyasında güvenlik headers'ları eklenmiş:
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

### 10. Test ve Doğrulama

#### Deploy Sonrası Kontroller:
1. **Frontend**: `https://your-app.vercel.app`
2. **Backend API**: `https://your-app.vercel.app/api/health`
3. **Admin Panel**: `https://your-app.vercel.app` (desktop'ta)

#### Test Endpoints:
```bash
# Health check
curl https://your-app.vercel.app/api/health

# Admin panel (token gerekli)
curl -H "Authorization: Bearer test-admin-token" https://your-app.vercel.app/api/verifications
```

### 11. Monitoring ve Logs

#### Vercel Dashboard:
1. **Functions** sekmesi: API logları
2. **Analytics** sekmesi: Trafik analizi
3. **Speed Insights**: Performance metrikleri

#### Log Görüntüleme:
```powershell
# Vercel CLI ile logları görüntüleme
vercel logs
```

### 12. Sorun Giderme

#### Yaygın Sorunlar:

1. **Python Runtime Hatası**:
   - `vercel.json`'da Python 3.10 belirtildiğinden emin olun
   - `requirements.txt` dosyasının root dizinde olduğunu kontrol edin

2. **Environment Variables**:
   - Tüm ortamlar için (Production, Preview, Development) ayarlandığından emin olun
   - Değişken adlarında typo olmadığını kontrol edin

3. **CORS Hatası**:
   - FastAPI'da CORS middleware'i doğru yapılandırıldığından emin olun
   - Supabase'de URL ayarlarını kontrol edin

4. **Build Hatası**:
   - `package.json` dosyasındaki scripts'leri kontrol edin
   - Node.js dependencies'lerin doğru olduğunu kontrol edin

### 13. Güncelleme ve Bakım

#### Kod Güncellemeleri:
```powershell
# Değişiklikleri commit et
git add .
git commit -m "Özellik: Yeni güncelleme"
git push origin main
```

#### Vercel Otomatik Deploy:
- Her push işleminde otomatik deploy
- Build logs'u Vercel dashboard'da görüntülenebilir
- Rollback özelliği mevcut

---

## 🎯 Sonuç

Bu rehberi takip ederek projenizi başarıyla Vercel'e deploy edebilirsiniz. Python 3.10 runtime'ı ile FastAPI backend'iniz ve React frontend'iniz tam olarak çalışacaktır.

### 📞 Destek
- Vercel Documentation: https://vercel.com/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- Supabase Documentation: https://supabase.com/docs

**Başarılar! 🚀** 