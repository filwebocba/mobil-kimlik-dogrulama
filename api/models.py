"""
Pydantic modelleri - API için veri validasyonu
"""
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import re


class VerificationStatus(str, Enum):
    """Doğrulama durumu enum'u"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class VerificationBase(BaseModel):
    """Temel doğrulama modeli"""
    username: str = Field(..., min_length=3, max_length=50, description="Kullanıcı adı")
    first_name: str = Field(..., min_length=2, max_length=100, description="Ad")
    last_name: str = Field(..., min_length=2, max_length=100, description="Soyad")
    email: EmailStr = Field(..., description="E-posta adresi")
    phone: str = Field(..., min_length=10, max_length=20, description="Telefon numarası")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Kullanıcı adı validasyonu"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Kullanıcı adı sadece harf, rakam, tire ve alt tire içerebilir')
        return v.lower()
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        """Ad ve soyad validasyonu"""
        if not re.match(r'^[a-zA-ZğĞıİöÖüÜşŞçÇ\s]+$', v):
            raise ValueError('Ad ve soyad sadece harf içerebilir')
        return v.title()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        """Telefon numarası validasyonu (E.164 formatı)"""
        # Basit validasyon, üretimde libphonenumber kullanılacak
        phone_pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(phone_pattern, v.replace(' ', '').replace('-', '')):
            raise ValueError('Geçerli bir telefon numarası giriniz')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email_lowercase(cls, v):
        """E-posta adresini küçük harfe çevir"""
        return str(v).lower()


class VerificationCreate(VerificationBase):
    """Doğrulama isteği oluşturma modeli"""
    pass


class VerificationResponse(VerificationBase):
    """Doğrulama isteği yanıt modeli"""
    id: str
    status: VerificationStatus
    id_image_url: Optional[str] = None
    selfie_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class VerificationUpdate(BaseModel):
    """Doğrulama durumu güncelleme modeli"""
    status: VerificationStatus
    reviewed_by: Optional[str] = None
    
    class Config:
        from_attributes = True


class VerificationList(BaseModel):
    """Doğrulama listesi modeli"""
    items: List[VerificationResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


class FileUploadResponse(BaseModel):
    """Dosya yükleme yanıt modeli"""
    url: str
    filename: str
    size: int
    content_type: str


class ErrorResponse(BaseModel):
    """Hata yanıt modeli"""
    error: str
    message: str
    details: Optional[dict] = None


class SuccessResponse(BaseModel):
    """Başarı yanıt modeli"""
    success: bool = True
    message: str
    data: Optional[dict] = None


class HealthCheck(BaseModel):
    """Sağlık kontrol modeli"""
    status: str = "healthy"
    timestamp: datetime
    version: str = "1.0.0"
    database: str = "connected"
    storage: str = "connected" 