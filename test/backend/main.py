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

class OrderRequest(BaseModel):
    customer_name: str
    item: str
    quantity: int
    delivery_address: str


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


