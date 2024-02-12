from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def main():
    '''Entry point for app'''
    return "Hello World"