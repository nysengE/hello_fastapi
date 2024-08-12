from fastapi import FastAPI

# python -m uvicorn hello_fastapi:app --reload
app = FastAPI()

@app.get('/')
def index():
    return 'Hello, World!!'