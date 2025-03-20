import pytest
from pydantic import ValidationError
from app.models.product import ProductCreate, ProductResponse, ProductUpdate
from app.models.sale import SalesTotalResponse, SalesTopProductsResponse

def test_product_create_valid():
    valid_data = {"name": "Product A", "category_id": 1}
    product = ProductCreate(**valid_data)
    assert product.name == "Product A"
    assert product.category_id == 1

def test_product_create_invalid():
    invalid_data = {"name": 123, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**invalid_data)
    
    invalid_data = {"name": "Product B", "category_id": "invalid"}
    with pytest.raises(ValidationError):
        ProductCreate(**invalid_data)

def test_product_response_valid():
    valid_data = {"id": 1, "name": "Product A", "category_id": 1}
    product_response = ProductResponse(**valid_data)
    assert product_response.id == 1
    assert product_response.name == "Product A"
    assert product_response.category_id == 1

def test_product_response_invalid():
    invalid_data = {"name": "Product A", "category_id": 1}
    with pytest.raises(ValidationError):
        ProductResponse(**invalid_data)

def test_product_update_valid():
    valid_data = {"id": 1, "name": "Product A", "category_id": 1}
    product_update = ProductUpdate(**valid_data)
    assert product_update.id == 1
    assert product_update.name == "Product A"
    assert product_update.category_id == 1

def test_product_update_invalid():
    invalid_data = {"id": 1, "name": 123, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductUpdate(**invalid_data)

def test_sales_total_response_valid():
    valid_data = {"total": 100}
    sales_total = SalesTotalResponse(**valid_data)
    assert sales_total.total == 100

def test_sales_total_response_invalid():
    invalid_data = {"total": "invalid"}
    with pytest.raises(ValidationError):
        SalesTotalResponse(**invalid_data)

def test_sales_top_products_response_valid():
    valid_data = {"name": "Product A", "sold_amount": 50}
    sales_top_product = SalesTopProductsResponse(**valid_data)
    assert sales_top_product.name == "Product A"
    assert sales_top_product.sold_amount == 50

def test_sales_top_products_response_invalid():
    invalid_data = {"name": "Product A", "sold_amount": "invalid"}
    with pytest.raises(ValidationError):
        SalesTopProductsResponse(**invalid_data)
    
    invalid_data = {"name": 123, "sold_amount": 50}
    with pytest.raises(ValidationError):
        SalesTopProductsResponse(**invalid_data)

