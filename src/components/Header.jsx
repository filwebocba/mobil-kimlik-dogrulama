import './Header.css'

function Header({ currentView, onViewChange, isMobile }) {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <h1 className="header-title">
            <span className="header-icon">🛡️</span>
            Kimlik Doğrulama
          </h1>
        </div>
        
        <div className="header-right">
          {currentView === 'kyc' ? (
            <button 
              className="admin-button"
              onClick={() => onViewChange('admin')}
              aria-label="Admin paneline git"
            >
              <span className="admin-icon">⚙️</span>
              {isMobile ? '' : 'Admin'}
            </button>
          ) : (
            <button 
              className="kyc-button"
              onClick={() => onViewChange('kyc')}
              aria-label="KYC formuna git"
            >
              <span className="back-icon">←</span>
              {isMobile ? '' : 'Geri'}
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header 