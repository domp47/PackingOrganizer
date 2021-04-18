import pyodbc
import json
import os
import configparser

from flask import Response
from Models.box import Box
from Models.item import Item

dir_path = os.path.dirname(os.path.realpath(__file__))
configFilename = os.path.join(dir_path, "..", "config.ini")

config = configparser.RawConfigParser()
config.read(configFilename)
dbString = config['DATABASE']['ConnectionString']

def list(pageSize: int = None, pageNumber: int = None, filter: str = None) -> str:
    queryCmd = "SELECT [Id],[Label],[Description] FROM [dbo].[Box]"
    paramters = []

    if filter is not None:
        queryCmd += " WHERE LOWER(Label) LIKE LOWER(?)"
        paramters.append(f"%{filter}%")

    if type(pageSize) is int and type(pageNumber) is int and pageSize is not None and pageNumber is not None:
        if pageSize < 0 or pageSize > 100:
            return Response(
                "pageSize must be between 0 and 100 if supplied",
                status=400,
            )

        if type(pageNumber) is not int or pageNumber < 1:
            return Response(
                "pageNumber must be greather than 0",
                status=400,
            )
        queryCmd += " ORDER BY Id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        paramters.append((pageNumber-1)*pageSize)
        paramters.append(pageSize)
    
    results = []
    with pyodbc.connect(dbString) as conn:
        with conn.cursor() as cursor:
            if len(paramters) > 0:
                cursor.execute(queryCmd, tuple(paramters))
            else:
                cursor.execute(queryCmd)

            row = cursor.fetchone()
            while row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                results.append(box)
                row = cursor.fetchone()
    return results

def add(body: Box) -> str:
    
    body = Box(body)

    if isNullOrWhiteSpace(body.description):
        return Response(
                "Description is required",
                status=400,
            )
    if isNullOrWhiteSpace(body.label):
        return Response(
                "Label is required",
                status=400,
            )

    sql = """
        SET NOCOUNT ON;
        DECLARE @InsertedRecord TABLE(Id bigint, Label nvarchar(max), Description nvarchar(max)); 

        INSERT [dbo].[Box] ([Label], [Description]) OUTPUT INSERTED.Id, INSERTED.Label, INSERTED.Description INTO @InsertedRecord VALUES (?, ?);
        
        SELECT * FROM @InsertedRecord;
        """

    result = None
    with pyodbc.connect(dbString) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(sql, (body.label, body.description))

            row = cursor.fetchone()
            cursor.commit()
            if row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                result = box
        
    return result

def update(id: int, body: Box) -> str:
    body = Box(body)

    if isNullOrWhiteSpace(body.description):
        return Response(
                "Description is required",
                status=400,
            )
    if isNullOrWhiteSpace(body.label):
        return Response(
                "Label is required",
                status=400,
            )

    exists = "Select Case When Exists (SELECT [Id] FROM [dbo].[Box] WHERE [Id] = ?) Then 1 Else 0 End;"

    sql = """
        SET NOCOUNT ON;
        DECLARE @UpdatedRecord TABLE(Id bigint, Label nvarchar(max), Description nvarchar(max)); 

        UPDATE [dbo].[Box] SET [Label] = ?, [Description] = ? OUTPUT INSERTED.Id, INSERTED.Label, INSERTED.Description INTO @UpdatedRecord WHERE [Id] = ?;
        
        SELECT * FROM @UpdatedRecord;
        """

    result = None
    with pyodbc.connect(dbString) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, id)
            if cursor.fetchval() != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, (body.label, body.description, id))

            row = cursor.fetchone()
            cursor.commit()
            if row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                result = box
        
    return result

def delete(id: int) -> Response:
    exists = "Select Case When Exists (SELECT [Id] FROM [dbo].[Box] WHERE [Id] = ?) Then 1 Else 0 End;"

    sql = "DELETE FROM [dbo].[Box] WHERE [Id] = ?"

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
            

def listItems(id:int, pageSize: int = None, pageNumber: int = None, filter: str = None) -> str:
    queryCmd = "SELECT [Id],[BoxId],[Name] FROM [dbo].[Item] WHERE [BoxId] = ?"
    paramters = [id]

    if filter is not None:
        queryCmd += " AND LOWER(Name) LIKE LOWER(?)"
        paramters.append(f"%{filter}%")

    if type(pageSize) is int and type(pageNumber) is int and pageSize is not None and pageNumber is not None:
        if pageSize < 0 or pageSize > 100:
            return Response(
                "pageSize must be between 0 and 100 if supplied",
                status=400,
            )

        if type(pageNumber) is not int or pageNumber < 1:
            return Response(
                "pageNumber must be greather than 0",
                status=400,
            )
        queryCmd += " ORDER BY Id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        paramters.append((pageNumber-1)*pageSize)
        paramters.append(pageSize)
    
    results = []
    with pyodbc.connect(dbString) as conn:
        with conn.cursor() as cursor:
            cursor.execute(queryCmd, tuple(paramters))

            row = cursor.fetchone()
            while row:
                item = Item()
                item.id = row[0]
                item.boxId = row[1]
                item.name = row[2]

                results.append(item)
                row = cursor.fetchone()
    return results

def addItem(id: int, body: Item) -> str:
    body = Item(body)

    if isNullOrWhiteSpace(body.name):
        return Response(
                "Name is required",
                status=400,
            )

    exists = "Select Case When Exists (SELECT [Id] FROM [dbo].[Box] WHERE [Id] = ?) Then 1 Else 0 End;"

    sql = """
        SET NOCOUNT ON;
        DECLARE @InsertedRecord TABLE(Id bigint, BoxId bigint, Name nvarchar(max)); 

        INSERT [dbo].[Item] ([BoxId], [Name]) OUTPUT INSERTED.Id, INSERTED.BoxId, INSERTED.Name INTO @InsertedRecord VALUES (?, ?);
        
        SELECT * FROM @InsertedRecord;
        """

    result = None
    with pyodbc.connect(dbString) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, id)
            if cursor.fetchval() != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, (id, body.name))

            row = cursor.fetchone()
            cursor.commit()
            if row:
                item = Item()
                item.id = row[0]
                item.boxId = row[1]
                item.name = row[2]

                result = item
        
    return result

def isNullOrWhiteSpace(s: str) -> bool:
    return s is None or s == "" or s.isspace()