from sqlalchemy import create_engine, String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os, requests
from dotenv import load_dotenv

load_dotenv()

PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@localhost:5432/parfume_store",
    echo=True,
)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)


class Parfume(Base):
    __tablename__ = "parfumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(255), nullable=False)
    price_old: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    picture: Mapped[str] = mapped_column(String(255), nullable=False)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="parfume")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    parfume_id: Mapped[int] = mapped_column(ForeignKey("parfumes.id"), nullable=False)
    parfume: Mapped["Parfume"] = relationship("Parfume", back_populates="orders")


def init_db():
    base = Base()
    base.create_db()


if __name__ == "__main__":
    init_db()
