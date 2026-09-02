from fastapi import FastAPI, Query, Path

app = FastAPI()


# This is called path parameters
@app.get("/students/{student_id}")
def get_student(student_id: int = Path(ge=1)):
    return {"student_id": student_id}


@app.get("/products/{product_id}")
def get_product(
        product_id: int = Path(ge=1, le=10000),
        include_reviews: bool = False):
    return {
        "product_id": product_id,
        "include_reviews": include_reviews}


# FastAPI expects an age query parameter.
# if we search /students, it shows an error
@app.get("/students")
def get_students(age: int):
    return {"age": age}


# query parameters can have initial value. When it has initial value, by searching /products we can see them
# we can search it either /products?category=laptop or /products?category=laptop&min_price=500.0
# by Query(), we can comfortably alternate our parameters by selecting max, min, length and so on
# Required vs Optional Parameters: Having the initial value- optional. Not having the initial value- required.
# i.e, category is required and min_price is optional.
@app.get("/products")
def get_products(
        category: str = Query(min_length=3),
        min_price: float = Query(0.0, ge=0)):
    return {"category": category,
            "min_price": min_price}


@app.get("/products/{product_id}/search")  # endpoint
def search_products(
        product_id: int = Path(ge=1, le=10000),
        keyword: str = Query(min_length=2),
        min_price: float = Query(0.0, ge=0),
        limit: int = Query(10, ge=1, le=100)):

    return {
        "product_id": product_id,
        "keyword": keyword,
        "min_price": min_price,
        "limit": limit
    }

