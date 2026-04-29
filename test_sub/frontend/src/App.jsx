import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './Login'
import ResetPassword from './ResetPassword'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/reset-password" element={<ResetPassword />} />
      </Routes>
    </Router>
  )
}

export default App
