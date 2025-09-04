from flask import Flask
from routes import travels_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(travels_bp, url_prefix="/api/travel-journal")

    @app.get("/")
    def root():
        return {"message": "Travel Journal API"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
