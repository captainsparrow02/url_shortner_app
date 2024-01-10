from fastapi import FastAPI, Depends, HTTPException, Request, status
from starlette.datastructures import URL
from fastapi.responses import RedirectResponse
from . import schemas, models, crud, keygen
from .database import SessionLocal, engine, get_db
from .config import get_settings
from sqlalchemy.orm import Session
import validators

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def raise_bad_request(message):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "administrative info", secret_key = db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url

@app.get("/")
def root():
    return "Welcome to URL Shortner App."

@app.post("/url", response_model=schemas.URLInfo, status_code=status.HTTP_201_CREATED)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    
    if not validators.url(url.target_url): # Here validators check if URL provided is valid or not
        raise_bad_request(message="Provided URL is not valid.") 
    
    db_url = crud.create_db_url(db=db, url=url)
    return get_admin_info(db_url)

@app.get("/{url_key}")
def forward_to_target_url(url_key: str, request: Request, db: Session = Depends(get_db)):
    
    if db_url := crud.get_db_url_key(db=db, url_key=url_key):
        crud.update_db_clicks(db, db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.get("/admin/{secret_key}", name="administrative info", response_model=schemas.URLInfo)
def get_url_info(secret_key: str, request: Request, db:Session=Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db = db, secret_key=secret_key):
        db_url.url = db_url.key
        db_url.admin_url = db_url.secret_key
        return get_admin_info(db_url)
    else:
        raise raise_not_found(request)

@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session=Depends(get_db)):
    if db_url := crud.deactivate_db_url_by_secret_key(db, secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise raise_not_found()