-- Kimlik Doğrulama Sistemi - Veritabanı Şeması
-- Bu dosyayı Supabase SQL Editor'da çalıştırın

-- 1. ENUM tipini oluştur
CREATE TYPE verification_status AS ENUM ('pending', 'approved', 'rejected');

-- 2. Ana tabloyu oluştur
CREATE TABLE verification_requests (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    id_image_url TEXT NOT NULL,
    selfie_image_url TEXT NOT NULL,
    status verification_status DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_by UUID REFERENCES auth.users(id),
    reviewed_at TIMESTAMPTZ,
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_phone CHECK (phone ~* '^\+?[1-9]\d{1,14}$')
);

-- 3. Indexes oluştur (performans için)
CREATE INDEX idx_verification_requests_status ON verification_requests(status);
CREATE INDEX idx_verification_requests_created_at ON verification_requests(created_at);
CREATE INDEX idx_verification_requests_username ON verification_requests(username);
CREATE INDEX idx_verification_requests_email ON verification_requests(email);

-- 4. Updated_at trigger'ı oluştur
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_verification_requests_updated_at 
    BEFORE UPDATE ON verification_requests 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 5. Row Level Security (RLS) aktif et
ALTER TABLE verification_requests ENABLE ROW LEVEL SECURITY;

-- 6. RLS Policies oluştur

-- Policy 1: Sadece service_role INSERT yapabilir (backend için)
CREATE POLICY "Service role can insert" ON verification_requests
    FOR INSERT WITH CHECK (auth.role() = 'service_role');

-- Policy 2: Sadece service_role UPDATE yapabilir (backend için)
CREATE POLICY "Service role can update" ON verification_requests
    FOR UPDATE USING (auth.role() = 'service_role');

-- Policy 3: Authenticated kullanıcılar okuyabilir (admin paneli için)
CREATE POLICY "Authenticated users can read" ON verification_requests
    FOR SELECT USING (auth.role() = 'authenticated');

-- 7. Admin kullanıcıları için profile tablosu oluştur
CREATE TABLE admin_profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'admin',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Admin profiles için RLS
ALTER TABLE admin_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own profile" ON admin_profiles
    FOR SELECT USING (auth.uid() = id);

-- 9. Real-time subscription için publication oluştur
-- Bu, admin panelinin gerçek zamanlı güncellemeler almasını sağlar
DROP PUBLICATION IF EXISTS supabase_realtime;
CREATE PUBLICATION supabase_realtime FOR ALL TABLES;

-- 10. Test verisi ekle (opsiyonel - silebilirsiniz)
-- INSERT INTO verification_requests (
--     username, first_name, last_name, email, phone, 
--     id_image_url, selfie_image_url
-- ) VALUES (
--     'test_user', 'Test', 'User', 'test@example.com', '+905551234567',
--     'https://example.com/id.jpg', 'https://example.com/selfie.jpg'
-- );

-- İşlem tamamlandı!
SELECT 'Veritabanı şeması başarıyla oluşturuldu!' as message; 