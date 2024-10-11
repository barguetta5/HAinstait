# from albemic import run_migrations
from app import app, db_creating

if __name__ == '__main__':
    db_creating()
    # run_migrations()
    app.run(debug=True)
