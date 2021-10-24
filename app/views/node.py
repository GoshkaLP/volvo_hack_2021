from flask import Blueprint, render_template

from .extensions import generate_resp, generate_map

node = Blueprint('node', __name__)


@node.route('/api/version', methods=['GET'])
def api_version():
    resp = {
        'version': '2.0.0',
        'server_status': 'working'
    }
    return generate_resp('ok', 'Success', resp)


@node.route('/', methods=['GET'])
def api_index():
    return render_template('map.html', map_code=generate_map()._repr_html_(), title='Volvo Digital Cars')


