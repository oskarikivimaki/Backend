from fastapi import FastAPI

app = FastAPI()

anturit = {
    "Lohko1" : {
        0 : {"name" : "Anturi_1", "arvo" : "15", "tila" : "Toimii", }
    },
    "Lohko2" : {},
    "Lohko3" : {}
}


@app.get("/")
def read_root():
    return {"Hello": "World"}