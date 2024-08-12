from fastapi import FastAPI

# python -m uvicorn hello_fastapi:app --reload

app = FastAPI()

@app.get('/')
def index():
    return 'Hello, World!! again!!'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('hello2_fastapi:app', reload=True)