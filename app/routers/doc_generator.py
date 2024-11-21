from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.corporation_articles import DocumentRequest
from app.services.doc_service import replace_markers

router = APIRouter()

TEMPLATE_PATH = "app/templates/정관_template.docx"  # 템플릿 파일 경로

@router.post("/generate-doc/")
async def generate_doc(request: DocumentRequest):
    """
    템플릿 Word 문서를 기반으로 입력 데이터를 치환하여 결과 문서를 반환하는 API.
    """
    # 입력 데이터 검증
    if request.executives and len(request.executives) > 9:
        raise HTTPException(status_code=400, detail="임원 정보는 최대 9명까지만 입력 가능합니다.")
    if request.shareholders and len(request.shareholders) > 9:
        raise HTTPException(status_code=400, detail="주주 정보는 최대 9명까지만 입력 가능합니다.")

    # 데이터를 치환 가능한 형식으로 정리
    data = {
        "establishment_date": request.establishment_date,

        "corporate_name": request.corporate_name,
        "corporate_name_big_bold": request.corporate_name,

        "corporate_name_en": request.corporate_name_en,

        "corporate_purpose_bold": request.corporate_purpose,
        "corporate_address": request.corporate_address,

        "max_shares_bold": request.max_shares,
        "price_per_share": request.price_per_share,
        "current_shares": request.current_shares,
        "type_of_shares": request.type_of_shares,
        "corporate_purpose": request.corporate_purpose,
        "capital_increase_plan": "Yes" if request.capital_increase_plan else "No",
        "bond_with_warrant_plan": "Yes" if request.bond_with_warrant_plan else "No",
        "interim_dividend_execution": "Yes" if request.interim_dividend_execution else "No",
        "convertible_bond_plan": "Yes" if request.convertible_bond_plan else "No",
        # 리스트 데이터를 처리
        "executives": [
            {
                "position": exec.position,
                "name": exec.name or "",
                "nationality": exec.nationality or "",
            }
            for exec in request.executives or []
        ],
        "shareholders": [
            {
                "type": sh.shareholder_type,
                "name": sh.shareholder_person.name if sh.shareholder_person else "",
                "shares": sh.shareholder_person.shares_held if sh.shareholder_person else 0,
            }
            for sh in request.shareholders or []
        ],
    }

    # 결과 파일 경로
    output_path = "generated_document.docx"

    # 템플릿 치환 및 저장
    replace_markers(TEMPLATE_PATH, output_path, data)

    # 결과 파일 반환
    return FileResponse(
        path=output_path,
        filename="generated_document.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
