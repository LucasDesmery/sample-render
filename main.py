from fastapi import FastAPI
import sqlite3
from datetime import date

app = FastAPI()

DB_PATH = "mibase.db"

# Tus ranges reales de IDs
MIN_ID = 2
MAX_ID = 708


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

    cursor.execute("SELECT * FROM Answer WHERE id = ?", (aid,))
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

    # Crear ID estable para el día
    qid = (seed % (MAX_ID - MIN_ID + 1)) + MIN_ID

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
