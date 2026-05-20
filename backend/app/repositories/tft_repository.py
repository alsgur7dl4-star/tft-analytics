from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.tft import (
    RiotAccount,
    TftAugment,
    TftMatch,
    TftMatchParticipant,
    TftSummoner,
    TftTrait,
    TftUnit,
)


class TftRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_riot_account(self, game_name: str, tag_line: str, puuid: str, region: str) -> RiotAccount:
        account = self.db.scalar(select(RiotAccount).where(RiotAccount.puuid == puuid))
        if account:
            account.game_name = game_name
            account.tag_line = tag_line
            account.region = region.upper()
            self.db.add(account)
            self.db.flush()
            return account
        account = RiotAccount(game_name=game_name, tag_line=tag_line, puuid=puuid, region=region.upper())
        self.db.add(account)
        self.db.flush()
        return account

    def get_account_by_puuid(self, puuid: str) -> RiotAccount | None:
        return self.db.scalar(select(RiotAccount).where(RiotAccount.puuid == puuid))

    def upsert_summoner(
        self,
        riot_account_id: int,
        summoner_id: str,
        region: str,
        profile_icon_id: int | None,
        summoner_level: int | None,
    ) -> TftSummoner:
        summoner = self.db.scalar(select(TftSummoner).where(TftSummoner.summoner_id == summoner_id))
        if summoner:
            summoner.profile_icon_id = profile_icon_id
            summoner.summoner_level = summoner_level
            summoner.updated_at = datetime.now(timezone.utc)
            self.db.add(summoner)
            self.db.flush()
            return summoner
        summoner = TftSummoner(
            riot_account_id=riot_account_id,
            summoner_id=summoner_id,
            region=region.upper(),
            profile_icon_id=profile_icon_id,
            summoner_level=summoner_level,
        )
        self.db.add(summoner)
        self.db.flush()
        return summoner

    def get_match_by_match_id(self, match_id: str) -> TftMatch | None:
        return self.db.scalar(
            select(TftMatch)
            .where(TftMatch.match_id == match_id)
            .options(selectinload(TftMatch.participants))
        )

    def list_matches_for_puuid(self, puuid: str, limit: int = 20) -> list[TftMatch]:
        return list(
            self.db.scalars(
                select(TftMatch)
                .join(TftMatchParticipant)
                .where(TftMatchParticipant.puuid == puuid)
                .order_by(TftMatch.game_datetime.desc().nullslast(), TftMatch.id.desc())
                .limit(limit)
                .options(selectinload(TftMatch.participants))
            )
        )

    def create_match_from_raw(self, match_id: str, raw: dict[str, Any], region: str) -> TftMatch:
        info = raw.get("info", {})
        metadata = raw.get("metadata", {})
        game_datetime = info.get("game_datetime")
        match = TftMatch(
            match_id=metadata.get("match_id", match_id),
            region=region.upper(),
            set_name=str(info.get("tft_set_number")) if info.get("tft_set_number") else None,
            game_version=info.get("game_version"),
            queue_id=info.get("queue_id"),
            game_datetime=datetime.fromtimestamp(game_datetime / 1000, tz=timezone.utc) if game_datetime else None,
            game_length=info.get("game_length"),
            raw_json=raw,
        )
        self.db.add(match)
        self.db.flush()
        for participant_raw in info.get("participants", []):
            selected_god_key = (
                participant_raw.get("selected_god")
                or participant_raw.get("god_key")
                or participant_raw.get("tft_god_key")
            )
            participant = TftMatchParticipant(
                match_id=match.id,
                puuid=participant_raw.get("puuid", ""),
                placement=participant_raw.get("placement", 0),
                level=participant_raw.get("level"),
                gold_left=participant_raw.get("gold_left"),
                last_round=participant_raw.get("last_round"),
                players_eliminated=participant_raw.get("players_eliminated"),
                total_damage_to_players=participant_raw.get("total_damage_to_players"),
                traits_json=participant_raw.get("traits", []),
                units_json=participant_raw.get("units", []),
                augments_json=participant_raw.get("augments", []),
                companion_json=participant_raw.get("companion"),
                selected_god_key=selected_god_key,
            )
            self.db.add(participant)
            self.db.flush()
            for unit_raw in participant_raw.get("units", []):
                self.db.add(
                    TftUnit(
                        match_participant_id=participant.id,
                        character_id=unit_raw.get("character_id", ""),
                        name=unit_raw.get("name"),
                        rarity=unit_raw.get("rarity"),
                        tier=unit_raw.get("tier"),
                        item_names_json=unit_raw.get("itemNames", []),
                    )
                )
            for trait_raw in participant_raw.get("traits", []):
                self.db.add(
                    TftTrait(
                        match_participant_id=participant.id,
                        name=trait_raw.get("name", ""),
                        num_units=trait_raw.get("num_units"),
                        style=trait_raw.get("style"),
                        tier_current=trait_raw.get("tier_current"),
                        tier_total=trait_raw.get("tier_total"),
                    )
                )
            for augment_key in participant_raw.get("augments", []):
                self.db.add(TftAugment(match_participant_id=participant.id, augment_key=augment_key, augment_name=None))
        self.db.flush()
        return match

