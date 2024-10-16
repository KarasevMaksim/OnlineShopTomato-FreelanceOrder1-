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
    name: so.Mapped[str] = so.mapped_column(sa.String(11), unique=True)
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
        return f'class Users: {self.name}'


class Sections(db.Model):
    __tablename__ = 'section'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    sub_sections: so.Mapped[list['SubSections']] = so.relationship(
        'SubSections',
        back_populates='section',
        cascade='all, delete-orphan'
    )
    products: so.Mapped[list['Products']] = so.relationship(
        'Products',
        secondary='section_product_association',
        back_populates='section'
    )

    
    def __repr__(self) -> str:
        return f'class Sections: {self.name}'
    
    
class SubSections(db.Model):
    __tablename__ = 'sub_section'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(100))

    section_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('section.id', ondelete='CASCADE')
    )
    section: so.Mapped['Sections'] = so.relationship(
        'Sections',
        back_populates='sub_sections'
    )
    products: so.Mapped[list['Products']] = so.relationship(
        'Products',
        back_populates='sub_section',
        cascade='all, delete-orphan'
    )

    
    def __repr__(self) -> str:
        return f'class SubSections: {self.name}'
    

class Products(db.Model):
    __tablename__ = 'product'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(300))
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    about: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    img_link: so.Mapped[str] = so.mapped_column(sa.String(100))
    is_active: so.Mapped[bool] = so.mapped_column(default=True)

    sub_section_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('sub_section.id', ondelete='CASCADE')
    )
    sub_section: so.Mapped['SubSections'] = so.relationship(
        'SubSections',
        back_populates='products'
    )
    section: so.Mapped['Sections'] = so.relationship(
        'Sections',
        secondary='section_product_association',
        back_populates='products'
    )

    
    def __repr__(self) -> str:
        return f'class Product {self.name}'
    

class SectionProductAssociation(db.Model):
    __tablename__ = 'section_product_association'
    
    section_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('section.id'),
        primary_key=True
    )
    product_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('product.id'),
        primary_key=True
    )

    
class News(db.Model):
    __tablename__ = 'news'
    id: so.Mapped[int] = so.mapped_column(
       primary_key=True,
       autoincrement=True 
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(300))
    post: so.Mapped[str] = so.mapped_column(sa.Text)


class Contacts(db.Model):
    __tablename__ = 'contact'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    phone: so.Mapped[str] = so.mapped_column(sa.String(50))
    email: so.Mapped[str] = so.mapped_column(sa.String(100))


class About(db.Model):
    __tablename__ = 'about'
    id: so.Mapped[int] = so.mapped_column(
       primary_key=True,
       autoincrement=True 
    )
    about: so.Mapped[str] = so.mapped_column(sa.Text)


class SellAndBy(db.Model):
    __tablename__ = 'sell_and_by'
    id: so.Mapped[int] = so.mapped_column(
       primary_key=True,
       autoincrement=True 
    )
    sell_and_by: so.Mapped[str] = so.mapped_column(sa.Text)


class HistoryProducts(db.Model):
    __tablename__ = 'history_product'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name_user: so.Mapped[str] = so.mapped_column(sa.String(300))
    email_user: so.Mapped[str] = so.mapped_column(sa.String(300))
    phone_user: so.Mapped[str] = so.mapped_column(sa.String(300))
    
    name_product: so.Mapped[str] = so.mapped_column(sa.String(300))
    about_product: so.Mapped[str] = so.mapped_column(sa.Text)
    price: so.Mapped[int] = so.mapped_column(sa.Integer)
    total_price: so.Mapped[int] = so.mapped_column(sa.Integer)
    count: so.Mapped[int] = so.mapped_column(sa.Integer) 
    img_link: so.Mapped[str] = so.mapped_column(sa.String(100))
    section: so.Mapped[str] = so.mapped_column(sa.String(300))
    sub_section: so.Mapped[str] = so.mapped_column(sa.String(300))
    link_to_product: so.Mapped[str] = so.mapped_column(sa.String(300))
    sales_id: so.Mapped[int] = so.mapped_column(
            sa.ForeignKey('history_sales.id', ondelete='CASCADE')
    )
    h_sales: so.Mapped['HistorySales'] = so.relationship(
        'HistorySales',
        back_populates='h_prod'
    )



class HistorySales(db.Model):
    __tablename__ = 'history_sales'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    h_prod: so.Mapped[list['HistoryProducts']] = so.relationship(
        'HistoryProducts',
        back_populates='h_sales',
        cascade='all, delete-orphan'
    )