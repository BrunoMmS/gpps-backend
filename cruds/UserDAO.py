# crud/user_dao.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models.user_model import UserModel
from schema.user_schema import UserCreate, UserLogin

class UserDAO:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_by_email(self, db: Session, email: str) -> UserModel | None:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> UserModel | None:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    def create(self, db: Session, user_data: UserCreate) -> UserModel:
        hashed_password = self.pwd_context.hash(user_data.password)
        db_user = UserModel(
            username=user_data.username,
            lastname=user_data.lastname,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def list(self, db: Session, skip: int = 0, limit: int = 10) -> list[UserModel]:
        return db.query(UserModel).offset(skip).limit(limit).all()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate(self, db: Session, login_data: UserLogin) -> UserModel | None:
        user = self.get_by_email(db, login_data.email)
        if not user or not self.verify_password(login_data.password, user.password):
            return None
        return user
