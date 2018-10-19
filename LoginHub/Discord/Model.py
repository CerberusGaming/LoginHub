import datetime
from LoginHub.App.Storage import Base
from sqlalchemy import Column, DateTime, String, Integer, Boolean


class DiscordTokens(Base):
    __tablename__ = "discord_tokens"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(255))
    token_type = Column(String(255))
    expires = Column(DateTime, datetime.datetime.utcnow() + datetime.timedelta(weeks=1))
    refresh_token = Column(String(255))
    scope = Column(String(255))
    expired = Column(Boolean, default=False)
