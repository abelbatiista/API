from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#CREACION DEL OBJETO APP
app = FastAPI()

#ORÍGENES DESCONOCIDOS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message":"Hello TutLinks.com"}