import psycopg2

from flask import Response
from Controllers.config import dbParams


def item_delete(item_id: int) -> Response:
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM item WHERE id = %s) THEN 1 ELSE 0 END;"

    sql = "DELETE FROM item WHERE id = %s"

    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
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
