from shopping_list.db.init import init
from shopping_list.db.session import SessionLocal


def run():
    init(SessionLocal())


if __name__ == "__main__":
    run()
