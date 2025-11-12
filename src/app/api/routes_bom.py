"""BOM parsing routes."""
from fastapi import APIRouter, File, UploadFile, status

from ..services import bom_parser

router = APIRouter(prefix="/v1/bom", tags=["bom"])


@router.post("/parse", status_code=status.HTTP_200_OK)
async def parse_bom_endpoint(file: UploadFile = File(...)) -> dict:
    file_bytes = await file.read()
    response = bom_parser.parse_bom(file_bytes, file.filename)
    return response.model_dump()
