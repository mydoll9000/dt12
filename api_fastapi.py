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
def search(q: str, page: int = 1):

    page_size = 20
    if page < 1:
        page = 1

    like = f"%{q}%"

    # Đếm tổng số kết quả
    count_rows = query(
        """
        SELECT COUNT(*) AS total
        FROM work_items
        WHERE code LIKE ? OR description LIKE ?
        """,
        (like, like)
    )

    total = count_rows[0]["total"] if count_rows else 0

    offset = (page - 1) * page_size

    items = query(
        """
        SELECT code, description
        FROM work_items
        WHERE code LIKE ? OR description LIKE ?
        LIMIT ? OFFSET ?
        """,
        (like, like, page_size, offset)
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "pageSize": page_size,
    }


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