from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Date, Float, UniqueConstraint

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
    password = Column(String(255), nullable=False)
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
    amount = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=True)

    def __repr__(self):
        return f"Discount(id={self.id}, amount={self.amount}, name={self.name})"


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(255), nullable=False)
    balance = Column(Integer, default=0)
    address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    block_date = Column(DateTime, nullable=True)
    registered_date = Column(DateTime, default=datetime.utcnow)
    is_on_credit = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    discount_id = Column(Integer, ForeignKey("discounts.id"), nullable=True)

    user = relationship("User", backref="agents")
    discount = relationship("Discount", backref="agents")

    def __repr__(self):
        return f"Agent(id={self.id}, balance={self.balance})"


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name_ru = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    name_uz = Column(String(255), nullable=True)

    def __repr__(self):
        return f"Section(id={self.id}, name={self.name_ru})"


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    alias = Column(String(255), nullable=False)
    title_ru = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=True)
    title_uz = Column(String(255), nullable=True)
    description = Column(String(560), nullable=True)

    section = relationship("Section", backref="permissions")

    def __repr__(self):
        return f"Permission(id={self.id}, name={self.title_ru})"


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)

    __table_args__ = (UniqueConstraint('role_id', 'permission_id', name='_role_permission_uc'),)

    role = relationship("Role", backref="role_permissions")
    permission = relationship("Permission", backref="role_permissions")

    def __repr__(self):
        return f"RolePermission(id={self.id}, role_id={self.role_id}, permission_id={self.permission_id})"


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    country_ru = Column(String(255), nullable=False)
    country_en = Column(String(255), nullable=True)
    country_uz = Column(String(255), nullable=True)
    code = Column(String(3), nullable=True)

    def __repr__(self):
        return f"Country(id={self.id}, country_ru={self.country_ru}, short_name={self.short_name})"


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    city_ru = Column(String(255), nullable=False)
    city_en = Column(String(255), nullable=True)
    city_uz = Column(String(255), nullable=True)
    code = Column(String(3), nullable=True)
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
    code = Column(String(3), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    city = relationship("City", backref="airports")

    def __repr__(self):
        return f"Airport(id={self.id}, airport_ru={self.airport_ru}, city_id={self.city_id})"


class CurrencyCode(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    UZS = "UZS"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    icon = Column(String(510), nullable=True)
    code = Column(String(3), nullable=True)
    description = Column(String(510), nullable=True)

    def __repr__(self):
        return f"Company(id={self.id}, name={self.name})"


class FlightGuide(Base):
    __tablename__ = "flight_guides"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    flight_number = Column(String(255), nullable=False, unique=True)
    from_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    to_airport_id = Column(Integer, ForeignKey("airports.id"), nullable=False)
    luggage = Column(Integer, default=0)
    baggage_weight = Column(Integer, default=0, nullable=True)

    company = relationship("Company", backref="flight_guides")
    from_airport = relationship("Airport", foreign_keys=[from_airport_id])
    to_airport = relationship("Airport", foreign_keys=[to_airport_id])

    def __repr__(self):
        return f"FlightGuide(id={self.id}, flight_number={self.flight_number}, from_airport_id={self.from_airport_id}, \
               to_airport_id={self.to_airport_id})"


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_guide_id = Column(Integer, ForeignKey("flight_guides.id"), nullable=False)
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

    flight_guide = relationship("FlightGuide", backref="flights")
    actor = relationship("User", backref="flights")

    def __repr__(self):
        return f"Flight(id={self.id}, flight_number={self.flight_number}, departure_date={self.departure_date}, " \
               f"arrival_date={self.arrival_date}, price={self.price}, currency={self.currency}, " \
               f"total_seats={self.total_seats}, left_seats={self.left_seats}, on_sale={self.on_sale}, " \
               f"actor_id={self.actor_id})"


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
        return f"FlightPriceHistory(id={self.id}, flight_id={self.flight_id}, new_price={self.new_price}, " \
               f"currency={self.currency})"


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
        return f"ScrapedPrice(id={self.id}, flight_id={self.flight_id}, price={self.price}, " \
               f"currency={self.currency}, name={self.name})"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hard_block = Column(Integer, default=0)
    soft_block = Column(Integer, default=0)
    price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    __tablde_args__ = (UniqueConstraint('flight_id', 'agent_id', name='unique_booking'),)

    flight = relationship("Flight", backref="bookings")
    agent = relationship("Agent", backref="bookings")
    actor = relationship("User", backref="bookings")

    def __repr__(self):
        return f"Booking(id={self.id}, flight_id={self.flight_id}, actor_id={self.actor_id}), agent_id={self.agent_id})"


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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

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


class TicketClass(Base):
    __tablename__ = 'ticket_classes'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name_ru = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    name_uz = Column(String(255), nullable=True)
    code = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"TicketClass(id={self.id}, name={self.name})"


class TicketStatus(Base):
    __tablename__ = 'ticket_statuses'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name_ru = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    name_uz = Column(String(255), nullable=True)

    def __repr__(self):
        return f"TicketStatus(id={self.id}, name={self.name_ru})"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    ticket_number = Column(String(255), nullable=False)
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
    class_id = Column(Integer, ForeignKey('ticket_classes.id'), nullable=False)
    price = Column(Integer, default=0)
    currency = Column(Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), default='RUB')
    discount_id = Column(Integer, ForeignKey('discounts.id'), nullable=True)
    comment = Column(String(255), nullable=True)
    taking_amount = Column(Integer, default=0)  # Сумма, которую берет агент/кассир/бронзировщик за бронирование
    luggage = Column(Boolean, default=False)
    is_booked = Column(Boolean, default=False)
    platform = Column(Enum('web', 'ios', 'android', name='Platform'), default='web')
    status_id = Column(Integer, ForeignKey('ticket_statuses.id'), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    flight = relationship("Flight", backref="tickets")
    agent = relationship("Agent", backref="tickets")
    passenger = relationship("Passenger", backref="tickets")
    gender = relationship("Gender", backref="tickets")
    class_ = relationship("TicketClass", backref="tickets")
    discount = relationship("Discount", backref="tickets")
    status = relationship("TicketStatus", backref="tickets")
    actor = relationship("User", backref="tickets")

    def __repr__(self):
        return f"Ticket(id={self.id}, flight_id={self.flight_id}, passenger_id={self.passenger_id}), " \
               f"agent_id={self.agent_id})"


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
        return f"Transaction(id={self.id}, passenger={self.passenger}, ticket={self.ticket}, " \
               f"payment_system={self.payment_system}, status={self.status})"


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    rub_to_usd = Column(Float, default=0)
    rub_to_eur = Column(Float, default=0)
    rub_to_uzs = Column(Float, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Refill(Base):
    __tablename__ = 'refills'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    amount = Column(Integer, default=0)
    comment = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    receiver = relationship("User", backref="refills")
    agent = relationship("Agent", backref="refills")

    def __repr__(self):
        return f"Refill(id={self.id}, agent={self.agent})"


class AgentDebt(Base):
    __tablename__ = 'agent_debts'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    type = Column(Enum('fine', 'purchase', name='DebtType'), default='fine')
    amount = Column(Integer, default=0)
    comment = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    agent = relationship("Agent", backref="debts")
    flight = relationship("Flight", backref="debts")
    ticket = relationship("Ticket", backref="debts")

    def __repr__(self):
        return f"AgentDebt(id={self.id}, agent={self.agent})"
