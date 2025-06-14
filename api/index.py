"""
Kimlik Doğrulama Sistemi - FastAPI Backend
Ana API endpoint'leri
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
from datetime import datetime
import uuid
import json

# Local imports - ABSOLUTE IMPORTS
from models import (
    VerificationCreate, VerificationResponse, VerificationUpdate, 
    VerificationList, SuccessResponse, ErrorResponse, HealthCheck,
    VerificationStatus
)
from config import settings, get_supabase_client, SupabaseClient
from storage import get_storage_manager, StorageManager

# FastAPI app oluştur
app = FastAPI(
    title="Kimlik Doğrulama Sistemi API",
    description="Mobil KYC (Know Your Customer) sistemi için RESTful API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Trusted host middleware (güvenlik için)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Production'da domain'inizi ekleyin
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    """Güvenlik başlıkları ekle"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP_EXCEPTION",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Genel exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Sunucu hatası oluştu",
            "details": str(exc) if settings.secret_key == "your-secret-key-change-in-production" else None
        }
    )


# === HEALTH CHECK ENDPOINT ===
@app.get("/api/health", response_model=HealthCheck, tags=["System"])
async def health_check(
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """Sistem sağlık kontrolü"""
    try:
        # Veritabanı bağlantısını kontrol et
        db_status = await supabase.health_check()
        
        return HealthCheck(
            status="healthy" if db_status else "unhealthy",
            timestamp=datetime.now(),
            database="connected" if db_status else "disconnected",
            storage="connected"  # Storage her zaman bağlı (Supabase)
        )
    except Exception as e:
        return HealthCheck(
            status="unhealthy",
            timestamp=datetime.now(),
            database="error",
            storage="error"
        )


# === KYC BAŞVURU ENDPOINTS ===
@app.post("/api/verification", response_model=SuccessResponse, tags=["KYC"])
async def submit_verification(
    # Form verileri
    username: str = Form(..., description="Kullanıcı adı"),
    first_name: str = Form(..., description="Ad"),
    last_name: str = Form(..., description="Soyad"),
    email: str = Form(..., description="E-posta"),
    phone: str = Form(..., description="Telefon"),
    
    # Dosya yüklemeleri
    id_document: UploadFile = File(..., description="Kimlik belgesi"),
    selfie: UploadFile = File(..., description="Selfie fotoğrafı"),
    
    # Dependencies
    supabase: SupabaseClient = Depends(get_supabase_client),
    storage: StorageManager = Depends(get_storage_manager)
):
    """KYC başvurusu gönder"""
    try:
        # Form verilerini model ile valide et
        form_data = VerificationCreate(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        
        # Username ve email benzersizlik kontrolü
        if await supabase.check_username_exists(form_data.username):
            raise HTTPException(
                status_code=400,
                detail="Bu kullanıcı adı zaten kullanılıyor"
            )
        
        if await supabase.check_email_exists(form_data.email):
            raise HTTPException(
                status_code=400,
                detail="Bu e-posta adresi zaten kullanılıyor"
            )
        
        # Dosyaları yükle
        id_doc_result = await storage.upload_id_document(id_document, form_data.username)
        selfie_result = await storage.upload_selfie(selfie, form_data.username)
        
        # Veritabanına kaydet
        verification_data = {
            "id": str(uuid.uuid4()),
            "username": form_data.username,
            "first_name": form_data.first_name,
            "last_name": form_data.last_name,
            "email": form_data.email,
            "phone": form_data.phone,
            "id_image_url": id_doc_result["url"],
            "selfie_image_url": selfie_result["url"],
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        response = supabase.client.table('verification_requests').insert(verification_data).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Başvuru kaydedilemedi"
            )
        
        return SuccessResponse(
            message="Kimlik doğrulama başvurunuz başarıyla gönderildi",
            data={
                "id": verification_data["id"],
                "status": "pending",
                "username": form_data.username
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Verification submission error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Başvuru gönderilirken bir hata oluştu"
        )


# === ADMIN PANEL ENDPOINTS ===
@app.get("/api/verifications", response_model=VerificationList, tags=["Admin"])
async def get_verifications(
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    per_page: int = Query(10, ge=1, le=100, description="Sayfa başına kayıt"),
    status: Optional[VerificationStatus] = Query(None, description="Durum filtresi"),
    search: Optional[str] = Query(None, description="Arama terimi"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """Admin paneli için doğrulama taleplerini listele"""
    try:
        # Offset hesapla
        offset = (page - 1) * per_page
        
        # Query builder
        query = supabase.client.table('verification_requests').select('*')
        
        # Filtreler uygula
        if status:
            query = query.eq('status', status.value)
        
        if search:
            # Basit arama (username, email, first_name, last_name)
            search_term = f"%{search}%"
            query = query.or_(
                f"username.ilike.{search_term},"
                f"email.ilike.{search_term},"
                f"first_name.ilike.{search_term},"
                f"last_name.ilike.{search_term}"
            )
        
        # Toplam kayıt sayısını al
        count_response = query.execute()
        total = len(count_response.data) if count_response.data else 0
        
        # Sayfalı veri al
        data_response = query.order('created_at', desc=True).range(offset, offset + per_page - 1).execute()
        
        # Sayfalama bilgileri
        has_next = (offset + per_page) < total
        has_prev = page > 1
        
        return VerificationList(
            items=[VerificationResponse(**item) for item in data_response.data],
            total=total,
            page=page,
            per_page=per_page,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        print(f"Get verifications error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Veriler alınırken bir hata oluştu"
        )


@app.patch("/api/verifications/{verification_id}", response_model=SuccessResponse, tags=["Admin"])
async def update_verification_status(
    verification_id: str,
    update_data: VerificationUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """Doğrulama durumunu güncelle (Onayla/Reddet)"""
    try:
        # Mevcut kaydı kontrol et
        existing = supabase.client.table('verification_requests').select('*').eq('id', verification_id).execute()
        
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Doğrulama talebi bulunamadı"
            )
        
        # Güncelleme verilerini hazırla
        update_payload = {
            "status": update_data.status.value,
            "updated_at": datetime.now().isoformat(),
            "reviewed_at": datetime.now().isoformat()
        }
        
        if update_data.reviewed_by:
            update_payload["reviewed_by"] = update_data.reviewed_by
        
        # Güncelleme yap
        response = supabase.client.table('verification_requests').update(update_payload).eq('id', verification_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Güncelleme yapılamadı"
            )
        
        status_text = {
            "approved": "onaylandı",
            "rejected": "reddedildi"
        }
        
        return SuccessResponse(
            message=f"Doğrulama talebi {status_text.get(update_data.status.value, 'güncellendi')}",
            data=response.data[0]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update verification error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Güncelleme sırasında bir hata oluştu"
        )


@app.get("/api/verifications/{verification_id}", response_model=VerificationResponse, tags=["Admin"])
async def get_verification_detail(
    verification_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """Tek bir doğrulama talebinin detayını getir"""
    try:
        response = supabase.client.table('verification_requests').select('*').eq('id', verification_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Doğrulama talebi bulunamadı"
            )
        
        return VerificationResponse(**response.data[0])
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get verification detail error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Veri alınırken bir hata oluştu"
        )


# === UYGULAMA BAŞLATMA ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 