from fastapi import FastAPI

from routes import expenses, users

app = FastAPI(root_path='/api')

app.include_router(expenses.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app.app:app", host="0.0.0.0", port=8000, reload=True)
