from fastapi import APIRouter

# APIRouter 객체 생성
router = APIRouter()

# 샘플 API 경로 정의
@router.get("/example")
def example_route():
    return {"message": "This is an example route in other_feature module"}
