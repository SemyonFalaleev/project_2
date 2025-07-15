from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response
from fastapi import UploadFile
from src.db.models.article_model import Article
from src.dto.article_dto import ArticleDTOGetMin, ArticleDTOCreate
from src.db.init_db import AsyncSession, get_async_db
from sqlalchemy.exc import IntegrityError
from src.utils.aws_interface import client_s3
from decouple import config

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleDTOGetMin,
)
async def create_article(cover_image: UploadFile,
                         request: Request,
                         data: ArticleDTOCreate = Depends(ArticleDTOCreate.as_form),
                         session: AsyncSession = Depends(get_async_db)):
    
    cover_image_url = client_s3.upload_file_from_stream(cover_image)

    data_dict = data.model_dump(exclude={"cover_image_url", "user_id"})
    new_obj = Article(**data_dict, cover_image_url=cover_image_url,
                      user_id = request.state.user.get("user_id"))

    try:
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
    except IntegrityError:
        return Response(content="A article with such name already exists",
                        status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as exp:
        return Response(content=f"{exp}",
                        status_code=422)
    
    return new_obj