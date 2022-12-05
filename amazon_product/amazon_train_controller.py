from fastapi import APIRouter

from amazon_product.amazon_train_service import AmazonTrainService

router = APIRouter(
    prefix="/amazon",
    tags=['Coffee'],
    responses={404: {'message': "Not found"}}
)


amazon_train_service = AmazonTrainService()
@router.get('/train')
def get_size():

    return {
        "message": amazon_train_service.hello()
    }