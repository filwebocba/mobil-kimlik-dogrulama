import { useState, useEffect } from 'react'
import './AdminPanel.css'
import LoadingSpinner from './LoadingSpinner'

function AdminPanel() {
  const [verifications, setVerifications] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedVerification, setSelectedVerification] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [authToken, setAuthToken] = useState('')

  // Basit authentication
  const handleAuth = () => {
    if (authToken === 'admin123') {
      setIsAuthenticated(true)
      fetchVerifications()
    } else {
      alert('Geçersiz token!')
    }
  }

  // Verification'ları çek
  const fetchVerifications = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/verifications', {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setVerifications(data.items || [])
      }
    } catch (error) {
      console.error('Verifikasyonlar yüklenemedi:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Status güncelle
  const updateStatus = async (id, status) => {
    try {
      const response = await fetch(`/api/verifications/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
          status: status,
          reviewed_by: 'admin'
        })
      })
      
      if (response.ok) {
        fetchVerifications()
        setSelectedVerification(null)
      }
    } catch (error) {
      console.error('Status güncellenemedi:', error)
    }
  }

  // Giriş yapmamışsa login formu göster
  if (!isAuthenticated) {
    return (
      <div className="admin-login">
        <div className="login-form">
          <h2>Admin Girişi</h2>
          <div className="form-group">
            <label>Auth Token:</label>
            <input
              type="password"
              value={authToken}
              onChange={(e) => setAuthToken(e.target.value)}
              placeholder="Token giriniz"
            />
          </div>
          <button onClick={handleAuth} className="btn btn-primary">
            Giriş Yap
          </button>
          <p className="login-hint">Test token: admin123</p>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return <LoadingSpinner message="Verifikasyonlar yükleniyor..." />
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h2>Admin Paneli</h2>
        <div className="admin-stats">
          <div className="stat">
            <span className="stat-number">{verifications.length}</span>
            <span className="stat-label">Toplam Başvuru</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {verifications.filter(v => v.status === 'pending').length}
            </span>
            <span className="stat-label">Bekleyen</span>
          </div>
          <div className="stat">
            <span className="stat-number">
              {verifications.filter(v => v.status === 'approved').length}
            </span>
            <span className="stat-label">Onaylanan</span>
          </div>
        </div>
      </div>

      <div className="verification-list">
        {verifications.length === 0 ? (
          <div className="empty-state">
            <p>Henüz başvuru bulunmuyor.</p>
          </div>
        ) : (
          verifications.map(verification => (
            <div 
              key={verification.id} 
              className={`verification-item ${verification.status}`}
              onClick={() => setSelectedVerification(verification)}
            >
              <div className="verification-info">
                <h3>{verification.first_name} {verification.last_name}</h3>
                <p>{verification.email}</p>
                <p>{verification.phone}</p>
                <span className={`status-badge ${verification.status}`}>
                  {verification.status === 'pending' && '⏳ Bekliyor'}
                  {verification.status === 'approved' && '✅ Onaylandı'}
                  {verification.status === 'rejected' && '❌ Reddedildi'}
                </span>
              </div>
              <div className="verification-date">
                {new Date(verification.created_at).toLocaleDateString('tr-TR')}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal */}
      {selectedVerification && (
        <div className="modal-overlay" onClick={() => setSelectedVerification(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Başvuru Detayı</h3>
              <button 
                className="modal-close"
                onClick={() => setSelectedVerification(null)}
              >
                ×
              </button>
            </div>
            
            <div className="modal-content">
              <div className="verification-details">
                <div className="detail-section">
                  <h4>Kişisel Bilgiler</h4>
                  <p><strong>Ad Soyad:</strong> {selectedVerification.first_name} {selectedVerification.last_name}</p>
                  <p><strong>Kullanıcı Adı:</strong> {selectedVerification.username}</p>
                  <p><strong>E-posta:</strong> {selectedVerification.email}</p>
                  <p><strong>Telefon:</strong> {selectedVerification.phone}</p>
                  <p><strong>Durum:</strong> 
                    <span className={`status-badge ${selectedVerification.status}`}>
                      {selectedVerification.status === 'pending' && 'Bekliyor'}
                      {selectedVerification.status === 'approved' && 'Onaylandı'}
                      {selectedVerification.status === 'rejected' && 'Reddedildi'}
                    </span>
                  </p>
                </div>

                <div className="detail-section">
                  <h4>Belgeler</h4>
                  <div className="document-images">
                    {selectedVerification.id_image_url && (
                      <div className="document-image">
                        <h5>Kimlik Belgesi</h5>
                        <img 
                          src={selectedVerification.id_image_url} 
                          alt="Kimlik belgesi"
                          onError={(e) => e.target.style.display = 'none'}
                        />
                      </div>
                    )}
                    
                    {selectedVerification.selfie_image_url && (
                      <div className="document-image">
                        <h5>Selfie</h5>
                        <img 
                          src={selectedVerification.selfie_image_url} 
                          alt="Selfie"
                          onError={(e) => e.target.style.display = 'none'}
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
            
            {selectedVerification.status === 'pending' && (
              <div className="modal-actions">
                <button 
                  className="btn btn-success"
                  onClick={() => updateStatus(selectedVerification.id, 'approved')}
                >
                  ✅ Onayla
                </button>
                <button 
                  className="btn btn-danger"
                  onClick={() => updateStatus(selectedVerification.id, 'rejected')}
                >
                  ❌ Reddet
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminPanel 