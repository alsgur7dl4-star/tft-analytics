from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TftStaticGod(Base):
    __tablename__ = "tft_static_gods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    god_key: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    god_name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    passive_desc: Mapped[str | None] = mapped_column(Text)
    set_name: Mapped[str | None] = mapped_column(String(40))
    icon_url: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class RiotAccount(Base):
    __tablename__ = "riot_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_name: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    tag_line: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    puuid: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(20), default="KR", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    summoner: Mapped["TftSummoner | None"] = relationship(back_populates="riot_account")


class TftSummoner(Base):
    __tablename__ = "tft_summoners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    riot_account_id: Mapped[int] = mapped_column(ForeignKey("riot_accounts.id", ondelete="CASCADE"), nullable=False)
    summoner_id: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    profile_icon_id: Mapped[int | None] = mapped_column(Integer)
    summoner_level: Mapped[int | None] = mapped_column(Integer)
    region: Mapped[str] = mapped_column(String(20), default="KR", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    riot_account: Mapped[RiotAccount] = relationship(back_populates="summoner")
    league_entries: Mapped[list["TftLeagueEntry"]] = relationship(back_populates="summoner", cascade="all, delete-orphan")


class TftLeagueEntry(Base):
    __tablename__ = "tft_league_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    summoner_id: Mapped[int] = mapped_column(ForeignKey("tft_summoners.id", ondelete="CASCADE"), nullable=False)
    queue_type: Mapped[str] = mapped_column(String(80), nullable=False)
    tier: Mapped[str | None] = mapped_column(String(40))
    rank: Mapped[str | None] = mapped_column(String(10))
    league_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wins: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    summoner: Mapped[TftSummoner] = relationship(back_populates="league_entries")


class TftMatch(Base):
    __tablename__ = "tft_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(20), default="KR", nullable=False)
    set_name: Mapped[str | None] = mapped_column(String(40))
    game_version: Mapped[str | None] = mapped_column(String(80), index=True)
    queue_id: Mapped[int | None] = mapped_column(Integer)
    game_datetime: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    game_length: Mapped[float | None] = mapped_column(Float)
    raw_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    participants: Mapped[list["TftMatchParticipant"]] = relationship(back_populates="match", cascade="all, delete-orphan")


class TftMatchParticipant(Base):
    __tablename__ = "tft_match_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("tft_matches.id", ondelete="CASCADE"), index=True, nullable=False)
    puuid: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    placement: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int | None] = mapped_column(Integer)
    gold_left: Mapped[int | None] = mapped_column(Integer)
    last_round: Mapped[int | None] = mapped_column(Integer)
    players_eliminated: Mapped[int | None] = mapped_column(Integer)
    total_damage_to_players: Mapped[int | None] = mapped_column(Integer)
    traits_json: Mapped[list | None] = mapped_column(JSON)
    units_json: Mapped[list | None] = mapped_column(JSON)
    augments_json: Mapped[list | None] = mapped_column(JSON)
    companion_json: Mapped[dict | None] = mapped_column(JSON)
    selected_god_key: Mapped[str | None] = mapped_column(String(120), index=True)

    match: Mapped[TftMatch] = relationship(back_populates="participants")
    units: Mapped[list["TftUnit"]] = relationship(back_populates="participant", cascade="all, delete-orphan")
    traits: Mapped[list["TftTrait"]] = relationship(back_populates="participant", cascade="all, delete-orphan")
    augments: Mapped[list["TftAugment"]] = relationship(back_populates="participant", cascade="all, delete-orphan")


class TftUnit(Base):
    __tablename__ = "tft_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_participant_id: Mapped[int] = mapped_column(
        ForeignKey("tft_match_participants.id", ondelete="CASCADE"), index=True, nullable=False
    )
    character_id: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(120))
    rarity: Mapped[int | None] = mapped_column(Integer)
    tier: Mapped[int | None] = mapped_column(Integer)
    item_names_json: Mapped[list | None] = mapped_column(JSON)

    participant: Mapped[TftMatchParticipant] = relationship(back_populates="units")


class TftTrait(Base):
    __tablename__ = "tft_traits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_participant_id: Mapped[int] = mapped_column(
        ForeignKey("tft_match_participants.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    num_units: Mapped[int | None] = mapped_column(Integer)
    style: Mapped[int | None] = mapped_column(Integer)
    tier_current: Mapped[int | None] = mapped_column(Integer)
    tier_total: Mapped[int | None] = mapped_column(Integer)

    participant: Mapped[TftMatchParticipant] = relationship(back_populates="traits")


class TftAugment(Base):
    __tablename__ = "tft_augments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_participant_id: Mapped[int] = mapped_column(
        ForeignKey("tft_match_participants.id", ondelete="CASCADE"), index=True, nullable=False
    )
    augment_key: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    augment_name: Mapped[str | None] = mapped_column(String(160))

    participant: Mapped[TftMatchParticipant] = relationship(back_populates="augments")


class TftItem(Base):
    __tablename__ = "tft_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_key: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    item_name: Mapped[str] = mapped_column(String(160), nullable=False)
    item_type: Mapped[str] = mapped_column(String(40), nullable=False)
    set_name: Mapped[str | None] = mapped_column(String(40))
    is_artifact: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class TftComp(Base):
    __tablename__ = "tft_comps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comp_name: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    set_name: Mapped[str] = mapped_column(String(40), nullable=False)
    patch_version: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    core_units_json: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    core_traits_json: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    core_items_json: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    preferred_gods_json: Mapped[list | None] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    stats: Mapped[list["TftCompStatsDaily"]] = relationship(back_populates="comp", cascade="all, delete-orphan")


class TftCompStatsDaily(Base):
    __tablename__ = "tft_comp_stats_daily"
    __table_args__ = (UniqueConstraint("stat_date", "region", "comp_id", name="uq_comp_stats_day_region_comp"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stat_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    set_name: Mapped[str] = mapped_column(String(40), nullable=False)
    patch_version: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    region: Mapped[str] = mapped_column(String(20), default="KR", nullable=False)
    tier: Mapped[str | None] = mapped_column(String(40))
    comp_id: Mapped[int] = mapped_column(ForeignKey("tft_comps.id", ondelete="CASCADE"), index=True, nullable=False)
    games: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_placement: Mapped[float] = mapped_column(Float, nullable=False)
    top4_rate: Mapped[float] = mapped_column(Float, nullable=False)
    first_rate: Mapped[float] = mapped_column(Float, nullable=False)
    pick_rate: Mapped[float] = mapped_column(Float, nullable=False)
    tier_label: Mapped[str] = mapped_column(String(10), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)

    comp: Mapped[TftComp] = relationship(back_populates="stats")


class TftUnitStatsDaily(Base):
    __tablename__ = "tft_unit_stats_daily"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stat_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    set_name: Mapped[str] = mapped_column(String(40), nullable=False)
    patch_version: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    unit_key: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    unit_name: Mapped[str | None] = mapped_column(String(120))
    games: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_placement: Mapped[float] = mapped_column(Float, nullable=False)
    top4_rate: Mapped[float] = mapped_column(Float, nullable=False)
    first_rate: Mapped[float] = mapped_column(Float, nullable=False)
    pick_rate: Mapped[float] = mapped_column(Float, nullable=False)


class TftRecommendationLog(Base):
    __tablename__ = "tft_recommendation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    input_units_json: Mapped[list | None] = mapped_column(JSON)
    input_items_json: Mapped[list | None] = mapped_column(JSON)
    input_augments_json: Mapped[list | None] = mapped_column(JSON)
    input_gods_json: Mapped[list | None] = mapped_column(JSON)
    recommendation_result_json: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

