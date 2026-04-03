from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

users = []

@app.post("/user/", description="Endpoint to add user in list", status_code=201)
def add_user(name: str = Query(..., min_length=1, max_length=30, description="Username")):
    name = name.strip().lower()
    if name in users:
        raise HTTPException(status_code=409, detail="User has already been in list")
    users.append(name)
    return {"message": "User added successfully"}

@app.delete('/user/', description="Endpoint to delete user from list")
def del_user(name: str = Query(..., min_length=1, max_length=30, description="Username")):
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(name)
    return {"message": "User deleted successfully"}

@app.get("/users/", description="Endpoint to get all users in list")
def get_all_users():
    return {"users": users}