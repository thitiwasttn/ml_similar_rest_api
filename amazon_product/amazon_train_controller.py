from fastapi import APIRouter

router = APIRouter(
    prefix="/amazon",
    tags=['Coffee'],
    responses={404: {'message': "Not found"}}
)


@router.get('/train')
def get_size():

    return {
        "message": "ok"
    }