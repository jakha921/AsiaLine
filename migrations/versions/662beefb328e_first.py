"""first

Revision ID: 662beefb328e
Revises: 
Create Date: 2023-02-23 00:28:55.582937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662beefb328e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('icon', sa.String(length=510), nullable=True),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.Column('description', sa.String(length=510), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=True)
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_ru', sa.String(length=255), nullable=False),
    sa.Column('country_en', sa.String(length=255), nullable=True),
    sa.Column('country_uz', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_countries_id'), 'countries', ['id'], unique=True)
    op.create_table('currency_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rub_to_usd', sa.Float(), nullable=True),
    sa.Column('rub_to_eur', sa.Float(), nullable=True),
    sa.Column('rub_to_uzs', sa.Float(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currency_rates_id'), 'currency_rates', ['id'], unique=True)
    op.create_table('discounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_discounts_id'), 'discounts', ['id'], unique=True)
    op.create_table('genders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gender_ru', sa.String(length=255), nullable=False),
    sa.Column('gender_en', sa.String(length=255), nullable=True),
    sa.Column('gender_uz', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genders_id'), 'genders', ['id'], unique=True)
    op.create_table('passengers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('login', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('platform', sa.Enum('web', 'ios', 'android', name='Platform'), nullable=True),
    sa.Column('language', sa.Enum('ru', 'en', 'uz', name='Language'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_passengers_id'), 'passengers', ['id'], unique=True)
    op.create_table('payment_systems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('icon', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_systems_id'), 'payment_systems', ['id'], unique=True)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('title_ru', sa.String(length=255), nullable=False),
    sa.Column('title_en', sa.String(length=255), nullable=True),
    sa.Column('title_uz', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=True)
    op.create_table('sections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('name_uz', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sections_id'), 'sections', ['id'], unique=True)
    op.create_table('ticket_classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('name_uz', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_classes_id'), 'ticket_classes', ['id'], unique=True)
    op.create_table('ticket_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_ru', sa.String(length=255), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('name_uz', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_statuses_id'), 'ticket_statuses', ['id'], unique=True)
    op.create_table('transaction_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alias', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_statuses_id'), 'transaction_statuses', ['id'], unique=True)
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_ru', sa.String(length=255), nullable=False),
    sa.Column('city_en', sa.String(length=255), nullable=True),
    sa.Column('city_uz', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cities_id'), 'cities', ['id'], unique=True)
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('alias', sa.String(length=255), nullable=False),
    sa.Column('title_ru', sa.String(length=255), nullable=False),
    sa.Column('title_en', sa.String(length=255), nullable=True),
    sa.Column('title_uz', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=560), nullable=True),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_id'), 'permissions', ['id'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('language', sa.Enum('ru', 'en', 'uz', name='Language'), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('agents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('block_date', sa.DateTime(), nullable=True),
    sa.Column('registered_date', sa.DateTime(), nullable=True),
    sa.Column('is_on_credit', sa.Boolean(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('discount_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['discount_id'], ['discounts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agents_id'), 'agents', ['id'], unique=True)
    op.create_table('airports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('airport_ru', sa.String(length=255), nullable=False),
    sa.Column('airport_en', sa.String(length=255), nullable=True),
    sa.Column('airport_uz', sa.String(length=255), nullable=True),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_airports_id'), 'airports', ['id'], unique=True)
    op.create_table('role_permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role_id', 'permission_id', name='_role_permission_uc')
    )
    op.create_index(op.f('ix_role_permissions_id'), 'role_permissions', ['id'], unique=True)
    op.create_table('user_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Enum('create flight', 'update flight', 'delete flight', 'create ticket', 'update ticket', 'cancel ticket', 'create booking', 'update booking', 'delete booking', 'create user', 'update user', 'delete user', 'create agent', 'update agent', 'delete agent', 'create agent debit', 'update agent debit', 'delete agent debit', 'create discount', 'update discount', 'delete discount', 'create role', 'update role', 'delete role', 'create country', 'update country', 'delete country', 'create city', 'update city', 'delete city', 'create airport', 'update airport', 'delete airport', 'create company', 'update company', 'delete company', 'create flight guide', 'update flight guide', 'delete flight guide', name='Action'), nullable=False),
    sa.Column('extra_info', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_history_id'), 'user_history', ['id'], unique=True)
    op.create_table('flight_guides',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('flight_number', sa.String(length=255), nullable=False),
    sa.Column('from_airport_id', sa.Integer(), nullable=False),
    sa.Column('to_airport_id', sa.Integer(), nullable=False),
    sa.Column('luggage', sa.Integer(), nullable=True),
    sa.Column('baggage_weight', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['from_airport_id'], ['airports.id'], ),
    sa.ForeignKeyConstraint(['to_airport_id'], ['airports.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('flight_number')
    )
    op.create_index(op.f('ix_flight_guides_id'), 'flight_guides', ['id'], unique=True)
    op.create_table('refills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_refills_id'), 'refills', ['id'], unique=True)
    op.create_table('flights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_guide_id', sa.Integer(), nullable=False),
    sa.Column('departure_date', sa.DateTime(), nullable=False),
    sa.Column('arrival_date', sa.DateTime(), nullable=False),
    sa.Column('purchase_price', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('currency', sa.Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), nullable=True),
    sa.Column('total_seats', sa.Integer(), nullable=True),
    sa.Column('left_seats', sa.Integer(), nullable=True),
    sa.Column('online_seats', sa.Integer(), nullable=True),
    sa.Column('on_sale', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['flight_guide_id'], ['flight_guides.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flights_id'), 'flights', ['id'], unique=True)
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('hard_block', sa.Integer(), nullable=True),
    sa.Column('soft_block', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('currency', sa.Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bookings_id'), 'bookings', ['id'], unique=True)
    op.create_table('flight_price_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('new_price', sa.Integer(), nullable=True),
    sa.Column('currency', sa.Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flight_price_history_id'), 'flight_price_history', ['id'], unique=True)
    op.create_table('scraped_prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('currency', sa.Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scraped_prices_id'), 'scraped_prices', ['id'], unique=True)
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_number', sa.String(length=255), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('passenger_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('surname', sa.String(length=100), nullable=False),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('gender_id', sa.Integer(), nullable=False),
    sa.Column('passport', sa.String(length=10), nullable=False),
    sa.Column('passport_expires', sa.Date(), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('citizenship', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('currency', sa.Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), nullable=True),
    sa.Column('discount_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('taking_amount', sa.Integer(), nullable=True),
    sa.Column('luggage', sa.Boolean(), nullable=True),
    sa.Column('is_booked', sa.Boolean(), nullable=True),
    sa.Column('platform', sa.Enum('web', 'ios', 'android', name='Platform'), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.ForeignKeyConstraint(['citizenship'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['class_id'], ['ticket_classes.id'], ),
    sa.ForeignKeyConstraint(['discount_id'], ['discounts.id'], ),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['passengers.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['ticket_statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=True)
    op.create_table('agent_debts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('fine', 'purchase', name='DebtType'), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_debts_id'), 'agent_debts', ['id'], unique=True)
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('passenger_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('payment_system_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('currency', sa.Enum('RUB', 'USD', 'EUR', 'UZS', name='CurrencyCode'), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('is_online_payment', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.ForeignKeyConstraint(['passenger_id'], ['passengers.id'], ),
    sa.ForeignKeyConstraint(['payment_system_id'], ['payment_systems.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['transaction_statuses.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_agent_debts_id'), table_name='agent_debts')
    op.drop_table('agent_debts')
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')
    op.drop_index(op.f('ix_scraped_prices_id'), table_name='scraped_prices')
    op.drop_table('scraped_prices')
    op.drop_index(op.f('ix_flight_price_history_id'), table_name='flight_price_history')
    op.drop_table('flight_price_history')
    op.drop_index(op.f('ix_bookings_id'), table_name='bookings')
    op.drop_table('bookings')
    op.drop_index(op.f('ix_flights_id'), table_name='flights')
    op.drop_table('flights')
    op.drop_index(op.f('ix_refills_id'), table_name='refills')
    op.drop_table('refills')
    op.drop_index(op.f('ix_flight_guides_id'), table_name='flight_guides')
    op.drop_table('flight_guides')
    op.drop_index(op.f('ix_user_history_id'), table_name='user_history')
    op.drop_table('user_history')
    op.drop_index(op.f('ix_role_permissions_id'), table_name='role_permissions')
    op.drop_table('role_permissions')
    op.drop_index(op.f('ix_airports_id'), table_name='airports')
    op.drop_table('airports')
    op.drop_index(op.f('ix_agents_id'), table_name='agents')
    op.drop_table('agents')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_permissions_id'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_cities_id'), table_name='cities')
    op.drop_table('cities')
    op.drop_index(op.f('ix_transaction_statuses_id'), table_name='transaction_statuses')
    op.drop_table('transaction_statuses')
    op.drop_index(op.f('ix_ticket_statuses_id'), table_name='ticket_statuses')
    op.drop_table('ticket_statuses')
    op.drop_index(op.f('ix_ticket_classes_id'), table_name='ticket_classes')
    op.drop_table('ticket_classes')
    op.drop_index(op.f('ix_sections_id'), table_name='sections')
    op.drop_table('sections')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_payment_systems_id'), table_name='payment_systems')
    op.drop_table('payment_systems')
    op.drop_index(op.f('ix_passengers_id'), table_name='passengers')
    op.drop_table('passengers')
    op.drop_index(op.f('ix_genders_id'), table_name='genders')
    op.drop_table('genders')
    op.drop_index(op.f('ix_discounts_id'), table_name='discounts')
    op.drop_table('discounts')
    op.drop_index(op.f('ix_currency_rates_id'), table_name='currency_rates')
    op.drop_table('currency_rates')
    op.drop_index(op.f('ix_countries_id'), table_name='countries')
    op.drop_table('countries')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
    # ### end Alembic commands ###
