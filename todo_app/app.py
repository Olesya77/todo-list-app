from flask import Flask
from routes import app as routes_blueprint

app = Flask(__name__)

# Регистрируем blueprint с маршрутами
app.register_blueprint(routes_blueprint)

# Убираем предупреждение ngrok (если используется)
@app.after_request
def add_ngrok_header(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
