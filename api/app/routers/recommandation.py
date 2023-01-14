from sqlalchemy.orm import Session
from app import models
from app.schemas.recommandation import Recommandation, RecommandationCreate
import app.crud.recommandation as crud_reco 

router: APIRouter = APIRouter(
    prefix="/recommandation",
    tags=["Recommantations"],
)

@router.get("/", response_model=list[Recommandation], tags=["Recommandations"])
async def get_recommandations(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    order_by: RecommandationOrderBy = RecommandationOrderBy.id,
    reverse_order: bool = False,
):
    """
    Find all recommandations
    """
    res = crud_reco.get_all_recommandation(db, limit, offset, order_by, reverse_order)
    if res is None:
        raise HTTPException(status_code=404, detail="No recommandation found")
    return res



@router.put("/{", response_model=Recommandation, tags=["Recommandations"])
async def new_recommandation(
    reco: RoomCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new recommandation
    """
    try:
        res = crud_reco.create_recommandation(db, reco)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating a room ")
        logger(db, user, f"Created room {room.label}")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.delete("/{recommandation_id}", response_model=bool, tags=["Recommandations"])
async def delete_recommandation(
    recommandation_id: int, db: Session = Depends(get_db)
):
    """
    Delete a recommandation from the database
    """
    crud_reco.delete_recommandation(db, recommandation_id)
    return True
