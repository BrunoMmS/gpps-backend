from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.user_model import UserModel
from entities.user_entity import UserEntity 

class UserDAO:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_by_email(self, db: Session, email: str) -> UserModel | None:
        return db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> UserModel | None:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    def create(self, db: Session, user_entity: UserEntity) -> UserModel:
        hashed_password = self.pwd_context.hash(user_entity.getPassword())

        db_user = UserModel(
            username=user_entity.getUsername(),
            lastname=user_entity.getLastname(),
            email=user_entity.getEmail(),
            password=hashed_password,
            role=user_entity.getRole()
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def list(self, db: Session, skip: int = 0, limit: int = 10) -> list[UserModel]:
        return db.query(UserModel).offset(skip).limit(limit).all()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate(self, db: Session, login_data: UserEntity) -> UserModel | None:
        user = self.get_by_email(db, login_data.getEmail())
        if not user or not self.verify_password(login_data.password, user.password):
            return None
        return user
