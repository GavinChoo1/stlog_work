import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './Login'
import Dashboard from './Dashboard'
import UpdatePassword from './UpdatePassword'
import Order from './Order'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/update-password" element={<UpdatePassword />} />
        <Route path="/order" element={<Order />} />
      </Routes>
    </Router>
  )
}

export default App
