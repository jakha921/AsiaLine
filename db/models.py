from enum import Enum
from datetime import datetime


from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Date


from db.database import Base


class Language(str, Enum):    
    ru = "Russian"
    en = "English"
    uz = "Uzbek"


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=True)
    title_uz = Column(String(255), nullable=True)
    description = Column(String(255), nullable=False)

    def __repr__(self):
        return f"Role(id={self.id}, name={self.name}, title_en={self.title_en}, description={self.description})"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(50), index=True)
    phone = Column(String(20), nullable=True)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    language = Column(Enum("ru", "en", "uz", name="Language"), default="ru")
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    role = relationship("Role", backref="users")
    
    
    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, username={self.username}, role_id={self.role_id})"


class Discount(Base):
    __tablename__ = "discounts"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    formula = Column(String, nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"Discount(id={self.id}, formula={self.formula})"


class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    balance = Column(Integer, default=0)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    block_date = Column(DateTime, nullable=True)
    registered_date = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=True)
    
    discount = relationship("Discount", backref="agents")

    def __repr__(self):
        return f"Agent(id={self.id}, name={self.name}, address={self.address}, phone={self.phone}, mail={self.mail})"


class AgentUser(Base):
    __tablename__ = "agent_users"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)

    user = relationship("User", backref="agents")
    agent = relationship("Agent", backref="users")

    def __repr__(self):
        return f"UserAgent(id={self.id}, user_id={self.user_id}, agent_id={self.agent_id})"


class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=True)
    title_uz = Column(String(255), nullable=True)
    description = Column(String(560), nullable=True)

    def __repr__(self):
        return f"Permission(id={self.id}, name={self.name})"


class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)

    role = relationship("Role", backref="permissions")
    permission = relationship("Permission", backref="roles")

    def __repr__(self):
        return f"RolePermission(id={self.id}, role_id={self.role_id}, permission_id={self.permission_id})"


class Country(Base):
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    country_ru = Column(String(255), nullable=False)
    country_en = Column(String(255), nullable=True)
    country_uz = Column(String(255), nullable=True)
    short_name = Column(String(2), nullable=False)
    code = Column(String(3), nullable=False)

    def __repr__(self):
        return f"Country(id={self.id}, country_ru={self.country_ru}, short_name={self.short_name})"


class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    city_ru = Column(String(255), nullable=False)
    city_en = Column(String(255), nullable=True)
    city_uz = Column(String(255), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    country = relationship("Country", backref="cities")

    def __repr__(self):
        return f"City(id={self.id}, city_ru={self.city_ru}, country_id={self.country_id})"


class Airport(Base):
    __tablename__ = "airports"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    airport_ru = Column(String(255), nullable=False)
    airport_en = Column(String(255), nullable=True)
    airport_uz = Column(String(255), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    city = relationship("City", backref="airports")

    def __repr__(self):
        return f"Airport(id={self.id}, airport_ru={self.airport_ru}, city_id={self.city_id})"


class CurrencyCode(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    UZS = "UZS"


class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_number = Column(String(255), nullable=False)
    from_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    to_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    departure_date = Column(DateTime, nullable=False)
    arrival_date = Column(DateTime, nullable=False)
    price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    total_seats = Column(Integer, default=0)
    left_seats = Column(Integer, default=0)
    on_sale = Column(DateTime, nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    from_airport = relationship("Airport", foreign_keys=[from_airport_id])
    to_airport = relationship("Airport", foreign_keys=[to_airport_id])
    actor = relationship("User", backref="flights")

    def __repr__(self):
        return f"Flight(id={self.id}, flight_number={self.flight_number}, from_airport_id={self.from_airport_id}, to_airport_id={self.to_airport_id}, departure_date={self.departure_date}, arrival_date={self.arrival_date}, price={self.price}, currency={self.currency}, total_seats={self.total_seats}, left_seats={self.left_seats}, on_sale={self.on_sale}, actor_id={self.actor_id}, created_at={self.created_at}, updated_at={self.updated_at}, deleted_at={self.deleted_at})"


class FlightPriceHistory(Base):
    __tablename__ = "flight_price_history"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    new_price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    comment = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    flight = relationship("Flight", backref="price_history")

    def __repr__(self):
        return f"FlightPriceHistory(id={self.id}, flight_id={self.flight_id}, new_price={self.new_price}, currency={self.currency})"


class ScrapedPrice(Base):
    __tablename__ = "scraped_prices"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    flight = relationship("Flight", backref="scraped_prices")

    def __repr__(self):
        return f"ScrapedPrice(id={self.id}, flight_id={self.flight_id}, price={self.price}, currency={self.currency}, name={self.name})"


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_hard_block = Column(Boolean, default=False)
    sets_count = Column(Integer, default=0)
    price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    flight = relationship("Flight", backref="bookings")
    agent = relationship("Agent", backref="bookings")
    actor = relationship("User", backref="bookings")
    
    def __repr__(self):
        return f"Booking(id={self.id}, flight_id={self.flight_id}, user_id={self.user_id}), agent_id={self.agent_id})"


class Platform(str, Enum):
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"


class Passenger(Base):
    __tablename__ = "passengers"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    login = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    platform = Column(Enum('web', 'ios', 'android', name='Platform'), default='web')
    language = Column(Enum('ru', 'en', 'uz', name='Language'), default='ru')
    
    def __repr__(self):
        return f"Passenger(id={self.id}, login={self.login})"


class Gender(Base):
    __tablename__ = 'genders'
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    gender_ru = Column(String(255), nullable=False)
    gender_en = Column(String(255), nullable=True)
    gender_uz = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"Gender(id={self.id}, gender={self.gender_ru})"


class TickerClass(Base):
    __tablename__ = 'ticker_classes'
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name_ru = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    name_uz = Column(String(255), nullable=True)
    code = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"TickerClass(id={self.id}, name={self.name})"


class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=True)
    first_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    dob = Column(Date, nullable=False)
    gender_id = Column(Integer, ForeignKey('genders.id'), nullable=False)
    passport = Column(String(10), nullable=False)
    citizenship = Column(Integer, ForeignKey('countries.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('ticker_classes.id'), nullable=False)
    price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    discount_id = Column(Integer, ForeignKey('discounts.id'), nullable=True)
    comment = Column(String(255), nullable=True)
    taking_amount = Column(Integer, default=0)  # Сумма, которую берет агент/кассир/бронзировщик за бронирование
    luggage = Column(Integer, default=0)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    flight = relationship("Flight", backref="tickets")
    agent = relationship("Agent", backref="tickets")
    passenger = relationship("Passenger", backref="tickets")
    gender = relationship("Gender", backref="tickets")
    class_ = relationship("TickerClass", backref="tickets")
    discount = relationship("Discount", backref="tickets")
    actor = relationship("User", backref="tickets")
    
    def __repr__(self):
        return f"Ticket(id={self.id}, flight_id={self.flight_id}, passenger_id={self.passenger_id}), agent_id={self.agent_id})"


class PaymentSystem(Base):
    __tablename__ = 'payment_systems'
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"PaymentSystem(id={self.id}, name={self.name})"


class TransactionStatus(Base):
    __tablename__ = 'transaction_statuses'
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    alias = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"TransactionStatus(id={self.id}, alias={self.alias})"


class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    payment_system_id = Column(Integer, ForeignKey("payment_systems.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("transaction_statuses.id"), nullable=False)
    amount = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    comment = Column(String(255), nullable=True)
    is_online_payment = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    passenger = relationship("Passenger", backref="transactions")
    ticket = relationship("Ticket", backref="transactions")
    payment_system = relationship("PaymentSystem", backref="transactions")
    status = relationship("TransactionStatus", backref="transactions")
    
    def __repr__(self):
        return f"Transaction(id={self.id}, passenger={self.passenger}, ticket={self.ticket}, payment_system={self.payment_system}, status={self.status})"

