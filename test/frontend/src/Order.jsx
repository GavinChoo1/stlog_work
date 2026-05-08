import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './App.css'

function Order() {
  const initialFormState = {
    id: '',
    vertical_id: '',
    project_id: '',
    delivery_order_id: '',
    zone_id: '',
    start_point_id: '',
    end_point_id: '',
    vehicle_id: '',
    repeat_direction_id: '',
    vehicle_task_id: '',
    courier_ms_job_id: '',
    packing_task_id: '',
    name: '',
    description: '',
    start_date_time: '',
    delivery_date: '',
    duration: '',
    start_point_instruction: '',
    end_point_instruction: '',
    tags: '',
    error_description: '',
    closure_reason: '',
    group_code: '',
    group_name: '',
    do_number: '',
    end_point_code: '',
    is_product_code_scan_enabled: false,
    is_customer_card_scan_enabled: false,
    is_nric_scan_enabled: false,
    is_sending_email: false,
    is_sending_sms: false,
    is_sent_email: false,
    is_rescheduled: false,
    is_courier_ms: false,
    external_updated_date_time: '',
    epod_distance_meter: '',
    priority: '',
    task_status: '',
    file_uploaded_count: '',
    require_start_point_epod: false,
    require_end_point_epod: false,
    parent_id: '',
    route_plan_no: '',
    delivery_route_plan_date_time: '',
    is_sent_consolidated_email: false,
    sensitive_do: false,
    created_date_time: '',
    modified_date_time: '',
    created_user_id: '',
    modified_user_id: ''
  }

  const [formData, setFormData] = useState(initialFormState)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleInputChange = (e) => {
    const { id, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [id]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setIsLoading(true)

    const token = localStorage.getItem('token')

    // Clean data for API (convert numbers)
    const cleanedData = { ...formData }
    const numericFields = [
      'id', 'vertical_id', 'project_id', 'delivery_order_id', 'zone_id', 
      'start_point_id', 'end_point_id', 'vehicle_id', 'repeat_direction_id', 
      'vehicle_task_id', 'courier_ms_job_id', 'packing_task_id', 'priority', 
      'task_status', 'file_uploaded_count', 'parent_id', 'epod_distance_meter'
    ]
    
    numericFields.forEach(field => {
      if (cleanedData[field] === '') {
        cleanedData[field] = null
      } else {
        cleanedData[field] = field === 'epod_distance_meter' 
          ? parseFloat(cleanedData[field]) 
          : parseInt(cleanedData[field])
      }
    })

    // Handle timestamps
    const timestampFields = [
      'start_date_time', 'delivery_date', 'external_updated_date_time', 
      'delivery_route_plan_date_time', 'created_date_time', 'modified_date_time'
    ]
    timestampFields.forEach(field => {
      if (cleanedData[field] === '') cleanedData[field] = null
    })

    try {
      const response = await fetch('http://localhost:8000/submit-order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(cleanedData),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Order submission failed')
      }

      setSuccess('Operation Order recorded successfully!')
      setFormData(initialFormState)
      
      setTimeout(() => setSuccess(''), 3000)

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const renderInput = (id, label, type = 'text', required = false) => (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <div className="input-wrapper">
        <input
          type={type}
          id={id}
          value={formData[id]}
          onChange={handleInputChange}
          required={required}
          step={type === 'number' && id === 'epod_distance_meter' ? 'any' : '1'}
        />
      </div>
    </div>
  )

  const renderCheckbox = (id, label) => (
    <label className="checkbox-item" key={id}>
      <input
        type="checkbox"
        id={id}
        checked={formData[id]}
        onChange={handleInputChange}
      />
      {label}
    </label>
  )

  return (
    <div className="login-container">
      <div className="bg-blob blob-1"></div>
      <div className="bg-blob blob-2"></div>

      <div className="login-card order-card">
        <div className="login-header">
          <h1>HC Operation Order</h1>
          <p>Complete the operation order details below</p>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <form onSubmit={handleSubmit}>
          
          <div className="form-section">
            <h3>Core Information</h3>
            <div className="form-grid">
              {renderInput('id', 'Order ID', 'number', true)}
              {renderInput('name', 'Order Name')}
              {renderInput('do_number', 'DO Number')}
              {renderInput('priority', 'Priority', 'number')}
              {renderInput('task_status', 'Task Status', 'number')}
              <div className="form-group full-width">
                <label htmlFor="description">Description</label>
                <textarea id="description" value={formData.description} onChange={handleInputChange} />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Locations & Instructions</h3>
            <div className="form-grid">
              {renderInput('zone_id', 'Zone ID', 'number')}
              {renderInput('start_point_id', 'Start Point ID', 'number')}
              {renderInput('end_point_id', 'End Point ID', 'number')}
              {renderInput('end_point_code', 'End Point Code')}
              <div className="form-group">
                <label htmlFor="start_point_instruction">Start Point Instruction</label>
                <textarea id="start_point_instruction" value={formData.start_point_instruction} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label htmlFor="end_point_instruction">End Point Instruction</label>
                <textarea id="end_point_instruction" value={formData.end_point_instruction} onChange={handleInputChange} />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Logistics & Assignment</h3>
            <div className="form-grid">
              {renderInput('vertical_id', 'Vertical ID', 'number')}
              {renderInput('project_id', 'Project ID', 'number')}
              {renderInput('vehicle_id', 'Vehicle ID', 'number')}
              {renderInput('vehicle_task_id', 'Vehicle Task ID', 'number')}
              {renderInput('courier_ms_job_id', 'Courier MS Job ID', 'number')}
              {renderInput('packing_task_id', 'Packing Task ID', 'number')}
              {renderInput('route_plan_no', 'Route Plan No')}
              {renderInput('parent_id', 'Parent ID', 'number')}
            </div>
          </div>

          <div className="form-section">
            <h3>Dates & Schedule</h3>
            <div className="form-grid">
              {renderInput('start_date_time', 'Start Date Time', 'datetime-local')}
              {renderInput('delivery_date', 'Delivery Date', 'datetime-local')}
              {renderInput('delivery_route_plan_date_time', 'Route Plan Date Time', 'datetime-local')}
              {renderInput('external_updated_date_time', 'External Updated Time', 'datetime-local')}
              {renderInput('duration', 'Duration')}
            </div>
          </div>

          <div className="form-section">
            <h3>Settings & Flags</h3>
            <div className="checkbox-group">
              {renderCheckbox('is_product_code_scan_enabled', 'Product Scan')}
              {renderCheckbox('is_customer_card_scan_enabled', 'Customer Card Scan')}
              {renderCheckbox('is_nric_scan_enabled', 'NRIC Scan')}
              {renderCheckbox('is_sending_email', 'Send Email')}
              {renderCheckbox('is_sending_sms', 'Send SMS')}
              {renderCheckbox('is_sent_email', 'Email Sent')}
              {renderCheckbox('is_rescheduled', 'Rescheduled')}
              {renderCheckbox('is_courier_ms', 'Courier MS')}
              {renderCheckbox('require_start_point_epod', 'Req Start EPOD')}
              {renderCheckbox('require_end_point_epod', 'Req End EPOD')}
              {renderCheckbox('is_sent_consolidated_email', 'Consolidated Email')}
              {renderCheckbox('sensitive_do', 'Sensitive DO')}
            </div>
          </div>

          <div className="form-section">
            <h3>Additional Data</h3>
            <div className="form-grid">
              {renderInput('epod_distance_meter', 'EPOD Distance (m)', 'number')}
              {renderInput('file_uploaded_count', 'Files Uploaded', 'number')}
              {renderInput('tags', 'Tags')}
              {renderInput('group_code', 'Group Code')}
              {renderInput('group_name', 'Group Name')}
              {renderInput('closure_reason', 'Closure Reason')}
              <div className="form-group full-width">
                <label htmlFor="error_description">Error Description</label>
                <textarea id="error_description" value={formData.error_description} onChange={handleInputChange} />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Audit</h3>
            <div className="form-grid">
              {renderInput('created_user_id', 'Created By')}
              {renderInput('modified_user_id', 'Modified By')}
              {renderInput('created_date_time', 'Created Date', 'datetime-local')}
              {renderInput('modified_date_time', 'Modified Date', 'datetime-local')}
            </div>
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? 'Submitting...' : 'Submit Operation Order'}
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

