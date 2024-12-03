from fastapi import APIRouter, status, Depends, HTTPException
from .oauth2 import get_current_user
from ..models import User
from ..database import SessionDep
from .. import models
from sqlmodel import select




router = APIRouter(
    prefix='/votes'
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def vote_post(payload: models.VoteOut , session: SessionDep, current_user:  User = Depends(get_current_user)):
 
    record_found = session.exec(select(models.Votes).where(models.Votes.post_id==payload.post_id, models.Votes.user_id==current_user.id)).first()

    if not record_found:
        if payload.up_direction == True:
            session.add(models.Votes(user_id=current_user.id, post_id=payload.post_id))
            session.commit()
            session.refresh(models.Votes)
        if payload.up_direction == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'cannot dislike non existent post')
    if record_found:
        if payload.up_direction == True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='post already liked')
        if payload.up_direction == False:
            session.delete(record_found)
            session.commit()
            # session.refresh(models.Votes)


    print(record_found)
    return {'message': 'success'}