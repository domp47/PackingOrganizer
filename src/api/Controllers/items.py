"""Controller to Handler Item API Calls."""
import sqlite3

from Controllers.config import dbFile
from flask import Response


def item_delete(item_id: int) -> Response:
    """Delete an item from a box."""
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM item WHERE id = ?) THEN 1 ELSE 0 END;"

    sql = "DELETE FROM item WHERE id = ?"

    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

        cursor.execute(exists, [item_id])
        if cursor.fetchone()[0] != 1:
            return Response(
                "Not Found",
                status=404,
            )

        cursor.execute(sql, [item_id])
        conn.commit()

    return Response(
        None,
        status=204,
    )
