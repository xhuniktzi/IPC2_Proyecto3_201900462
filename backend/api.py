import re
from xml.etree import ElementTree as ET
from xml.dom import minidom

from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from dateutil.parser import parse

from admin import Admin
from event import Event
from helpers import parse_list_users

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})

admin = Admin()


@app.route('/events', methods=['POST'])
def post_events():
    info_request = request.data.decode('utf-8')
    data = open('info_request.xml', 'w+', encoding='utf-8')
    data.write(info_request)
    data.close()

    parse_data = open('info_request.xml', 'r+', encoding='utf-8')
    parse_info = parse_data.read()
    parse_info = re.sub(r'<.+ (.+@.+)>', r'\1', parse_info)
    parse_info = re.sub(r'<(.+@.+)>', r'\1', parse_info)

    parse_request = open('parse_request.xml', 'w+', encoding='utf-8')
    parse_request.write(parse_info)
    parse_request.close()

    parse_data.close()

    tree = ET.parse('parse_request.xml')
    root = tree.getroot()

    for child in root:
        date = re.search(r'(\d{2,2}/\d{2,2}/\d{4,4})',
                         child.text).group(1).strip()
        reported_by = re.search(r'Reportado por:(.+)',
                                child.text).group(1).strip()
        affected_users = re.search(r'Usuarios afectados:(.+)',
                                   child.text).group(1).strip()
        error_code = re.search(r'Error:.?(\d+)\d*',
                               child.text).group(1).strip()

        event = Event(parse(date, dayfirst=True), reported_by, int(error_code))
        for user in parse_list_users(affected_users):
            event.add_affected_user(user)

        admin.add_event(event)

    return Response(status=204)


@app.route('/stats', methods=['GET'])
def get_stats():
    stats = admin.query_events()

    document = minidom.Document()
    root = document.createElement('ESTADISTICAS')
    document.appendChild(root)

    for stat in stats:
        stat_element = document.createElement('ESTADISTICA')
        root.appendChild(stat_element)

        date_element = document.createElement('FECHA')
        date_element.appendChild(document.createTextNode(stat['date']))
        stat_element.appendChild(date_element)

        cant_msg_element = document.createElement('CANTIDAD_MENSAJES')
        cant_msg_element.appendChild(
            document.createTextNode(str(stat['cant_events'])))
        stat_element.appendChild(cant_msg_element)

        reported_by_element = document.createElement('REPORTADO_POR')
        stat_element.appendChild(reported_by_element)

        for user in stat['reported_by']:
            user_element = document.createElement('USUARIO')
            reported_by_element.appendChild(user_element)

            email_element = document.createElement('EMAIL')
            email_element.appendChild(document.createTextNode(user['email']))
            user_element.appendChild(email_element)

            cant_element = document.createElement('CANTIDAD_MENSAJES')
            cant_element.appendChild(document.createTextNode(str(
                user['cant'])))
            user_element.appendChild(cant_element)

        affects_element = document.createElement('AFECTADOS')
        stat_element.appendChild(affects_element)

        for user in stat['affects']:
            user_element = document.createElement('AFECTADO')
            user_element.appendChild(document.createTextNode(user))
            affects_element.appendChild(user_element)

        errors_element = document.createElement('ERRORES')
        stat_element.appendChild(errors_element)

        for error in stat['errors']:
            error_element = document.createElement('ERROR')
            errors_element.appendChild(error_element)

            code_element = document.createElement('CODIGO')
            code_element.appendChild(
                document.createTextNode(str(error['code'])))
            error_element.appendChild(code_element)

            cant_element = document.createElement('CANTIDAD_MENSAJES')
            cant_element.appendChild(
                document.createTextNode(str(error['cant'])))
            error_element.appendChild(cant_element)

    xml_output = document.toprettyxml(indent='\t', newl='\n', encoding='utf-8')
    return Response(response=xml_output,
                    status=200,
                    mimetype='application/xml',
                    content_type='application/xml')


@app.route('/stats/by_date', methods=['GET'])
def get_stats_by_date():
    date = parse(request.args.get('date'), dayfirst=True)

    return jsonify(admin.query_events_by_date(date))


@app.route('/stats/by_error', methods=['GET'])
def get_stats_by_error():
    error = request.args.get('error')

    return jsonify(admin.query_events_by_error_code(error))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
