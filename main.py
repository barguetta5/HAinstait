from albemic import run_migrations
from app import app


if __name__ == '__main__':
    run_migrations()
    app.run(debug=True)
