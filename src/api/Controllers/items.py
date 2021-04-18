import pyodbc
import json
import os
import configparser

from flask import Response

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = os.path.join(dir_path, "..", "config.ini")

config = configparser.RawConfigParser()
config.read(configFilename)
dbString = config['DATABASE']['ConnectionString']

def itemDelete(id: int) -> Response:
    exists = "Select Case When Exists (SELECT [Id] FROM [dbo].[Item] WHERE [Id] = ?) Then 1 Else 0 End;"

    sql = "DELETE FROM [dbo].[Item] WHERE [Id] = ?"

    with pyodbc.connect(dbString) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, id)
            if cursor.fetchval() != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, id)
            cursor.commit()

    return Response(
        None,
        status=204,
    )
