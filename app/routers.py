from __future__ import annotations

import csv
import io
from datetime import datetime, date
from typing import List, Set

import asyncpg
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.db import db_conn
from app.schemas import GradeRow, StudentTwosResponse, UploadGradesResponse


router = APIRouter()


def _parse_date(value: str) -> date:
    '''Валидация даты'''
    value = value.strip()
    try:
        return datetime.strptime(value, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError(f"Дата должна быть в формате ДД.ММ.ГГГГ")


def parse_csv_to_rows(file_text: str) -> list[GradeRow]:
    ''' Парсинг файла '''
    reader = csv.DictReader(io.StringIO(file_text), delimiter=";")

    required = {"Дата", "Номер группы", "ФИО", "Оценка"}
    if reader.fieldnames is None or not required.issubset({h.strip() for h in reader.fieldnames}):
        raise HTTPException(
            status_code=422,
            detail=f"нет заголовков: {', '.join(sorted(required))}",
        )

    rows: list[GradeRow] = []
    errors: list[str] = []

    for i, raw in enumerate(reader, start=2):
        try:
            row = GradeRow(
                grade_date=_parse_date(str(raw.get("Дата", ""))),
                group_number=str(raw.get("Номер группы", "")).strip(),
                full_name=str(raw.get("ФИО", "")).strip(),
                grade=int(str(raw.get("Оценка", "")).strip()),
            )
            rows.append(row)
        except Exception as e:
            errors.append(f"строка {i}: {e}")
            if len(errors) >= 20:
                break

    if errors:
        raise HTTPException(status_code=422, detail={"errors": errors})
    if not rows:
        raise HTTPException(status_code=422, detail="CSV пустой или не содержит валидных строк")

    return rows

@router.post("/upload-grades", response_model=UploadGradesResponse)
async def upload_grades(
    file: UploadFile = File(...),
    conn: asyncpg.Connection = Depends(db_conn),
):
    ''' Post на загрузку файла'''
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Нужен .csv файл")

    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=422, detail="Файл должен быть в UTF-8")

    rows = parse_csv_to_rows(text)
    uniq_students: Set[str] = {r.full_name for r in rows}

    async with conn.transaction():
        values = [(r.grade_date, r.group_number, r.full_name, r.grade) for r in rows]
        await conn.executemany(
            """
            INSERT INTO grades (grade_date, group_number, full_name, grade)
            VALUES ($1, $2, $3, $4)
            """,
            values,
        )

    return UploadGradesResponse(records_loaded=len(rows), students=len(uniq_students))


@router.get("/students/more-than-3-twos", response_model=List[StudentTwosResponse])
async def more_than_3_twos(conn: asyncpg.Connection = Depends(db_conn)):
    ''' GET на двойки больше 3'''
    rows = await conn.fetch(
        """
        SELECT full_name, COUNT(*)::int AS count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) > 3
        ORDER BY count_twos DESC, full_name ASC
        """
    )
    return [StudentTwosResponse(full_name=r["full_name"], count_twos=r["count_twos"]) for r in rows]


@router.get("/students/less-than-5-twos", response_model=List[StudentTwosResponse])
async def less_than_5_twos(conn: asyncpg.Connection = Depends(db_conn)):
    ''' GET на двойки меньше 5'''
    rows = await conn.fetch(
        """
        SELECT full_name, COUNT(*)::int AS count_twos
        FROM grades
        WHERE grade = 2
        GROUP BY full_name
        HAVING COUNT(*) < 5
        ORDER BY count_twos ASC, full_name ASC
        """
    )
    return [StudentTwosResponse(full_name=r["full_name"], count_twos=r["count_twos"]) for r in rows]
