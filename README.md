# 🛡️ Mobil Kimlik Doğrulama Sistemi

Mobil-first KYC (Know Your Customer) kimlik doğrulama sistemi.

## 🚀 Özellikler

- **Mobil-only erişim** - Desktop cihazlardan erişim engellendi
- **Kamera entegrasyonu** - Kimlik belgesi ve selfie çekimi
- **Real-time admin paneli** - Başvuru onay/red sistemi
- **Güvenli dosya depolama** - Supabase Storage
- **Modern UI** - React + CSS Grid/Flexbox

## 🏗️ Teknolojiler

### Backend
- **FastAPI** - Python web framework
- **Supabase** - Database + Storage
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **CSS3** - Modern styling

## 🌐 Demo

- **Frontend**: [https://YOUR-VERCEL-URL.vercel.app](https://YOUR-VERCEL-URL.vercel.app)
- **API Docs**: [https://YOUR-VERCEL-URL.vercel.app/docs](https://YOUR-VERCEL-URL.vercel.app/docs)
- **Admin Panel**: [https://YOUR-VERCEL-URL.vercel.app#admin](https://YOUR-VERCEL-URL.vercel.app#admin)

## 🔑 Admin Giriş

Admin token: `admin123`

## 📱 Kullanım

1. Mobil cihazınızla siteye girin
2. Kimlik doğrulama formunu doldurun
3. Kimlik belgesi ve selfie fotoğrafı çekin
4. Başvurunuzu gönderin
5. Admin panelinden başvuru durumunu takip edin

## 🛠️ Local Development

```bash
# Backend
cd api
pip install -r requirements.txt
uvicorn index:app --reload

# Frontend  
npm install
npm run dev
```

## 📋 Environment Variables

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_SERVICE_KEY=your_service_key
```

## 📄 Lisans

MIT License 