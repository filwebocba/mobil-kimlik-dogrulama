import { useState } from 'react'
import './KYCForm.css'

function KYCForm() {
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: ''
  })
  
  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setIsSubmitted(true)
  }

  if (isSubmitted) {
    return (
      <div className="kyc-success">
        <div className="success-icon">✅</div>
        <h2>Başvuru Gönderildi!</h2>
        <p>Kimlik doğrulama başvurunuz başarıyla gönderildi.</p>
        <button 
          className="btn btn-primary"
          onClick={() => setIsSubmitted(false)}
        >
          Yeni Başvuru Yap
        </button>
      </div>
    )
  }

  return (
    <div className="kyc-form">
      <div className="form-header">
        <h2>Kimlik Doğrulama Formu</h2>
        <p>Lütfen tüm bilgileri eksiksiz doldurun</p>
      </div>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="form-section">
          <h3>Kişisel Bilgiler</h3>
          
          <div className="form-group">
            <label htmlFor="username">Kullanıcı Adı *</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Kullanıcı adınızı girin"
              required
            />
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">Ad *</label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleInputChange}
                placeholder="Adınız"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="last_name">Soyad *</label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleInputChange}
                placeholder="Soyadınız"
                required
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="email">E-posta *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="email@ornek.com"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="phone">Telefon *</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleInputChange}
              placeholder="05xxxxxxxxx"
              required
            />
          </div>
        </div>
        
        <div className="form-footer">
          <button type="submit" className="btn btn-primary btn-large">
            Başvuru Gönder
          </button>
        </div>
      </form>
    </div>
  )
}

export default KYCForm 