from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import multipart
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/{popa}')
async def get(popa):
    return popa


@app.post('/Upload')
async def uploadFile(file):
    print(file)
    return {file}

@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}
import