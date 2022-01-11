from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os 
import requests
from typing import Optional
import json
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [   
 "http://localhost:8080",
 "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET, POST"],
    allow_headers=["*"],
)

class Profile(BaseModel):
    username: str

@app.post("/profile")
async def create_item(data: Profile):
    return get_repos(data)
    
@app.get("/")
def main_page():
    parent_dir_path = os.path.dirname(os.path.realpath(__file__))
    return FileResponse(parent_dir_path + "/home.html")

def sanitize_profile_name(profile: str):
    pattern = '^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$'
    if re.match(pattern,profile) :
        return True
    else :
        return False


def check_exist_repos(profile: json):
    for field in profile:
        if(field=='message'):
            return False
    return True

def get_repos(data: Profile):
    if(sanitize_profile_name(str(data.username))):
        r = requests.get('https://api.github.com/users/'+data.username+'/repos').text
        data_response = json.loads(r)
        if(check_exist_repos(data_response)):
            json_prepare = []
            for repo in data_response:
                json_prepare.append({"id":str(repo['id']),"name":str(repo['name']),"html_url":str(repo['html_url']),"language":str(repo['language'])})
            return json_prepare
        else:
            return "not_found"
    else:
        return "incorrect_username"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, log_level="info")