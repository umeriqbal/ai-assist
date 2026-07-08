from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():

    return {
        "message": "Enterprise AI Assistant",
    }


@router.get("/health")
async def health():

    return {
        "status": "healthy",
    }