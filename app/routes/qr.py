import os
from io import StringIO, BytesIO

import qrcode
from flask import send_file, url_for, render_template
from PIL import ImageDraw, ImageFont

from app.models import Waypoint
from app.routes import admin_bp as bp


def get_font():
    this = os.path.abspath(os.path.dirname(__file__))
    arial = os.path.join(this, '../static/arial.ttf')
    return ImageFont.truetype(arial, 30)


def random_qr(url, name):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make()
    img = qr.make_image()

    ImageDraw.Draw(img).text((0, 0), name, font=get_font())  # Coordinates  # Text

    return img


@bp.route('/image/<token>')
def qr_image(token):
    waypoint = Waypoint.query.filter_by(token=token).first_or_404()

    img = random_qr(url_for('main.found', token=waypoint.token, _external=True), waypoint.name)

    img_buf = BytesIO()
    img.save(img_buf)
    img_buf.seek(0)

    return send_file(img_buf, mimetype='image/png')


@bp.route('/all_images')
def all_images():
    waypoints = Waypoint.query.all()
    return render_template('admin/all_images.html', waypoints=waypoints)
