# from albemic import run_migrations
from app import app, db_creating

if __name__ == '__main__':
    db_creating()
    # run_migrations()
    app.run(host='0.0.0.0', port=int("3000"), debug=True)
