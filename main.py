from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

IS_DEV = True

"""
if IS_DEV is true its a dev server, if false its a prod server
HOST: 0.0.0.0.0
PORT: 8000
"""

"""
Because its a dev server dont share it with outsiders and block every requests to access port 8000 from out of our company's network
"""


class contact(BaseModel):
    name: str
    email: str
    message: str


DATABASE = []


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("./index.html", "r") as file:
        return file.read()


@app.post("/contact_us")
async def contact(contact: contact):
    return {"message": "Thank "+contact.name+" for your message"}


@app.post("/playlist/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    """upload your playlist"""
    pickle.dump("/playlist/"+file.filename, file.file)
    return {"message": "File uploaded successfully"}


@app.post("/playlist/load")
async def load_playlist(file: UploadFile = File(...)):
    """load your playlist"""
    loaded_track = pickle.load(file.file)
    DATABASE.append(loaded_track)
    return {"message": "File loaded successfully"}
