from worker_images import app


@app.route('/')
def index():
    return 'Hello World !'


@app.route('/ping')
def ping():
    return 'pong', 200


@app.route('/health')
def health():
     return 'UP', 200
