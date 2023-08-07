

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin123",
  database="mydatabase"
)


from fastapi import FastAPI,HTTPException,Request,Depends
from pydantic import BaseModel
from datetime import datetime,timedelta
from typing import Optional
import jwt



app = FastAPI()

# User Model
class User(BaseModel):
    username: str
    password: str

# User Endpoint
@app.post("/users")
async def create_user(user: User):
  
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    val = (user.username, user.password)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "User created successfully"}

#Login Endpoint
@app.post("/login")
async def login_user(user: User):
   
    mycursor = mydb.cursor()
    
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (user.username, user.password)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if len(result)==0:
        raise HTTPException(status_code=404, detail="Invalid Username or Password")
    else:
        sessionData = {}
        sessionData['username'] = user.username
        sessionData['expiryTime'] = datetime.now() + timedelta(minutes=30)
        return sessionData


#Middleware Function for Session Validation
async def validate_session(request: Request, call_next):
    try:
        sessionToken = request.headers['Authorization']
        tokenData = jwt.decode(sessionToken, 'SECRET_KEY', algorithms=["HS256"])
        if datetime.strptime(tokenData['expiryTime'], '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
            raise HTTPException(status_code=401, detail="Session Expired")
    except:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    response = await call_next(request)
    return response



# Authenticated Endpoint
@app.get("/authenticated")
async def authenticated_user(user: User, token: str = Depends(validate_session)):
    return {"message": "Authenticated User"}


#Middleware Function for Session Validation and Timeout
async def validate_session(request: Request, call_next):
    try:
        sessionToken = request.headers['Authorization']
        tokenData = jwt.decode(sessionToken, 'SECRET_KEY', algorithms=["HS256"])
        if datetime.strptime(tokenData['expiryTime'], '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
            raise HTTPException(status_code=401, detail="Session Expired")
    except:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    tokenData['expiryTime'] = datetime.now() + timedelta(minutes=30)
    newToken = jwt.encode(tokenData, 'SECRET_KEY', algorithm="HS256")
    response = await call_next(request)
    response.headers['Authorization'] = newToken
    return response



# Authenticated Endpoint with Session Timeout
@app.get("/authenticated_timeout")
async def authenticated_timeout_user(user: User, token: str = Depends(validate_session)):
    return {"message": "Authenticated User with Session Timeout"}
