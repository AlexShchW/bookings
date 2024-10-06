"""Seed initial data

Revision ID: d5d0160e5152
Revises: 8bb0aed547ae
Create Date: 2024-10-06 03:31:12.015330

"""
from typing import Sequence, Union

from alembic import op
import os
from sqlalchemy import text
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd5d0160e5152'
down_revision: Union[str, None] = '8bb0aed547ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'initial_db_data.sql')
    with open(sql_file_path, 'r') as f:
        sql_content = f.read()

    sql_statements = sql_content.split(';')

    sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]

    connection = op.get_bind()
    for stmt in sql_statements:
        if stmt:
            connection.execute(text(stmt))

def downgrade():
    op.drop_table("bookings")
    op.drop_table("rooms")
    op.drop_table("users")
    op.drop_table("hotels")
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("services", sa.JSON(), nullable=True),
        sa.Column("rooms_quantity", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("services", sa.JSON(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "total_cost",
            sa.Integer(),
            sa.Computed(
                "(date_to - date_from) * price",
            ),
            nullable=True,
        ),
        sa.Column(
            "total_days",
            sa.Integer(),
            sa.Computed(
                "date_to - date_from",
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )