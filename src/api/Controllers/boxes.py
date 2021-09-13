import io
import os
import textwrap

import psycopg2
import qrcode
from PIL import Image, ImageDraw, ImageFont
from flask import Response
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

from Controllers.config import dbParams, boxViewUrl
from Models.box import Box
from Models.item import Item

dir_path = os.path.dirname(os.path.realpath(__file__))
fontFile = os.path.join(dir_path, "..", "Roboto.ttf")
font = ImageFont.truetype(fontFile, 50)


def list_boxes(page_size: int = None, page_number: int = None, search_filter: str = None) -> dict:
    query_cmd = "SELECT id, label, description FROM box"
    count_cmd = "SELECT COUNT(*) FROM box"
    parameters = []

    if search_filter is not None:
        query_cmd += " WHERE LOWER(Label) LIKE LOWER(%s)"
        count_cmd += " WHERE LOWER(Label) LIKE LOWER(%s)"
        parameters.append(f"%{search_filter}%")

    if type(page_size) is int and type(page_number) is int and page_size is not None and page_number is not None:
        if page_size < 0 or page_size > 100:
            return Response(
                "pageSize must be between 0 and 100 if supplied",
                status=400,
            )

        if type(page_number) is not int or page_number < 0:
            return Response(
                "pageNumber must be greather than or equal to 0",
                status=400,
            )
        query_cmd += " ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY"
        parameters.append(page_number * page_size)
        parameters.append(page_size)
    
    results = []
    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            if search_filter is not None:
                cursor.execute(count_cmd, f"%{search_filter}%")
                count = cursor.fetchone()
            else:
                cursor.execute(count_cmd)
                count = cursor.fetchone()

            if len(parameters) > 0:
                cursor.execute(query_cmd, tuple(parameters))
            else:
                cursor.execute(query_cmd)

            row = cursor.fetchone()
            while row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                results.append(box)
                row = cursor.fetchone()
    return {'count': count, 'result': results}


def add(body: dict) -> Box:
    
    body = Box(body)

    if is_null_or_white_space(body.description):
        return Response(
                "Description is required",
                status=400,
            )
    if is_null_or_white_space(body.label):
        return Response(
                "Label is required",
                status=400,
            )

    sql = """
        INSERT INTO box (label, description) VALUES (%s, %s) RETURNING id, label, description;
        """

    result = None
    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(sql, (body.label, body.description))

            row = cursor.fetchone()
            conn.commit()
            if row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                result = box
        
    return result


def get(box_id: int) -> Box:
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = %s) THEN 1 ELSE 0 END;"
    sql = "SELECT id, label, description FROM box WHERE id = %s"

    result = None
    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, [box_id])
            if cursor.fetchone()[0] != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, [box_id])

            row = cursor.fetchone()
            conn.commit()
            if row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                result = box
        
    return result
            

def update(box_id: int, body: dict) -> Box:
    body = Box(body)

    if is_null_or_white_space(body.description):
        return Response(
                "Description is required",
                status=400,
            )
    if is_null_or_white_space(body.label):
        return Response(
                "Label is required",
                status=400,
            )

    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = %s) THEN 1 ELSE 0 END;"

    sql = """
        UPDATE box SET label = %s, description = %s WHERE id = %s RETURNING id, label, description;
        """

    result = None
    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, [box_id])
            if cursor.fetchone()[0] != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, (body.label, body.description, box_id))

            row = cursor.fetchone()
            conn.commit()
            if row:
                box = Box()
                box.id = row[0]
                box.label = row[1]
                box.description = row[2]

                result = box
        
    return result


def get_label(box_id: int) -> bytes:
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = %s) THEN 1 ELSE 0 END;"
    sql = "SELECT label FROM box WHERE id = %s"

    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, [box_id])
            if cursor.fetchone()[0] != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, [box_id])
            label = cursor.fetchone()[0]
        
    return get_label_image(label, boxViewUrl.replace("{id}", f"{box_id}"))


def get_labels() -> bytes:
    sql = "SELECT id, label FROM box"

    fp = io.BytesIO()
    pp = PdfPages(fp)

    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            row = cursor.fetchone()
            while row:
                label_data = get_label_image(row[1], boxViewUrl.replace("{id}", f"{row[0]}"))
                label_img = Image.open(io.BytesIO(label_data))
                label_img.load()
                im = np.asarray(label_img, dtype="int32")

                plt.imshow(im)
                a = plt.gca()
                a.get_xaxis().set_visible(False)  # We don't need axis ticks
                a.get_yaxis().set_visible(False)
                pp.savefig(plt.gcf())  # This generates a page

                row = cursor.fetchone()

    pp.close()
    pdf_byte_arr = fp.getvalue()
    # pp.close()
    fp.close()
    return pdf_byte_arr


def delete(box_id: int) -> Response:
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = %s) THEN 1 ELSE 0 END;"

    sql = "DELETE FROM box WHERE id = %s"

    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, [box_id])
            if cursor.fetchone()[0] != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, [box_id])
            conn.commit()

    return Response(
        None,
        status=204,
    )
            

def list_items(box_id: int, page_size: int = None, page_number: int = None, search_filter: str = None) -> dict:
    query_cmd = "SELECT id, box_id, name FROM item WHERE box_id = %s"
    count_cmd = "SELECT COUNT(*) FROM item WHERE box_id = %s"
    parameters = [box_id]

    if search_filter is not None:
        query_cmd += " AND LOWER(Name) LIKE LOWER(%s)"
        count_cmd += " AND LOWER(Name) LIKE LOWER(%s)"
        parameters.append(f"%{search_filter}%")

    if type(page_size) is int and type(page_number) is int and page_size is not None and page_number is not None:
        if page_size < 0 or page_size > 100:
            return Response(
                "pageSize must be between 0 and 100 if supplied",
                status=400,
            )

        if type(page_number) is not int or page_number < 0:
            return Response(
                "pageNumber must be greater than or equal to 0",
                status=400,
            )
        query_cmd += " ORDER BY id OFFSET %s ROWS FETCH NEXT %s ROWS ONLY"
        parameters.append(page_number * page_size)
        parameters.append(page_size)
    
    results = []
    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            if search_filter is not None:
                cursor.execute(count_cmd, [box_id], f"%{search_filter}%")
                count = cursor.fetchone()
            else:
                cursor.execute(count_cmd, [box_id])
                count = cursor.fetchone()

            cursor.execute(query_cmd, parameters)

            row = cursor.fetchone()
            while row:
                item = Item()
                item.id = row[0]
                item.boxId = row[1]
                item.name = row[2]

                results.append(item)
                row = cursor.fetchone()
    return {'count': count, 'result': results}


def add_item(box_id: int, body: dict) -> Item:
    body = Item(body)

    if is_null_or_white_space(body.name):
        return Response(
                "Name is required",
                status=400,
            )

    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = %s) THEN 1 ELSE 0 END;"

    sql = """
        INSERT INTO item (box_id, name) VALUES (%s, %s) RETURNING id, box_id, name;
        """

    result = None
    with psycopg2.connect(**dbParams) as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(exists, [box_id])
            if cursor.fetchone()[0] != 1:
                return Response(
                    "Not Found",
                    status=404,
                )

            cursor.execute(sql, (box_id, body.name))

            row = cursor.fetchone()
            conn.commit()
            if row:
                item = Item()
                item.id = row[0]
                item.boxId = row[1]
                item.name = row[2]

                result = item
        
    return result


def is_null_or_white_space(s: str) -> bool:
    return s is None or s == "" or s.isspace()


def get_label_image(text: str, url: str) -> bytes:
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=5,
            box_size=15,
            border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Put the QR Code on an blank 800x1000 Image
    img_width, img_height = img.size
    background = Image.new('RGBA', (800, 1000), (255, 255, 255, 255))
    bg_width, bg_height = background.size
    offset = ((bg_width - img_width) // 2, (bg_height - img_height))
    background.paste(img, offset)

    drawable_img = ImageDraw.Draw(background)

    # Wrap the text if it's too long
    padding = 40
    text_len, _ = drawable_img.textsize(text, font=font)
    avg_pixels_per_char = text_len / len(text)
    text = "\n".join(textwrap.wrap(text, width=(img_width-padding)/avg_pixels_per_char))

    text_size = drawable_img.multiline_textsize(text, font=font)

    text_y = padding // 2
    if text_size[1] < offset[1]:
        text_y = (offset[1] - text_size[1]) // 2

    text_x = ((img_width - text_size[0]) // 2) + padding

    drawable_img.multiline_text((text_x, text_y), text, fill=(0, 0, 0), font=font)

    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr
