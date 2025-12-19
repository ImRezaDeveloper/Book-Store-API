from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"hello book store api project"}