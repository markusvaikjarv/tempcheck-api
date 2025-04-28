from fastapi import APIRouter
from pydantic import Field
from src.provisionings.schemas import NewProvisioning
from src.provisionings import model
from typing import Annotated
from fastapi import Depends
from src.auth.authorizers import get_user_id

router = APIRouter(prefix="/provisionings")

@router.get("/")
async def get_provisionings(user_id: Annotated[str, Depends(get_user_id)]):
    return await model.get_user_provisionings(user_id)

@router.post("/")
async def create_provisioning(user_id: Annotated[str, Depends(get_user_id)], provisioning: NewProvisioning):
    return await model.create_provisioning(user_id, provisioning.display_name)

