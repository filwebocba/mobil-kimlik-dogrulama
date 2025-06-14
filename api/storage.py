"""
Supabase Storage ile dosya yükleme işlemleri
"""
import os
import uuid
import mimetypes
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
import io
from config import settings, supabase_client


class StorageManager:
    """Dosya yükleme ve depolama yöneticisi"""
    
    def __init__(self):
        self.client = supabase_client.client
    
    def validate_file(self, file: UploadFile) -> bool:
        """Dosya validasyonu"""
        # Dosya boyutu kontrolü
        if file.size > settings.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"Dosya boyutu çok büyük. Maksimum {settings.max_file_size // 1024 // 1024}MB"
            )
        
        # MIME type kontrolü
        if file.content_type not in settings.allowed_mime_types:
            raise HTTPException(
                status_code=415,
                detail=f"Desteklenmeyen dosya tipi. Sadece {', '.join(settings.allowed_mime_types)} desteklenir"
            )
        
        # Dosya uzantısı kontrolü
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        if file_extension not in settings.allowed_extensions:
            raise HTTPException(
                status_code=415,
                detail=f"Desteklenmeyen dosya uzantısı. Sadece {', '.join(settings.allowed_extensions)} desteklenir"
            )
        
        return True
    
    def optimize_image(self, file_content: bytes, max_width: int = 1920, quality: int = 85) -> bytes:
        """Görüntü optimizasyonu"""
        try:
            # PIL ile görüntüyü aç
            image = Image.open(io.BytesIO(file_content))
            
            # EXIF bilgilerini koru ve doğru yönde döndür
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif is not None:
                    for tag, value in exif.items():
                        if tag == 274:  # Orientation tag
                            if value == 3:
                                image = image.rotate(180, expand=True)
                            elif value == 6:
                                image = image.rotate(270, expand=True)
                            elif value == 8:
                                image = image.rotate(90, expand=True)
            
            # Görüntüyü yeniden boyutlandır (orantılı)
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # RGB'ye çevir (eğer RGBA ise)
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Optimize edilmiş görüntüyü kaydet
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            return output.getvalue()
            
        except Exception as e:
            print(f"Görüntü optimizasyon hatası: {e}")
            return file_content  # Hata durumunda orijinal dosyayı döndür
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """Benzersiz dosya adı oluştur"""
        file_extension = original_filename.split('.')[-1].lower() if '.' in original_filename else 'jpg'
        unique_id = str(uuid.uuid4())
        return f"{unique_id}.{file_extension}"
    
    async def upload_file(self, file: UploadFile, bucket_name: str, folder: str = "") -> dict:
        """Dosyayı Supabase Storage'a yükle"""
        try:
            # Dosya validasyonu
            self.validate_file(file)
            
            # Dosya içeriğini oku
            file_content = await file.read()
            
            # Görüntü optimizasyonu
            optimized_content = self.optimize_image(file_content)
            
            # Benzersiz dosya adı oluştur
            filename = self.generate_unique_filename(file.filename)
            file_path = f"{folder}/{filename}" if folder else filename
            
            # Supabase Storage'a yükle
            response = self.client.storage.from_(bucket_name).upload(
                path=file_path,
                file=optimized_content,
                file_options={
                    "content-type": "image/jpeg",
                    "cache-control": "3600"
                }
            )
            
            if response.status_code not in [200, 201]:
                raise HTTPException(
                    status_code=500,
                    detail=f"Dosya yükleme hatası: {response.error}"
                )
            
            # Dosya URL'ini al
            public_url = self.client.storage.from_(bucket_name).get_public_url(file_path)
            
            return {
                "url": public_url,
                "filename": filename,
                "path": file_path,
                "size": len(optimized_content),
                "content_type": "image/jpeg"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Dosya yükleme hatası: {e}")
            raise HTTPException(
                status_code=500,
                detail="Dosya yükleme sırasında bir hata oluştu"
            )
    
    async def upload_id_document(self, file: UploadFile, username: str) -> dict:
        """Kimlik belgesi yükleme"""
        folder = f"documents/{username}"
        return await self.upload_file(file, settings.kyc_documents_bucket, folder)
    
    async def upload_selfie(self, file: UploadFile, username: str) -> dict:
        """Selfie yükleme"""
        folder = f"selfies/{username}"
        return await self.upload_file(file, settings.kyc_selfies_bucket, folder)
    
    async def delete_file(self, bucket_name: str, file_path: str) -> bool:
        """Dosya silme"""
        try:
            response = self.client.storage.from_(bucket_name).remove([file_path])
            return response.status_code == 200
        except Exception as e:
            print(f"Dosya silme hatası: {e}")
            return False
    
    def get_signed_url(self, bucket_name: str, file_path: str, expires_in: int = 3600) -> str:
        """İmzalı URL oluştur (güvenli erişim için)"""
        try:
            response = self.client.storage.from_(bucket_name).create_signed_url(
                file_path, expires_in
            )
            return response.get('signedURL', '')
        except Exception as e:
            print(f"İmzalı URL oluşturma hatası: {e}")
            return ""


# Global storage manager instance
storage_manager = StorageManager()


def get_storage_manager() -> StorageManager:
    """Dependency injection için storage manager'ı döndür"""
    return storage_manager 