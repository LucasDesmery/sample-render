from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "mibase.db"


def get_question_by_id(qid):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Question WHERE id = ?", (qid,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    return None


def get_answer_by_id(aid):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM newAnswer WHERE id = ?", (aid,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    return None


@app.get("/daily-random")
def daily_random():
    # Fecha => número siempre igual dentro del mismo día
    today = str(date.today())  
    seed = abs(hash(today))

    # Obtener todos los IDs válidos de la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Question ORDER BY id")
    valid_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not valid_ids:
        return {"error": "No hay preguntas disponibles en la base de datos"}

    # Seleccionar un ID basado en el seed del día
    index = seed % len(valid_ids)
    qid = valid_ids[index]

    # Obtener la question
    question = get_question_by_id(qid)
    if not question:
        return {"error": f"No existe question con id {qid}"}

    # Obtener el answer_id que tiene la question
    answer_id = question["answer_id"]

    # Obtener el answer correspondiente
    answer = get_answer_by_id(answer_id)
    if not answer:
        return {"error": f"No existe answer con id {answer_id}"}

    return {
        "date": today,
        "Question": question,
        "Answer": answer
    }
