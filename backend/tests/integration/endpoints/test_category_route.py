import requests

from sqlalchemy.orm import Session

from app.db.models import User
from app.auth import pwd_context


api_prefix = 'localhost:3000/categories'


def request_as_user(db_session: Session, url):
    user = User(
        email='test@user.cc',
        username='test',
        hashed_password=pwd_context.hash('passwd')
    )

    db_session.add(user)
    db_session.commit()

    login_response = requests.post('localhost:8888/login', data={'email': user.email, 'password': 'passwd'})
    breakpoint()


def test_get_category(db_session):
    request_as_user(db_session, 'url')
