# main.py
from fastapi import FastAPI
from app.routers import home, doc_generator, other_feature

app = FastAPI()

# 다른 라우터 등록
app.include_router(home.router)
app.include_router(doc_generator.router, prefix="/docs", tags=["Document"])
app.include_router(other_feature.router, prefix="/features", tags=["Feature"])


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Application"}
