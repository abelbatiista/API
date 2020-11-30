from fastapi import FastAPI

#CREACION DEL OBJETO APP
app = FastAPI()

#ORÍGENES DESCONOCIDOS


@app.get("/")
def read_root():
    return {"message":"Hello TutLinks.com"}