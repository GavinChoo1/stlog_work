import { useNavigate } from 'react-router-dom'
import './App.css'

function Dashboard() {
  const navigate = useNavigate()
  const username = localStorage.getItem('username')

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    navigate('/')
  }

  return (
    <div className="login-container">
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>

      <div className="login-card" style={{ maxWidth: '600px' }}>
        <div className="login-header">
          <h1>Welcome, {username}!</h1>
          <p>You are now logged in.</p>
        </div>

        <div className="dashboard-actions">
          <div 
            className="action-card"
            onClick={() => navigate('/order')}
          >
            <div className="action-icon">📝</div>
            <h3>Fill New Order</h3>
            <p>Submit a new transport request</p>
          </div>

          <div 
            className="action-card"
            onClick={() => navigate('/update-password')}
          >
            <div className="action-icon">🔐</div>
            <h3>Update Password</h3>
            <p>Secure your account</p>
          </div>
        </div>

        <button
          className="reset-password-btn"
          onClick={handleLogout}
          style={{ marginTop: '2rem' }}
        >
          Sign Out
        </button>
      </div>
    </div>
  )
}

export default Dashboard
