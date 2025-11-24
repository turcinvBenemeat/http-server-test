from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="HTTP Server API",
    description="RESTful HTTP API server with Jenkins CI/CD",
    version="1.0.0"
)

# Mount static files
app.mount("/resources", StaticFiles(directory="resources"), name="resources")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data store (replace with database in production)
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

start_time = time.time()

# Pydantic models
class User(BaseModel):
    name: str
    email: EmailStr

class UserResponse(User):
    id: int
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# Serve homepage
@app.get("/")
async def read_root():
    return FileResponse("index.html")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "uptime": time.time() - start_time,
        "environment": os.getenv("ENV", os.getenv("NODE_ENV", "development")),
        "version": os.getenv("GIT_SHA", "unknown"),
    }

# API information endpoint
@app.get("/api")
async def api_info():
    return {
        "message": "Welcome to HTTP Server API",
        "version": "1.0.0",
        "endpoints": [
            "GET /health - Health check",
            "GET /api - API information",
            "GET /api/users - Get all users",
            "GET /api/users/{id} - Get user by ID",
            "POST /api/users - Create new user",
            "PUT /api/users/{id} - Update user",
            "DELETE /api/users/{id} - Delete user"
        ]
    }

# Get all users
@app.get("/api/users", response_model=dict)
async def get_users():
    return {
        "success": True,
        "count": len(users_db),
        "data": users_db
    }

# Get user by ID
@app.get("/api/users/{user_id}", response_model=dict)
async def get_user(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {
        "success": True,
        "data": user
    }

# Create new user
@app.post("/api/users", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_user(user: User):
    new_id = max([u["id"] for u in users_db], default=0) + 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email
    }
    users_db.append(new_user)
    return {
        "success": True,
        "message": "User created successfully",
        "data": new_user
    }

# Update user
@app.put("/api/users/{user_id}", response_model=dict)
async def update_user(user_id: int, user_update: UserUpdate):
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    users_db[user_index].update(update_data)
    
    return {
        "success": True,
        "message": "User updated successfully",
        "data": users_db[user_index]
    }

# Delete user
@app.delete("/api/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    users_db.pop(user_index)
    return {
        "success": True,
        "message": "User deleted successfully"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)

