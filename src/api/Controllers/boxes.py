"""Controller To Handle Box Operations."""
import io
import os
import sqlite3
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import qrcode
from Controllers.config import boxViewUrl, dbFile
from flask import Response
from matplotlib.backends.backend_pdf import PdfPages
from Models.box import Box
from Models.item import Item
from PIL import Image, ImageDraw, ImageFont

dir_path = os.path.dirname(os.path.realpath(__file__))
fontFile = os.path.join(dir_path, "..", "Roboto.ttf")
font = ImageFont.truetype(fontFile, 50)


def list_boxes(page_size: int = None, page_number: int = None, search: str = None):
    """List all the boxes in the database."""
    query_cmd = "SELECT id, label, description FROM box"
    count_cmd = "SELECT COUNT(*) FROM box"
    parameters = []

    if search is not None:
        query_cmd += " WHERE LOWER(Label) LIKE LOWER(?)"
        count_cmd += " WHERE LOWER(Label) LIKE LOWER(?)"
        parameters.append(f"%{search}%")

    if isinstance(page_size, int) and isinstance(page_number, int):
        if page_size < 0 or page_size > 100:
            return Response(
                "pageSize must be between 0 and 100 if supplied",
                status=400,
            )

        if not isinstance(page_number, int) or page_number < 0:
            return Response(
                "pageNumber must be greater than or equal to 0",
                status=400,
            )
        query_cmd += " ORDER BY id LIMIT ? OFFSET ?"
        parameters.append(page_size)
        parameters.append(page_number * page_size)

    results = []
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

        if search is not None:
            cursor.execute(count_cmd, f"%{search}%")
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

    return {"count": count, "result": results}


def add(body: dict):
    """Add a box to the db."""
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
        INSERT INTO box (label, description) VALUES (?, ?);
        """

    result = None
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

        cursor.execute(sql, (body.label, body.description))

        row_id = cursor.lastrowid
        cursor.execute("SELECT id, label, description FROM box WHERE id = ?", (row_id,))
        row = cursor.fetchone()

        conn.commit()
        if row:
            box = Box()
            box.id = row[0]
            box.label = row[1]
            box.description = row[2]

            result = box

    return result


def get(box_id: int):
    """Get a specific box by id."""
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = ?) THEN 1 ELSE 0 END;"
    sql = "SELECT id, label, description FROM box WHERE id = ?"

    result = None
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

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


def update(box_id: int, body: dict):
    """Update an existing box."""
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

    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = ?) THEN 1 ELSE 0 END;"

    sql = """UPDATE box SET label = ?, description = ? WHERE id = ?;"""

    result = None
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

        cursor.execute(exists, [box_id])
        if cursor.fetchone()[0] != 1:
            return Response(
                "Not Found",
                status=404,
            )

        cursor.execute(sql, (body.label, body.description, box_id))

        row_id = cursor.lastrowid
        cursor.execute("SELECT id, label, description FROM box WHERE id = ?", (row_id,))
        row = cursor.fetchone()

        conn.commit()
        if row:
            box = Box()
            box.id = row[0]
            box.label = row[1]
            box.description = row[2]

            result = box

    return result


def get_label(box_id: int):
    """Get's a box's label."""
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = ?) THEN 1 ELSE 0 END;"
    sql = "SELECT label FROM box WHERE id = ?"

    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

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
    """Get labels for all boxes in the db."""
    sql = "SELECT id, label FROM box"

    fp = io.BytesIO()
    pp = PdfPages(fp)

    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

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
    fp.close()
    return pdf_byte_arr


def delete(box_id: int) -> Response:
    """Remove a box from the db."""
    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = ?) THEN 1 ELSE 0 END;"

    sql = "DELETE FROM box WHERE id = ?"

    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

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


def list_items(box_id: int, page_size: int = None, page_number: int = None, search: str = None):
    """Get items that go in a specified box."""
    query_cmd = "SELECT id, box_id, name FROM item WHERE box_id = ?"
    count_cmd = "SELECT COUNT(*) FROM item WHERE box_id = ?"
    parameters = [box_id]
    count_parameters = [box_id]

    if search is not None:
        query_cmd += " AND LOWER(Name) LIKE LOWER(?)"
        count_cmd += " AND LOWER(Name) LIKE LOWER(?)"
        parameters.append(f"%{search}%")
        count_parameters.append(f"%{search}%")

    if isinstance(page_size, int) and isinstance(page_number, int):
        if page_size < 0 or page_size > 100:
            return Response(
                "pageSize must be between 0 and 100 if supplied",
                status=400,
            )

        if not isinstance(page_number, int) or page_number < 0:
            return Response(
                "pageNumber must be greater than or equal to 0",
                status=400,
            )
        query_cmd += " ORDER BY id LIMIT ? OFFSET ?"
        parameters.append(page_size)
        parameters.append(page_number * page_size)

    results = []
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

        cursor.execute(count_cmd, count_parameters)
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

    return {"count": count, "result": results}


def add_item(box_id: int, body: dict):
    """Add an item to a box."""
    body = Item(body)

    if is_null_or_white_space(body.name):
        return Response(
            "Name is required",
            status=400,
        )

    exists = "SELECT CASE WHEN EXISTS (SELECT id FROM box WHERE id = ?) THEN 1 ELSE 0 END;"

    sql = """
        INSERT INTO item (box_id, name) VALUES (?, ?);
        """

    result = None
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()

        cursor.execute(exists, [box_id])
        if cursor.fetchone()[0] != 1:
            return Response(
                "Not Found",
                status=404,
            )

        cursor.execute(sql, (box_id, body.name))

        row_id = cursor.lastrowid
        cursor.execute("SELECT id, box_id, name FROM item WHERE id = ?", (row_id,))
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
    """Check whether a string is none or only white space."""
    return s is None or s == "" or s.isspace()


def get_label_image(text: str, url: str) -> bytes:
    """Get the QR Code for a specific URL."""
    # Creating an instance of qrcode
    qr = qrcode.QRCode(version=5, box_size=15, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    # Put the QR Code on an blank 800x1000 Image
    img_width, img_height = img.size
    background = Image.new("RGBA", (800, 1000), (255, 255, 255, 255))
    bg_width, bg_height = background.size
    offset = ((bg_width - img_width) // 2, (bg_height - img_height))
    background.paste(img, offset)

    drawable_img = ImageDraw.Draw(background)

    # Wrap the text if it's too long
    padding = 40
    text_len, _ = drawable_img.textsize(text, font=font)
    avg_pixels_per_char = text_len / len(text)
    text = "\n".join(textwrap.wrap(text, width=(img_width - padding) / avg_pixels_per_char))

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
