from fastapi import FastAPI , HTTPException
from models.user import UserLogin , Token
from auth import authenticate_user , create_access_token ,get_users_data

app = FastAPI(
    title="English Learning Bot",
    description="A smart chatbot to improve your English skills",
    version="1.0.0"
)
@app.get("/" , tags=["user"])
async def root():
    name = "Charan"
    return {name}
    return {"message" : "Hello bro i am chat bot speaking here"}

@app.post("/login" , response_model=Token)
async def login(user:UserLogin):
    print(user)
    authenticated_user = \
        authenticate_user(user.username , user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401 , detail="Invalid credentials")
    token=create_access_token(data={"sub" : user.username})
    return {"access_token":token,"token_type" : "bearer"}

@app.get("/get-data")
async def get_data_by_token(token:str):
    return get_users_data(token=token)
