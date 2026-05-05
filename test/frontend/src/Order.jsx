import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './App.css'

function Order() {
  const [customerName, setCustomerName] = useState('')
  const [item, setItem] = useState('')
  const [quantity, setQuantity] = useState(1)
  const [deliveryAddress, setDeliveryAddress] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setIsLoading(true)

    const token = localStorage.getItem('token')

    try {
      const response = await fetch('http://localhost:8000/submit-order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          customer_name: customerName,
          item: item,
          quantity: parseInt(quantity),
          delivery_address: deliveryAddress
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Order submission failed')
      }

      setSuccess('Order placed successfully!')
      // Clear form
      setCustomerName('')
      setItem('')
      setQuantity(1)
      setDeliveryAddress('')
      
      setTimeout(() => {
        setSuccess('')
      }, 3000)

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>

      <div className="login-card" style={{ maxWidth: '500px' }}>
        <div className="login-header">
          <h1>Place New Order</h1>
          <p>Enter the order details below</p>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="customerName">Customer Name</label>
            <div className="input-wrapper">
              <input
                type="text"
                id="customerName"
                placeholder="Full Name"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="item">Item Name</label>
            <div className="input-wrapper">
              <input
                type="text"
                id="item"
                placeholder="Product Name"
                value={item}
                onChange={(e) => setItem(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="quantity">Quantity</label>
            <div className="input-wrapper">
              <input
                type="number"
                id="quantity"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="deliveryAddress">Delivery Address</label>
            <div className="input-wrapper">
              <textarea
                id="deliveryAddress"
                placeholder="Full delivery address"
                value={deliveryAddress}
                onChange={(e) => setDeliveryAddress(e.target.value)}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Submitting...' : 'Submit Order'}
          </button>
          
          <button
            type="button"
            className="reset-password-btn"
            style={{ marginTop: '0.5rem', width: '100%' }}
            onClick={() => navigate('/dashboard')}
          >
            Back to Dashboard
          </button>
        </form>
      </div>
    </div>
  )
}

export default Order
