# Version: 0.29
import os
import requests
from flask import Flask, send_from_directory, request, abort

VERSION = "0.56"
PROJECT_NAME = "Eye"

base_dir = os.path.dirname(os.path.abspath(__file__))
www_dir = os.path.join(base_dir, 'www')

app = Flask(__name__, static_folder=www_dir)

# Konfiguratsioon keskkonnamuutujatest (.env failist)
GO2RTC_API = os.getenv('GO2RTC_API', 'http://127.0.0.1:1984/api/streams')
raw_tokens = os.getenv('ACCESS_TOKENS', 'eye-default-kood')
VALID_TOKENS = [t.strip() for t in raw_tokens.split(',') if t.strip()]

def get_streams():
    try:
        response = requests.get(GO2RTC_API, timeout=3)
        if response.status_code == 200:
            streams = response.json()
            # Teisendame kaamerate ID-d ilusamaks nimeks (nt "elutuba_kaamera" -> "Elutuba Kaamera")
            return [{"id": k, "name": k.replace('_', ' ').title()} for k in streams.keys()]
    except Exception as e:
        print(f"API Error at {GO2RTC_API}: {e}")
    return []

@app.before_request
def check_auth():
    # Lubame staatilised failid (favicon, js, manifest) ilma tokenita, 
    # et brauser saaks iidset ja ikooni laadida.
    if request.path != '/':
        return
    
    user_token = request.args.get('token')
    if user_token not in VALID_TOKENS:
        print(f"Unauthorized access attempt from {request.remote_addr}")
        abort(401, "Autoriseerimine ebaõnnestus. Lisa URL-i lõppu ?token=SINU_KOOD")

@app.route('/')
def index():
    streams = get_streams()
    index_path = os.path.join(www_dir, 'index.html')
    try:
        with open(index_path, 'r') as f:
            html = f.read()
        
        # Asendame HTML-is olevad kohahoidjad dünaamilise infoga
        html = html.replace('{{VERSION}}', VERSION)
        html = html.replace('{{PROJECT_NAME}}', PROJECT_NAME)
        
        # Süstime kaamerate andmed JavaScripti
        return html.replace('window.NVR_DATA = [];', f'window.NVR_DATA = {streams};')
    except FileNotFoundError:
        return "index.html not found", 404

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    print(f"--- {PROJECT_NAME} Dashboard v{VERSION} ---")
    print(f"Sihitakse go2rtc API-t: {GO2RTC_API}")
    print(f"Süsteemi laetud lubatud koode: {len(VALID_TOKENS)}")
    app.run(host='0.0.0.0', port=8080)
