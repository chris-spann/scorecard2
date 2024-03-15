import pytest
from fastapi import HTTPException
from sqlalchemy import asc, desc

from app.deps.request_params import parse_react_admin_params
from app.models.item import Item


class TestRequestParams:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.params_func = parse_react_admin_params(Item)

    def test_parse_default_params(self):
        params = self.params_func(sort_=None, range_=None)
        assert params.skip == 0
        assert params.limit == 10
        assert params.order_by.compare(desc(Item.id))

    def test_parse_range_params(self):
        params = self.params_func(sort_=None, range_="[0, 20]")
        assert params.skip == 0
        assert params.limit == 21

    def test_parse_sort_params_asc(self):
        params = self.params_func(sort_='["id", "ASC"]', range_=None)
        assert params.order_by.compare(asc(Item.id))

    def test_parse_sort_params_desc(self):
        params = self.params_func(sort_='["id", "DESC"]', range_=None)
        assert params.order_by.compare(desc(Item.id))

    def test_throw_invalid_sort_direction(self):
        with pytest.raises(HTTPException):
            self.params_func(sort_='["id", "INVALID"]', range_=None)
