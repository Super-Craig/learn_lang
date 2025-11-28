from flask import Flask, jsonify, request
import os
import datetime
import platform

# 创建 Flask 应用
app = Flask(__name__)

# 根路由 - 返回基本信息
@app.route('/')
def home():
    return jsonify({
        "message": "🚀 欢迎访问 Railway 测试接口!",
        "status": "运行正常",
        "timestamp": datetime.datetime.now().isoformat(),
        "environment": os.getenv('RAILWAY_ENVIRONMENT', 'development'),
        "python_version": platform.python_version()
    })

# 健康检查端点
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })

# 获取用户信息（示例带参数的路由）
@app.route('/user/<username>')
def get_user(username):
    return jsonify({
        "username": username,
        "joined_at": "2024-01-01",  # 模拟数据
        "profile_url": f"/user/{username}/profile"
    })

# 模拟用户数据
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

# 获取所有用户
@app.route('/users')
def get_all_users():
    return jsonify({
        "users": users,
        "count": len(users),
        "timestamp": datetime.datetime.now().isoformat()
    })

# 根据ID获取用户
@app.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "用户不存在"}), 404

# POST 请求示例 - 创建新用户
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "缺少必要字段: name 和 email"}), 400
    
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    
    return jsonify({
        "message": "用户创建成功",
        "user": new_user
    }), 201

# 环境信息端点
@app.route('/info')
def server_info():
    return jsonify({
        "server_time": datetime.datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "environment_variables": {
            "RAILWAY_ENVIRONMENT": os.getenv('RAILWAY_ENVIRONMENT'),
            "PORT": os.getenv('PORT'),
            "RAILWAY_GIT_COMMIT_SHA": os.getenv('RAILWAY_GIT_COMMIT_SHA', '未设置')
        }
    })

# 错误处理示例
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "端点不存在",
        "available_endpoints": [
            "GET /",
            "GET /health", 
            "GET /info",
            "GET /users",
            "GET /users/<id>",
            "POST /users",
            "GET /user/<username>"
        ]
    }), 404

# 启动应用
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)