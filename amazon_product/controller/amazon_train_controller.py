from fastapi import APIRouter

from amazon_product.service.amazon_train_service import AmazonTrainService

router = APIRouter(
    prefix="/amazon",
    tags=['Coffee'],
    responses={404: {'message': "Not found"}}
)

amazon_train_service = AmazonTrainService()


@router.get('/train')
def get_size():
    amazon_train_service.train_model()
    return {
        "message": "ok"
    }
