import os
from src.app import app
from src.app.routes import routes

routes(app)
os.remove('token.json')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
