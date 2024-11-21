from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, List


# 임원 정보 모델
class Executive(BaseModel):
    position: str = Field(..., description="임원의 직책")
    nationality: str = Field(..., description="임원의 국적")
    name: str = Field(..., description="임원의 이름")
    name_english: Optional[str] = Field(description="임원의 영문 이름")
    birth_date: Optional[str] = Field(description="임원의 생년월일")
    id_number: Optional[str] = Field(description="임원의 신분증 번호")
    residence: str = Field(..., description="임원의 주소")


class Shareholder_person(BaseModel):
    nationality: str = Field(..., description="주주의 국적")
    name: str = Field(..., description="주주의 이름")
    name_english: Optional[str] = Field(description="주주의 영문 이름")
    birth_date: Optional[str] = Field(description="주주의 생년월일")
    id_number: Optional[str] = Field(description="주주의 신분증 번호")
    residence: str = Field(..., description="주주의 주소")
    shares_held: int = Field(..., description="주주의 보유 주식 수")

# 법인 주주의 대표이사 모델
class Shareholder_corporation_ceo(BaseModel):
    nationality: str = Field(..., description="대표이사 국적")
    name: str = Field(..., description="대표이사명")
    id_number: Optional[str] = Field(description="대표이사 신분증 번호")
    birth_date: Optional[str] = Field(description="대표이사 생년월일")
    residence: str = Field(..., description="대표이사 주소")

# 법인 주주 모델
class Shareholder_corporation(BaseModel):
    corporation_name: str = Field(..., description="법인명")
    corporation_id: str = Field(..., description="법인등록번호")
    corporation_address: str = Field(..., description="법인 주소")
    shares_held: int = Field(..., description="보유 주식 수")
    co_representative: bool = Field(..., description="공동대표 여부")
    ceo: Optional[Shareholder_corporation_ceo] = Field(description="대표이사 정보")

# 주주 모델
class Shareholder(BaseModel):
    shareholder_type: Literal["개인", "법인"] = Field(..., description="주주 유형 (개인 또는 법인)")
    shareholder_person: Optional[Shareholder_person] = Field(None, description="개인 주주 정보")
    shareholder_corporation: Optional[Shareholder_corporation] = Field(None,description="법인 주주 정보")

    @model_validator(mode="after")
    def validate_shareholder_fields(self):
        if self.shareholder_type == "개인" and not self.shareholder_person:
            raise ValueError("개인 주주 유형일 경우 shareholder_person 필드가 필요합니다.")
        if self.shareholder_type == "법인" and not self.shareholder_corporation:
            raise ValueError("법인 주주 유형일 경우 shareholder_corporation 필드가 필요합니다.")
        if self.shareholder_type == "개인" and self.shareholder_corporation:
            raise ValueError("개인 주주 유형일 경우 shareholder_corporation 필드를 제공할 수 없습니다.")
        if self.shareholder_type == "법인" and self.shareholder_person:
            raise ValueError("법인 주주 유형일 경우 shareholder_person 필드를 제공할 수 없습니다.")
        return self

# 메인 요청 모델
class DocumentRequest(BaseModel):
    establishment_date: str = Field(..., description="정관 제정일")
    corporate_name: str = Field(..., description="법인명")
    corporate_name_en: str = Field(..., description="영문 법인명")
    corporate_address: str = Field(..., description="법인 주소")
    max_shares: int = Field(..., description="최대 주식 수")
    price_per_share: int = Field(..., description="1주당 금액")
    current_shares: int = Field(..., description="현 발행 주식 수")
    type_of_shares: str = Field(..., description="주식 종류")
    corporate_purpose: str = Field(..., description="회사 목적")
    capital_increase_plan: bool = Field(..., description="증자 계획 여부")
    bond_with_warrant_plan: bool = Field(..., description="신주인수권부사채 발행 계획 여부")
    interim_dividend_execution: bool = Field(..., description="중간 배당 실행 여부")
    convertible_bond_plan: bool = Field(..., description="전환사채 발행 계획 여부")
    executives: Optional[List[Executive]] = Field(description="임원 목록 (최대 9명)")
    shareholders: Optional[List[Shareholder]] = Field(description="주주 목록 (최대 9명)")

    @model_validator(mode="after")
    def validate_shareholders(self):
        if not self.shareholders or len(self.shareholders) == 0:
            raise ValueError("적어도 하나 이상의 개인 주주 또는 법인 주주가 필요합니다.")
        return self
