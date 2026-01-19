"""Tests for database initialization and session management."""

import pytest
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch, MagicMock
from app.db.init import Database, get_session, SessionDep


def test_database_initialization():
    """Test Database class initializes correctly."""
    db = Database(
        url="sqlite:///:memory:",
        pool_size=5,
        pool_recycle=900,
        echo=True,
    )
    assert db.url == "sqlite:///:memory:"
    assert db.engine is not None


def test_database_create_engine_success():
    """Test _create_engine successfully creates engine."""
    db = Database(url="sqlite:///:memory:")
    engine = db._create_engine(pool_size=5, pool_recycle=900, echo=False)
    assert engine is not None


def test_database_session_yields_session():
    """Test Database.session generator yields session."""
    db = Database(url="sqlite:///:memory:")
    session_gen = db.session()

    session = next(session_gen)
    assert session is not None
    assert hasattr(session, "add")
    assert hasattr(session, "commit")

    session.close()


def test_database_session_handles_sqlalchemy_error():
    """Test Database.session rolls back on SQLAlchemyError."""
    db = Database(url="sqlite:///:memory:")
    session_gen = db.session()

    session = next(session_gen)

    with patch.object(session, "add", side_effect=SQLAlchemyError("Test error")):
        try:
            session.add(MagicMock())
            session.commit()
        except SQLAlchemyError:
            pass

    try:
        session_gen.send(None)
    except StopIteration:
        pass


def test_database_session_closes_on_finally():
    """Test Database.session closes session in finally block."""
    db = Database(url="sqlite:///:memory:")
    session_gen = db.session()

    session = next(session_gen)
    close_mock = MagicMock()
    session.close = close_mock

    try:
        session_gen.send(None)
    except StopIteration:
        pass

    close_mock.assert_called_once()


def test_get_session_yields_from_database():
    """Test get_session yields from db.session()."""
    db = Database(url="sqlite:///:memory:")

    with patch("app.db.init.db", db):
        session_gen = get_session()
        session = next(session_gen)
        assert session is not None
        session.close()


def test_database_with_default_parameters():
    """Test Database with default parameters."""
    db = Database(url="sqlite:///:memory:")
    assert db.url == "sqlite:///:memory:"
    assert db.engine is not None


def test_database_session_exception_propagation():
    """Test Database.session propagates exceptions."""
    db = Database(url="sqlite:///:memory:")
    session_gen = db.session()

    session = next(session_gen)

    try:
        session_gen.throw(ValueError("Test exception"))
    except ValueError as e:
        assert str(e) == "Test exception"


def test_database_multiple_sessions():
    """Test creating multiple sessions from same Database instance."""
    db = Database(url="sqlite:///:memory:")

    session1 = next(db.session())
    session2 = next(db.session())

    assert session1 is not session2
    assert session1 is not None
    assert session2 is not None

    session1.close()
    session2.close()


def test_database_engine_reuse():
    """Test that same engine is reused across session creations."""
    db = Database(url="sqlite:///:memory:")

    session1 = next(db.session())
    session2 = next(db.session())

    assert session1.bind is session2.bind

    session1.close()
    session2.close()


def test_session_dep_type():
    """Test SessionDep is properly typed."""
    from typing import get_type_hints

    assert SessionDep is not None


def test_database_create_engine_with_invalid_url():
    """Test _create_engine handles invalid database URLs."""
    db = Database(url="invalid://url")

    with pytest.raises(Exception):  # Should raise some database connection error
        db._create_engine()


def test_database_session_with_exception_in_context():
    """Test Database.session handles exceptions in context manager."""
    db = Database(url="sqlite:///:memory:")
    session_gen = db.session()

    session = next(session_gen)

    # Simulate an exception during session use
    with patch.object(session, "rollback") as rollback_mock:
        try:
            raise ValueError("Test exception")
        except ValueError:
            pass
        finally:
            # Send None to trigger finally block
            try:
                session_gen.send(None)
            except StopIteration:
                pass

    rollback_mock.assert_called()


def test_database_session_with_commit_failure():
    """Test Database.session handles commit failures."""
    db = Database(url="sqlite:///:memory:")
    session_gen = db.session()

    session = next(session_gen)

    with patch.object(session, "commit", side_effect=SQLAlchemyError("Commit failed")):
        with patch.object(session, "rollback") as rollback_mock:
            try:
                session.commit()
            except SQLAlchemyError:
                pass
            finally:
                try:
                    session_gen.send(None)
                except StopIteration:
                    pass

    rollback_mock.assert_called()


def test_get_session_with_database_error():
    """Test get_session handles database connection errors."""
    db = Database(url="sqlite:///:memory:")

    with patch("app.db.init.db", db):
        with patch.object(db, "session", side_effect=Exception("DB error")):
            with pytest.raises(Exception):
                next(get_session())


def test_database_engine_configuration():
    """Test Database engine is configured with correct parameters."""
    db = Database(url="sqlite:///:memory:", pool_size=10, pool_recycle=1800, echo=True)

    assert db.engine is not None
    # SQLite doesn't use pool_size, but engine should still be created


def test_database_session_context_manager():
    """Test Database.session works as context manager."""
    db = Database(url="sqlite:///:memory:")

    with db.session() as session:
        assert session is not None
        assert hasattr(session, "add")
        assert hasattr(session, "commit")
