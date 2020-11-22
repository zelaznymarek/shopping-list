from app.db.session import SessionLocal
from app.db.init import init


def run():
    init(SessionLocal())


if __name__ == '__main__':
    run()
