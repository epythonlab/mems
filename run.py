from app import create_app
# from app.database import init_db

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='192.168.43.232', port=5001)
