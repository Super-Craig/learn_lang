from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "🎉 Railway 部署成功！",
        "status": "API 运行正常",
        "timestamp": datetime.datetime.now().isoformat(),
        "service": "Python Flask API",
        "version": "1.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)