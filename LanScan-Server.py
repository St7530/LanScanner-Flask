from flask import Flask, request, make_response
import keyboard
import qrcode
import io
import json

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def handle_data():
    data = request.json['data']
    print(f'Data received: {data}')

    keyboard.write(data)
    keyboard.press('enter')
    return 'ok'

@app.route("/")
def generate_qrcode():
    settings = {
        "serverIP": request.remote_addr,
        "serverPort": request.host.split(':')[1],
        "serverPath": "/data",
        "extraData": "St7530"
    }

    json_str = json.dumps(settings, ensure_ascii=False)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)