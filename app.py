import os
from src.app import app
from src.app.routes import routes

routes(app)


if __name__ == "__main__":
    try:
        os.remove('token.json')
    except:
        pass
    app.run(debug=True, host="0.0.0.0", port=8080)
