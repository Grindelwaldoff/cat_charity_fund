from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationCreate


donation_crud = CRUDBase[Donation, DonationCreate, None](Donation)
