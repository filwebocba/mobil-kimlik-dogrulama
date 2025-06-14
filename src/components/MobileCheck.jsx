import './MobileCheck.css'

function MobileCheck() {
  return (
    <div className="mobile-check">
      <div className="mobile-check-container">
        <div className="mobile-check-icon">
          📱
        </div>
        <h1 className="mobile-check-title">
          Mobil Cihaz Gerekli
        </h1>
        <p className="mobile-check-message">
          Bu kimlik doğrulama sistemi yalnızca mobil cihazlardan erişilebilir. 
          Lütfen mobil cihazınızı kullanarak tekrar deneyin.
        </p>
        <div className="mobile-check-features">
          <div className="feature">
            <span className="feature-icon">📷</span>
            <span className="feature-text">Kamera ile selfie</span>
          </div>
          <div className="feature">
            <span className="feature-icon">📄</span>
            <span className="feature-text">Belge fotoğrafı</span>
          </div>
          <div className="feature">
            <span className="feature-icon">🔒</span>
            <span className="feature-text">Güvenli doğrulama</span>
          </div>
        </div>
        <div className="mobile-check-qr">
          <p className="qr-text">
            Mobil cihazınızla QR kodu okutarak erişebilirsiniz:
          </p>
          <div className="qr-placeholder">
            <span className="qr-icon">📱</span>
            <span className="qr-label">QR Kod</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MobileCheck 