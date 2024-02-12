from requests import get, post, delete

print(get('http://localhost:5001/api/v1/basket').json())
print(get('http://localhost:5001/api/v1/products/category-6').json())
print(get('http://localhost:5001/api/v1/products/category-1').json())
print(get('http://localhost:5001/api/v1/products/category-0').json())

