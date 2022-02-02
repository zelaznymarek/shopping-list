from backend.app.db.init import init
from backend.app.db.session import SessionLocal


def run():
    init(SessionLocal())


if __name__ == "__main__":
    run()
