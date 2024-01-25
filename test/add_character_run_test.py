import pytest
from unittest.mock import MagicMock, patch

import app.db as db


# Replace 'your_module' with the actual name of the module where `add_character_run` is defined.
class TestCharacterDB:
    @pytest.fixture
    def mock_session(self):
        session = MagicMock()
        with patch("db.Session", return_value=session):
            with db.async_session_scope() as session:
                yield session

    @pytest.mark.usefixtures("mock_session")
    def test_add_character_run(self, mock_session):
        # Create example character and run objects
        character = db.CharacterDB(
            name="TestCharacter",
            realm="TestRealm",
            discord_user_id=12345,
            discord_guild_id=67890,
            guild_name="TestGuild",
            faction="Horde",
            region="US",
            role="DPS",
            spec_name="Frost",
            class_name="Mage",
            achievement_points=5000,
            item_level=200,
            score=1000,
            rank=1,
            thumbnail_url="https://example.com/thumbnail",
            url="https://example.com/character",
            last_crawled_at="2022-01-01",
            is_reporting=True,
        )
        run = db.DungeonRunDB(
            id=1,
            season="season-df-1",
            name="TestRun",
            short_name="Test",
            mythic_level=15,
            completed_at="2022-01-01",
            clear_time_ms=100000,
            par_time_ms=100000,
            num_keystone_upgrades=0,
            score=1000,
            url="https://example.com/run",
        )

        # Set up the database query results
        mock_session.query(db.CharacterDB).filter().first.return_value = character
        mock_session.query(db.DungeonRunDB).filter().first.return_value = run
        mock_session.query(db.CharacterRunDB).filter().first.return_value = None

        # Call the add_character_run function
        result = db.add_character_run(character, run)

        # Check if the new character run was added
        assert result is not None
        assert result.character_id == character.id
        assert result.dungeon_run_id == run.id

        # Verify database interactions
        mock_session.query(db.CharacterDB).filter.assert_called_once()
        mock_session.query(db.DungeonRunDB).filter.assert_called_once()
        mock_session.query(db.CharacterRunDB).filter.assert_called_once()
        mock_session.add.assert_called_once_with(result)
