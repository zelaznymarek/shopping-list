from app.db.models import User


def test_user(db_session, db_user):
    results = db_session.query(User).all()

    assert len(results) == 1

    user: User = results[0]

    assert user.name == 'Example'
