import pytest

from app.schemas.product import ProductBase, ProductCreate


@pytest.mark.parametrize('name,constructor', [
    ('', ProductBase),
    ('A'*256, ProductBase),
    ('', ProductCreate),
    ('A'*256, ProductCreate),
])
def test_should_throw_error(name, constructor):
    """"Check whether ValueError is thrown when name length is invalid"""

    with pytest.raises(ValueError, match='Name must be 1 to 255 chars long'):
        constructor(name=name, category_id=1)
