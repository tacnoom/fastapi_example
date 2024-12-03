from fastapi import APIRouter,status, HTTPException, Depends
from .. import models 
from .. import utils
from .. import database
from typing import List
from sqlmodel import select, text, func
from typing import Optional
from .oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model=List[models.PostOut])
def get_posts(session:database.SessionDep, user_id: models.UserOut = Depends(get_current_user), limit: int =1, search: Optional[str]=""):
    print('###################')

    query = '''
    (SELECT a.*, count(user_id) as votes
    FROM public.posts a
    left join
    public.votes b 
    on a.id = b.post_id
    group by id)
    '''


    # posts = session.exec(select(models.Posts).where((models.Posts.owner_id==user_id.id) & (models.Posts.title.contains(search))).limit(limit)).all()

    posts = session.exec(select(models.Posts, func.count(models.Votes.user_id).label("votes") ).join(models.Votes, models.Votes.post_id==models.Posts.id, isouter=True).group_by(models.Posts.id)).all()
    
    serialized_posts = [{**p.dict(),'votes':v} for p, v in posts]

    # posts = session.exec(text(query)).all()
    print(serialized_posts)
    return serialized_posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=models.PostResponse)
def create_post(payload: models.Posts, session: database.SessionDep, user_id: models.User = Depends(get_current_user) ):

    # sql_string = '''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *'''

    # cursor.execute(sql_string, (payload.title,payload.content, payload.published))

    # results = cursor.fetchone() # fetch the result
    # conn.commit() # push the changes
    print(user_id.id, '##################################', payload)
    payload.owner_id =  user_id.id
    session.add(payload)
    session.commit()
    session.refresh(payload)

    return payload

@router.get('/{id}', response_model=models.PostResponse)
def get_one_post(id: int, session: database.SessionDep, user_id: models.UserOut = Depends(get_current_user)):

    one_post = session.get(models.Posts, id)

    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'no id of {id} found')

    return one_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: database.SessionDep,user_id: models.UserOut = Depends(get_current_user)):
    

    owner_id = session.exec(select(models.Posts).where(models.Posts.id ==id)).one().owner_id
    print(owner_id, user_id.id)

    if user_id.id ==owner_id:
        post = session.get(models.Posts, id)
        session.delete(post)
        session.commit()
        return {'ok': True}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "you cannot delete another user's post")


@router.put('/{id}', response_model=models.PostResponse)
def update_posts(id:int, post: models.UpdatePost, session: database.SessionDep):

    # sql = '''UPDATE posts SET title = %s, content = %s  WHERE id = %s RETURNING *'''
    # cursor.execute(sql, (post.title, post.content, str(id)))
    # result = cursor.fetchone()

    # if pd.isna(result):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'no id found with id {id}')
    
    # else:
    #     conn.commit()

    post_db = session.get(models.Posts, id)

    new_post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(new_post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)

    return post_db
