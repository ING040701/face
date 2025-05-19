
from flask import Flask, render_template, request, jsonify, send_file
import os, csv, time, qrcode
from io import BytesIO

app = Flask(__name__)
LOG_PATH = os.path.join("logs", "invite_log.csv")
QR_PATH = os.path.join("static", "qrcodes")

@app.route('/')
def index():
    inviter = request.args.get('from', '小武')
    return render_template('invite.html', inviter=inviter)

@app.route('/respond', methods=['POST'])
def respond():
    data = request.get_json()
    inviter = data.get('inviter', '未知')
    result = data.get('result', 'unknown')
    ip = request.remote_addr
    with open(LOG_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), inviter, result, ip])
    return jsonify({'status': 'ok'})

@app.route('/qrcode')
def qrcode_route():
    inviter = request.args.get('from', '小武')
    url = request.host_url.rstrip('/') + f"/?from={inviter}"
    img = qrcode.make(url)
    file_path = os.path.join(QR_PATH, f"from_{inviter}.png")
    img.save(file_path)
    return send_file(file_path, mimetype='image/png')

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    os.makedirs('static/qrcodes', exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['时间', '邀请人', '操作', 'IP'])
    app.run(host='0.0.0.0', port=5000, debug=True)
