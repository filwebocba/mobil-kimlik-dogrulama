import { useState, useEffect } from 'react'
import './App.css'

// Bileşenler
import Header from './components/Header'
import MobileCheck from './components/MobileCheck'
import KYCForm from './components/KYCForm'
import AdminPanel from './components/AdminPanel'
import LoadingSpinner from './components/LoadingSpinner'

function App() {
  const [currentView, setCurrentView] = useState('kyc') // 'kyc' veya 'admin'
  const [isMobile, setIsMobile] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  // Mobil cihaz kontrolü
  useEffect(() => {
    const checkMobile = () => {
      const userAgent = navigator.userAgent.toLowerCase()
      const mobileKeywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone']
      const isMobileUserAgent = mobileKeywords.some(keyword => userAgent.includes(keyword))
      const isSmallScreen = window.innerWidth <= 768
      
      setIsMobile(isMobileUserAgent || isSmallScreen)
      setIsLoading(false)
    }

    checkMobile()
    window.addEventListener('resize', checkMobile)
    
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // Admin panel kontrolü (URL hash ile)
  useEffect(() => {
    const handleHashChange = () => {
      if (window.location.hash === '#admin') {
        setCurrentView('admin')
      } else {
        setCurrentView('kyc')
      }
    }

    handleHashChange()
    window.addEventListener('hashchange', handleHashChange)
    
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  if (isLoading) {
    return <LoadingSpinner />
  }

  // Mobil olmayan cihazlar için erişim engeli
  if (!isMobile && currentView === 'kyc') {
    return <MobileCheck />
  }

  return (
    <div className="app">
      <Header 
        currentView={currentView} 
        onViewChange={setCurrentView}
        isMobile={isMobile}
      />
      
      <main className="main-content">
        {currentView === 'kyc' ? (
          <KYCForm />
        ) : (
          <AdminPanel />
        )}
      </main>
    </div>
  )
}

export default App 