"""
Uygulama konfigürasyonu ve Supabase bağlantısı
"""
import os
from typing import Optional, List
from dotenv import load_dotenv
from supabase import create_client, Client

# .env dosyasını yükle
load_dotenv()


class Settings:
    """Uygulama ayarları"""
    
    def __init__(self):
        # Supabase ayarları
        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        self.supabase_anon_key = os.getenv("SUPABASE_ANON_KEY", "")
        
        # Güvenlik ayarları
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        
        # Dosya yükleme ayarları
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE", str(20 * 1024 * 1024)))  # 20MB
        self.allowed_extensions = ["jpg", "jpeg", "png"]
        self.allowed_mime_types = ["image/jpeg", "image/png"]
        
        # Storage bucket isimleri
        self.kyc_documents_bucket = os.getenv("KYC_DOCUMENTS_BUCKET", "kyc-documents")
        self.kyc_selfies_bucket = os.getenv("KYC_SELFIES_BUCKET", "kyc-selfies")
        
        # Sayfalama ayarları
        self.default_page_size = int(os.getenv("DEFAULT_PAGE_SIZE", "10"))
        self.max_page_size = int(os.getenv("MAX_PAGE_SIZE", "100"))
        
        # CORS ayarları
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        self.cors_origins = cors_origins_str.split(",") if cors_origins_str else ["*"]
        
        # Rate limiting
        self.rate_limit_requests = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
        self.rate_limit_window = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    def validate(self) -> List[str]:
        """Konfigürasyon validasyonu"""
        errors = []
        
        if not self.supabase_url:
            errors.append("SUPABASE_URL environment variable gerekli")
        elif not self.supabase_url.startswith('https://'):
            errors.append("SUPABASE_URL https:// ile başlamalıdır")
            
        if not self.supabase_service_role_key:
            errors.append("SUPABASE_SERVICE_ROLE_KEY environment variable gerekli")
            
        if not self.supabase_anon_key:
            errors.append("SUPABASE_ANON_KEY environment variable gerekli")
        
        return errors


# Global settings instance
settings = Settings()

# Konfigürasyon validasyonu
config_errors = settings.validate()
if config_errors:
    print("🚨 Konfigürasyon Hataları:")
    for error in config_errors:
        print(f"  - {error}")
    print("\n💡 .env dosyanızı kontrol edin ve gerekli değerleri ekleyin.")
    print("📝 env.example dosyasını .env olarak kopyalayıp değerleri doldurun.")


class SupabaseClient:
    """Supabase client wrapper"""
    
    def __init__(self):
        self._client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Supabase client'ı döndür"""
        if self._client is None:
            if not settings.supabase_url or not settings.supabase_service_role_key:
                raise ValueError("Supabase konfigürasyonu eksik. .env dosyasını kontrol edin.")
            
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
        return self._client
    
    async def health_check(self) -> bool:
        """Supabase bağlantısını kontrol et"""
        try:
            # Basit bir sorgu ile bağlantıyı test et
            response = self.client.table('verification_requests').select('count').limit(1).execute()
            return True
        except Exception as e:
            print(f"Supabase bağlantı hatası: {e}")
            return False
    
    async def check_username_exists(self, username: str) -> bool:
        """Kullanıcı adının var olup olmadığını kontrol et"""
        try:
            response = self.client.table('verification_requests').select('id').eq('username', username).limit(1).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Username kontrol hatası: {e}")
            return False
    
    async def check_email_exists(self, email: str) -> bool:
        """E-posta adresinin var olup olmadığını kontrol et"""
        try:
            response = self.client.table('verification_requests').select('id').eq('email', email).limit(1).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Email kontrol hatası: {e}")
            return False


# Global Supabase client instance
supabase_client = SupabaseClient()


def get_supabase_client() -> SupabaseClient:
    """Dependency injection için Supabase client'ı döndür"""
    return supabase_client 