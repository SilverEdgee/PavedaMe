import sqlalchemy as sa
from sqlalchemy.orm import registry

from pavedame.application.auth.session_model import AuthSession
from pavedame.domain.user import User

metadata = sa.MetaData()

mapper_registry = registry(metadata=metadata)

auth_table = sa.Table(
    "auth_sessions",
    metadata,
    sa.Column("id", sa.String, primary_key=True, nullable=False),
    sa.Column("user_id", sa.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    sa.Column("expiration", sa.DateTime(timezone=True), nullable=False),
    sa.Index("idx_auth_session_id", "user_id", unique=True),
)

user_table = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, nullable=False),
    sa.Column("username", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("password", sa.LargeBinary(), nullable=False),
)


def map_auth_session_table() -> None:
    mapper_registry.map_imperatively(
        AuthSession,
        auth_table,
    )


def map_user_table() -> None:
    mapper_registry.map_imperatively(
        User,
        user_table,
    )
