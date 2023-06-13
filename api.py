# Loading the Libraries and Data
import hashlib, re, json, configparser
from predict import *
from pydantic import BaseModel
from fastapi import FastAPI, Body, Form, Depends, HTTPException, status, APIRouter
from security_token import *
from user_db import *
from pydantic import BaseModel
from fastapi_localization import TranslateJsonResponse
from fastapi_localization import TranslatableStringField
from typing import List

# class LanguageTranslatableSchema(BaseModel):
#     code: str
#     title: TranslatableStringField

# setting the chart display specs
pd.set_option('display.max_colwidth', 500)

# importing details from config.ini
config = configparser.ConfigParser()
config.read('config.ini')  # reading the config file

debug = config.getboolean('DEFAULT', 'debug')  # getting debug value
host = config.get('DEFAULT', 'host')  # getting host id
port = config.getint('DEFAULT', 'port')  # getting port number


# Creating Class for Fast api input
class User(BaseModel):
    About: str

class User_about(BaseModel):
    job_title: str
    field: str
    experience: str


# Initializing the FastApi
app = FastAPI(debug=debug)

# for creating connection between the class and api
router = APIRouter(prefix="/v1")

# Method to do login and get the token
@router.post("/check-token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"status_code": 200, "access_token": access_token, "token_type": "bearer"}
    except Exception as err:
        return {"status_code": 401, "message": err}


# Get method to check the current user
@router.get("/users/me")
async def read_users_me(
        current_user: Annotated[User2, Depends(get_current_active_user)]):
    
    return {"status_code": 200, "message": current_user}


# Register user
@router.post("/register-user")
async def register(form_data: User2):
    try:
        username = form_data.username
        if database_user().query_user(username):
            return {"status_code": 401, "message": "Username already registered, change your username"}
        name = form_data.name
        email_id = form_data.email
        password = pwd_context.hash(form_data.password)
        message = database_user().write_user(username, name, email_id, password)

        return {"status_code": 200, "message": message}
    except Exception as err:
        return {"status_code": 401, "message": err}


# Update User details
@router.put("/update-user")
async def updates(form_data: User3, current_user: Annotated[User2, Depends(get_current_active_user)]):
    try:
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Not authenticated bro",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username = current_user.username
        name = form_data.name
        email_id = form_data.email
        update_msg = database_user().update_user(username, name, email_id)
        print(update_msg)
        updated_detail = database_user().user_detail(username)
        return {"status_code": 200, "message": updated_detail, "user_id":current_user.id}
    except Exception as err:
        return {"status_code": 401, "message": err}


# Delete User
@router.delete("/delete-user")
async def deletes(current_user: Annotated[User2, Depends(get_current_active_user)]):
    try:
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username = current_user.username
        msg = database_user().delete_user(username)

        return {"status_code": 200, "message": msg, "deleted_user_id":current_user.id}
    except Exception as err:
        return {"status_code": 401, "message": err}


# Getting recommended mentor
@router.post("/mentor-recommendation")
# Using ASYNC allows you to write non-blocking code that can handle multiple requests concurrently and efficiently.
async def get_in22labs(profile: User_about, current_user: Annotated[User2, Depends(get_current_active_user)]):
    try:
        if not current_user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Non Alphabet characters which are not allowed in name
        regex = re.compile('[@_!#$%^&*(",\')<>?/\|}{~:]')

        # getting the input
        profile1 = {
            "Name": [current_user.username],
            "About": [profile.job_title+", "+profile.field+", "+profile.experience]
        }

        name, about = profile1["Name"][0], profile1["About"][0]

        # # creating hash of About to generate an unique ID
        # my_hash = hashlib.sha256(about.encode()).hexdigest()

        # Checking if name or About is empty
        if about != "":
            about = about.split(",")
        else:
            return {"status_code": 400,  # If empty then returning code 400 error
                    "message": "Fields can't be empty"
                    }

        if len(about) > 1:  # Checking if About has atleast 2 comma seperated fields
            for elem in about:
                # Checking if the input is just a letter or non alphabet characters then returning code 400
                if len(elem) == 1 or elem.isnumeric() == True or regex.search(elem) != None:

                    return {
                        "status_code": 400,
                        "message": "Job profile / fields / description can't contain Special characters or number. It should be proper words."
                    }

            about2 = json.dumps(
                {"job_profile": about[0], "field": about[1], "experience": about[2] if len(about) > 2 else ""})
            # creating data frame for the input
            new_profile = pd.DataFrame(profile1)

            # predicting the mentors
            recomendation = In22labs_Mentor_mentee.predict_mentor(
                new_profile=new_profile)

            print(database_user().write_activity(current_user.id, name, about2, recomendation))

            return {"status_code": 200,
                    "data": json.loads(recomendation)
                    }
        else:
            return {"status_code": 400,  # returning code 400 if about doesn't have atleast two comma seperated fields
                    "message": "You have to give atleast two comma-separated words"
                    }
    except Exception as err:
        return {"status_code": 401, "message": err}


#Get all user details
@router.get("/all-users/{limit_no}")
async def read_all_users(limit_no:int):
    try:
        users = database_user().all_users(limit_no)
        jsone = {"status_code": 404,
                 "message": "There is an error please check"}
        if users:
            jsone = {"status_code": 200, "message": users}
        return jsone
    except Exception as err:
        return {"status_code": 401, "message": err}


# Get all activity details
@router.get("/all-activity/{limit_no}")
async def read_all_activity(limit_no:int):
    try:
        jsone = {"status_code": 404,
                 "message": "There is an error please check"}
        activity = database_user().all_activity(limit_no)
        if activity:
            jsone = {"status_code": 200, "message": activity}
        return jsone
    except Exception as err:
        return {"status_code": 401, "message": err}

app.include_router(router)

# Starting the API  with mentioned host and port in the config
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('api:app', host=host, port=port, reload=True)
