from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from funcs.auth_func import auth_check, reset_password_in_db

class LoginRequest(BaseModel):
    username: str
    password: str

class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str

from typing import Optional
from datetime import datetime

class OrderRequest(BaseModel):
    id: int
    vertical_id: Optional[int] = None
    project_id: Optional[int] = None
    delivery_order_id: Optional[int] = None
    zone_id: Optional[int] = None
    start_point_id: Optional[int] = None
    end_point_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    repeat_direction_id: Optional[int] = None
    vehicle_task_id: Optional[int] = None
    courier_ms_job_id: Optional[int] = None
    packing_task_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    start_date_time: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    duration: Optional[str] = None
    start_point_instruction: Optional[str] = None
    end_point_instruction: Optional[str] = None
    tags: Optional[str] = None
    error_description: Optional[str] = None
    closure_reason: Optional[str] = None
    group_code: Optional[str] = None
    group_name: Optional[str] = None
    do_number: Optional[str] = None
    end_point_code: Optional[str] = None
    is_product_code_scan_enabled: Optional[bool] = None
    is_customer_card_scan_enabled: Optional[bool] = None
    is_nric_scan_enabled: Optional[bool] = None
    is_sending_email: Optional[bool] = None
    is_sending_sms: Optional[bool] = None
    is_sent_email: Optional[bool] = None
    is_rescheduled: Optional[bool] = None
    is_courier_ms: Optional[bool] = None
    external_updated_date_time: Optional[datetime] = None
    epod_distance_meter: Optional[float] = None
    priority: Optional[int] = None
    task_status: Optional[int] = None
    file_uploaded_count: Optional[int] = None
    require_start_point_epod: Optional[bool] = None
    require_end_point_epod: Optional[bool] = None
    parent_id: Optional[int] = None
    route_plan_no: Optional[str] = None
    delivery_route_plan_date_time: Optional[datetime] = None
    is_sent_consolidated_email: Optional[bool] = None
    sensitive_do: Optional[bool] = None
    created_date_time: Optional[datetime] = None
    modified_date_time: Optional[datetime] = None
    created_user_id: Optional[str] = None
    modified_user_id: Optional[str] = None



app = FastAPI()

# Add CORS middleware to allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/login")
def login(data: LoginRequest):
    try:
        # 1. Authenticate user (auth_check handles sequential logging to Redis)
        is_authenticated = auth_check(data.username, data.password)
        
        if is_authenticated is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="System error. Please try again later."
                )

        if not is_authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # 2. Login successful
        return {"message": "Login successful!", "token": "fake-jwt-token"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, authorization: str = Header(None)):
    if authorization != "Bearer fake-jwt-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    try:
        success, message = reset_password_in_db(data.username, data.new_password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        return {"message": message}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during password reset"
        )

@app.post("/submit-order")
def submit_order(data: OrderRequest, authorization: str = Header(None)):
    if authorization != "Bearer fake-jwt-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    # Here you would typically save the order to a database
    print(f"Order received: {data}")
    return {"message": "Order submitted successfully!", "order_id": "ORD-12345"}


