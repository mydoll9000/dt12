from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3

app = FastAPI()

DB = "tt12_pro.db"


def query(sql, params=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(sql, params)

    rows = [dict(r) for r in cur.fetchall()]

    conn.close()
    return rows


@app.get("/")
def home():
    return FileResponse("web_index.html")


@app.get("/search")
def search(q: str):

    return query(
        """
        SELECT code, description
        FROM work_items
        WHERE code LIKE ? OR description LIKE ?
        LIMIT 50
        """,
        (f"%{q}%", f"%{q}%")
    )


@app.get("/work/{code}")
def get_work(code: str):

    return query(
        """
        SELECT *
        FROM work_items
        WHERE code = ?
        """,
        (code,)
    )


@app.get("/norm/{code}")
def norms(code: str):

    return query(
        """
        SELECT 
            w.code,
            w.description,
            n.quantity,
            n.resource_type,
            n.resource_id
        FROM work_items w
        JOIN norms n ON w.id = n.work_item_id
        WHERE w.code = ?
        """,
        (code,)
    )