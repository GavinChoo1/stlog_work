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

      <div className="login-card">
        <div className="login-header">
          <h1>Welcome, {username}!</h1>
          <p>You are now logged in.</p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '2rem' }}>
          <button
            className="login-button"
            onClick={() => navigate('/update-password')}
          >
            Update Password
          </button>

          <button
            className="reset-password-btn"
            onClick={handleLogout}
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
