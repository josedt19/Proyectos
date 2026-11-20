from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
import database
import enum

class UserRole(str, enum.Enum):
    NORMAL = "normal"
    ADMIN = "admin"

class MatchStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    LIVE = "live"
    FINISHED = "finished"

class ChallengeType(str, enum.Enum):
    PREDICTION = "prediction"
    ANALYSIS = "analysis"
    TACTIC = "tactic"
    PLAYERS = "players"

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.NORMAL, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    predictions = relationship("Prediction", back_populates="user")
    responses = relationship("ChallengeResponse", back_populates="user")
    score_history = relationship("ScoreHistory", back_populates="user")

class Team(database.Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    shield_url = Column(String(255), nullable=True)
    is_demo = Column(Boolean, default=True, nullable=False)

class Match(database.Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    competition = Column(String(100), nullable=False)
    match_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.UPCOMING, nullable=False, index=True)
    home_score = Column(Integer, default=0, nullable=False)
    away_score = Column(Integer, default=0, nullable=False)
    is_demo = Column(Boolean, default=True, nullable=False)

    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    predictions = relationship("Prediction", back_populates="match")
    challenges = relationship("Challenge", back_populates="match")

class Prediction(database.Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    predicted_home_score = Column(Integer, nullable=False)
    predicted_away_score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'match_id', name='uq_user_match_prediction'),)

    user = relationship("User", back_populates="predictions")
    match = relationship("Match", back_populates="predictions")

class Challenge(database.Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    challenge_type = Column(Enum(ChallengeType), nullable=False)
    difficulty = Column(String(20), default="Medium", nullable=False)
    max_score = Column(Integer, default=10, nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    match = relationship("Match", back_populates="challenges")
    responses = relationship("ChallengeResponse", back_populates="challenge")

class ChallengeResponse(database.Base):
    __tablename__ = "challenge_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    answer_data = Column(Text, nullable=False)
    awarded_points = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'challenge_id', name='uq_user_challenge_response'),)

    user = relationship("User", back_populates="responses")
    challenge = relationship("Challenge", back_populates="responses")

class ScoreHistory(database.Base):
    __tablename__ = "score_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points_change = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="score_history")