from sqlalchemy.orm import Session

from app.db.models import User
from app.auth import pwd_context


api_prefix = 'localhost:3000/categories'


def get_token(db_session: Session, client):
    user = User(
        email='test@user.cc',
        username='test',
        hashed_password=pwd_context.hash('passwd')
    )

    db_session.add(user)
    db_session.commit()

    login_response = client.post('/login', data={'username': user.email, 'password': 'passwd'})

    return login_response.json()['access_token']


def test_get_category(db_session, client):
    token = get_token(db_session, client)

    res = client.get('/categories', headers={'WWW-Authenticate': f'Bearer {token}'})
    breakpoint()
