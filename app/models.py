import sqlalchemy as sa
import sqlalchemy.orm as so

from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class Users(UserMixin, db.Model):
    __tablename__ = 'user'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(10), unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    @login.user_loader
    def load_user(id):
        return db.session.get(Users, int(id))
    
    
    def __repr__(self) -> str:
        return f"class Users: {self.name}"


class Sections(db.Model):
    __tablename__ = 'section'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(100))

    sec_products: so.Mapped[list['Products']] = so.relationship(
        passive_deletes=True,
        back_populates='sections'
    )

    
    def __repr__(self) -> str:
        return f"class Sections: {self.name}"
    

class Products(db.Model):
    __tablename__ = 'product'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(300))
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    link: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    is_active: so.Mapped[bool] = so.mapped_column(default=True)

    section_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('section.id'))
    sections: so.Mapped['Sections'] = so.relationship(
        passive_deletes=True,
        back_populates='sec_products'
    )

    
    def __repr__(self) -> str:
        return f"class Product {self.name}"
    