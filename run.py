from app import create_app
# from app.database import init_db

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
