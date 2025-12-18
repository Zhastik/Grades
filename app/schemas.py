from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field, field_validator


class UploadGradesResponse(BaseModel):
    ''' модель ответа на POST '''
    status: str = "ok"
    records_loaded: int
    students: int


class StudentTwosResponse(BaseModel):
    ''' модель ответа на GET '''
    full_name: str
    count_twos: int


class GradeRow(BaseModel):
    ''' модель для валидации данных '''
    grade_date: date
    group_number: str = Field(min_length=1)
    full_name: str = Field(min_length=1)
    grade: int

    @field_validator("grade")
    @classmethod
    def grade_must_be_valid(cls, v: int) -> int:
        if v not in (2, 3, 4, 5):
            raise ValueError("Оценка должна быть 2, 3, 4 или 5")
        return v
