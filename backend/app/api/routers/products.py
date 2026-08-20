import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas.product import ProductCreate
from app.services.database import products_collection


router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post("/")
def create_product(product: ProductCreate):
    product_id = f"PROD-{uuid.uuid4().hex[:8].upper()}"

    product_document = {
        "product_id": product_id,
        "crop_name": product.crop_name,
        "quantity": product.quantity,
        "unit": product.unit,
        "farmer_id": product.farmer_id,
        "harvest_date": product.harvest_date.isoformat(),
        "location": product.location,
        "quality_grade": product.quality_grade,
        "created_at": datetime.now(timezone.utc),
    }

    products_collection.insert_one(product_document)

    return {
        "success": True,
        "product": {
            "product_id": product_id,
            "crop_name": product.crop_name,
            "quantity": product.quantity,
            "unit": product.unit,
            "farmer_id": product.farmer_id,
            "harvest_date": product.harvest_date.isoformat(),
            "location": product.location,
            "quality_grade": product.quality_grade,
        }
    }


@router.get("/{product_id}")
def get_product(product_id: str):
    product = products_collection.find_one(
        {"product_id": product_id},
        {"_id": 0}
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "Product was not found"
                }
            }
        )

    # MongoDB stores datetime objects which are not directly
    # returned by our agreed JSON contract.
    if "created_at" in product:
        product.pop("created_at")

    return {
        "success": True,
        "product": product
    }