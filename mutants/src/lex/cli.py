"""Command Line Interface (CLI) for LEX Ingestion Engine.

Provides database initialization, schema migration, and crawler orchestration.
Defaults to crawling in reverse chronological order (from today back to 2002-01-02).
"""

import argparse
import sys
from datetime import date
from typing import Any

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, text

from lex.ingestion.infrastructure.persistence.models import Base
from lex.shared_kernel.config import LexSettings

# -----------------------------------------------------------------------------
# Module Constants (ADR-003)
# -----------------------------------------------------------------------------
# Earliest publication available in the modern digital DOU portal (in.gov.br)
EARLIEST_MODERN_DOU_DATE: str = "2002-01-02"
DEFAULT_SPIDER_NAME: str = "federal_dou"


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_init_db__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_init_db__mutmut)
def init_db() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_orig() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_1() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = None
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_2() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(None)
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_3() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = None

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_4() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(None, echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_5() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=None)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_6() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_7() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), )

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_8() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(None), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_9() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=True)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_10() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print(None)
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_11() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("XXCreating tables (gazette_editions, normative_acts)...XX")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_12() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_13() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("CREATING TABLES (GAZETTE_EDITIONS, NORMATIVE_ACTS)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_14() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(None)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_15() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name != "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_16() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "XXpostgresqlXX":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_17() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "POSTGRESQL":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_18() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print(None)
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_19() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("XXConfiguring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...XX")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_20() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("configuring postgresql 16 lz4 toast compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_21() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("CONFIGURING POSTGRESQL 16 LZ4 TOAST COMPRESSION ON NORMATIVE_ACTS.RAW_CONTENT...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_22() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    None
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_23() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text(None)
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_24() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("XXALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;XX")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_25() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("alter table normative_acts alter column raw_content set compression lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_26() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE NORMATIVE_ACTS ALTER COLUMN RAW_CONTENT SET COMPRESSION LZ4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_27() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print(None)
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_28() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("XXLZ4 TOAST compression successfully activated.XX")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_29() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("lz4 toast compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_30() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST COMPRESSION SUCCESSFULLY ACTIVATED.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("Database schema successfully initialized.")


def x_init_db__mutmut_31() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(None)

    print("Database schema successfully initialized.")


def x_init_db__mutmut_32() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print(None)


def x_init_db__mutmut_33() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("XXDatabase schema successfully initialized.XX")


def x_init_db__mutmut_34() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("database schema successfully initialized.")


def x_init_db__mutmut_35() -> None:
    """Initialize PostgreSQL schema and configure LZ4 TOAST compression on normative_acts."""
    settings = LexSettings()
    print(f"Connecting to database: {settings.database_url}...")
    engine = create_engine(str(settings.database_url), echo=False)

    print("Creating tables (gazette_editions, normative_acts)...")
    Base.metadata.create_all(engine)

    # Configure PostgreSQL LZ4 TOAST compression on normative_acts.raw_content
    if engine.dialect.name == "postgresql":
        print("Configuring PostgreSQL 16 LZ4 TOAST compression on normative_acts.raw_content...")
        with engine.connect() as conn:
            try:
                conn.execute(
                    text("ALTER TABLE normative_acts ALTER COLUMN raw_content SET COMPRESSION lz4;")
                )
                conn.commit()
                print("LZ4 TOAST compression successfully activated.")
            except Exception as exc:
                print(f"Note: Could not set LZ4 compression (standard TOAST will be used): {exc}")

    print("DATABASE SCHEMA SUCCESSFULLY INITIALIZED.")

mutants_x_init_db__mutmut['_mutmut_orig'] = x_init_db__mutmut_orig # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_1'] = x_init_db__mutmut_1 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_2'] = x_init_db__mutmut_2 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_3'] = x_init_db__mutmut_3 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_4'] = x_init_db__mutmut_4 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_5'] = x_init_db__mutmut_5 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_6'] = x_init_db__mutmut_6 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_7'] = x_init_db__mutmut_7 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_8'] = x_init_db__mutmut_8 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_9'] = x_init_db__mutmut_9 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_10'] = x_init_db__mutmut_10 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_11'] = x_init_db__mutmut_11 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_12'] = x_init_db__mutmut_12 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_13'] = x_init_db__mutmut_13 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_14'] = x_init_db__mutmut_14 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_15'] = x_init_db__mutmut_15 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_16'] = x_init_db__mutmut_16 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_17'] = x_init_db__mutmut_17 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_18'] = x_init_db__mutmut_18 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_19'] = x_init_db__mutmut_19 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_20'] = x_init_db__mutmut_20 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_21'] = x_init_db__mutmut_21 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_22'] = x_init_db__mutmut_22 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_23'] = x_init_db__mutmut_23 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_24'] = x_init_db__mutmut_24 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_25'] = x_init_db__mutmut_25 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_26'] = x_init_db__mutmut_26 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_27'] = x_init_db__mutmut_27 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_28'] = x_init_db__mutmut_28 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_29'] = x_init_db__mutmut_29 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_30'] = x_init_db__mutmut_30 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_31'] = x_init_db__mutmut_31 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_32'] = x_init_db__mutmut_32 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_33'] = x_init_db__mutmut_33 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_34'] = x_init_db__mutmut_34 # type: ignore # mutmut generated
mutants_x_init_db__mutmut['x_init_db__mutmut_35'] = x_init_db__mutmut_35 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_run_crawler__mutmut)
def run_crawler(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_orig(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_1(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = True,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_2(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = False,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_3(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = None
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_4(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = None

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_5(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(None)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_6(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = None

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_7(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = None
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_8(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = None
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_9(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = None
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_10(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date and EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_11(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = None

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_12(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date and today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_13(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = None

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_14(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "XXstart_dateXX": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_15(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "START_DATE": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_16(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "XXend_dateXX": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_17(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "END_DATE": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_18(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "XXforceXX": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_19(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "FORCE": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_20(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "XXreverseXX": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_21(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "REVERSE": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_22(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = None
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_23(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "XXnewest → oldestXX" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_24(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "NEWEST → OLDEST" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_25(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "XXoldest → newestXX"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_26(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "OLDEST → NEWEST"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_27(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = None
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_28(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = "XX [FORCE OVERRIDE]XX" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_29(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [force override]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_30(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else "XXXX"
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_31(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = None
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_32(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(None)
    process.crawl(spider_name, **spider_args)
    process.start()


def x_run_crawler__mutmut_33(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(None, **spider_args)
    process.start()


def x_run_crawler__mutmut_34(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(**spider_args)
    process.start()


def x_run_crawler__mutmut_35(
    spider_name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    single_date: str | None = None,
    force: bool = False,
    reverse: bool = True,
) -> None:
    """Execute Scrapy crawler process for target spider and date interval in descending order."""
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    today_str = date.today().isoformat()

    if single_date:
        effective_start = single_date
        effective_end = single_date
    else:
        effective_start = start_date or EARLIEST_MODERN_DOU_DATE
        effective_end = end_date or today_str

    spider_args: dict[str, Any] = {
        "start_date": effective_start,
        "end_date": effective_end,
        "force": force,
        "reverse": reverse,
    }

    order_desc = "newest → oldest" if reverse else "oldest → newest"
    force_msg = " [FORCE OVERRIDE]" if force else ""
    interval_info = f"range: {effective_start} to {effective_end} | order: {order_desc}"
    print(f"Starting spider '{spider_name}' ({interval_info}){force_msg}...")
    process.crawl(spider_name, )
    process.start()

mutants_x_run_crawler__mutmut['_mutmut_orig'] = x_run_crawler__mutmut_orig # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_1'] = x_run_crawler__mutmut_1 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_2'] = x_run_crawler__mutmut_2 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_3'] = x_run_crawler__mutmut_3 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_4'] = x_run_crawler__mutmut_4 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_5'] = x_run_crawler__mutmut_5 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_6'] = x_run_crawler__mutmut_6 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_7'] = x_run_crawler__mutmut_7 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_8'] = x_run_crawler__mutmut_8 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_9'] = x_run_crawler__mutmut_9 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_10'] = x_run_crawler__mutmut_10 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_11'] = x_run_crawler__mutmut_11 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_12'] = x_run_crawler__mutmut_12 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_13'] = x_run_crawler__mutmut_13 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_14'] = x_run_crawler__mutmut_14 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_15'] = x_run_crawler__mutmut_15 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_16'] = x_run_crawler__mutmut_16 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_17'] = x_run_crawler__mutmut_17 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_18'] = x_run_crawler__mutmut_18 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_19'] = x_run_crawler__mutmut_19 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_20'] = x_run_crawler__mutmut_20 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_21'] = x_run_crawler__mutmut_21 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_22'] = x_run_crawler__mutmut_22 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_23'] = x_run_crawler__mutmut_23 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_24'] = x_run_crawler__mutmut_24 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_25'] = x_run_crawler__mutmut_25 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_26'] = x_run_crawler__mutmut_26 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_27'] = x_run_crawler__mutmut_27 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_28'] = x_run_crawler__mutmut_28 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_29'] = x_run_crawler__mutmut_29 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_30'] = x_run_crawler__mutmut_30 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_31'] = x_run_crawler__mutmut_31 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_32'] = x_run_crawler__mutmut_32 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_33'] = x_run_crawler__mutmut_33 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_34'] = x_run_crawler__mutmut_34 # type: ignore # mutmut generated
mutants_x_run_crawler__mutmut['x_run_crawler__mutmut_35'] = x_run_crawler__mutmut_35 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build_parser__mutmut)
def build_parser() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_orig() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_1() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = None
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_2() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog=None,
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_3() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description=None,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_4() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_5() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_6() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="XXlexXX",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_7() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="LEX",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_8() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="XXLEX Brazilian Legislation Ingestion & Digestion Engine CLIXX",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_9() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="lex brazilian legislation ingestion & digestion engine cli",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_10() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX BRAZILIAN LEGISLATION INGESTION & DIGESTION ENGINE CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_11() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = None

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_12() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest=None, help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_13() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help=None)

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_14() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_15() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", )

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_16() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="XXcommandXX", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_17() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="COMMAND", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_18() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="XXAvailable sub-commandsXX")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_19() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_20() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="AVAILABLE SUB-COMMANDS")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_21() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        None,
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_22() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help=None,
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_23() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_24() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_25() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "XXinit-dbXX",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_26() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "INIT-DB",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_27() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="XXInitialize database schema and LZ4 TOAST compressionXX",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_28() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="initialize database schema and lz4 toast compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_29() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="INITIALIZE DATABASE SCHEMA AND LZ4 TOAST COMPRESSION",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_30() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = None
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_31() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser(None, help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_32() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help=None)
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_33() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser(help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_34() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", )
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_35() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("XXcrawlXX", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_36() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("CRAWL", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_37() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="XXRun a gazette spider (Default)XX")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_38() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="run a gazette spider (default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_39() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="RUN A GAZETTE SPIDER (DEFAULT)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_40() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        None,
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_41() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs=None,
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_42() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=None,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_43() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help=None,
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_44() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_45() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_46() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_47() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_48() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "XXspiderXX",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_49() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "SPIDER",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_50() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="XX?XX",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_51() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="XXSpider name (default: federal_dou). Options: federal_dou, state_sp, etc.XX",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_52() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="spider name (default: federal_dou). options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_53() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="SPIDER NAME (DEFAULT: FEDERAL_DOU). OPTIONS: FEDERAL_DOU, STATE_SP, ETC.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_54() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        None,
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_55() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        None,
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_56() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help=None,
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_57() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_58() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_59() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_60() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_61() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "XX--dateXX",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_62() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--DATE",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_63() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "XX-dXX",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_64() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-D",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_65() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="XXSingle target date (YYYY-MM-DD)XX",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_66() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="single target date (yyyy-mm-dd)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_67() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="SINGLE TARGET DATE (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_68() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        None,
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_69() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=None,
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_70() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_71() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_72() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_73() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "XX--start-dateXX",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_74() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--START-DATE",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_75() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        None,
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_76() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help=None,
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_77() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_78() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_79() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_80() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "XX--end-dateXX",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_81() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--END-DATE",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_82() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="XXEnd date (YYYY-MM-DD, default: today)XX",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_83() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="end date (yyyy-mm-dd, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_84() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="END DATE (YYYY-MM-DD, DEFAULT: TODAY)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_85() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        None,
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_86() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action=None,
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_87() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=None,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_88() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help=None,
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_89() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_90() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_91() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_92() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_93() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "XX--ascendingXX",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_94() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ASCENDING",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_95() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="XXstore_trueXX",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_96() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="STORE_TRUE",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_97() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=True,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_98() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="XXCrawl in ascending chronological order (oldest to newest).XX",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_99() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_100() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="CRAWL IN ASCENDING CHRONOLOGICAL ORDER (OLDEST TO NEWEST).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_101() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        None,
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_102() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action=None,
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_103() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=None,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_104() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help=None,
    )

    return parser


def x_build_parser__mutmut_105() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_106() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_107() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_108() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        )

    return parser


def x_build_parser__mutmut_109() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "XX--forceXX",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_110() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--FORCE",
        action="store_true",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_111() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="XXstore_trueXX",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_112() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="STORE_TRUE",
        default=False,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_113() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=True,
        help="Force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_114() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="XXForce re-scraping and downloading even if already completed.XX",
    )

    return parser


def x_build_parser__mutmut_115() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="force re-scraping and downloading even if already completed.",
    )

    return parser


def x_build_parser__mutmut_116() -> argparse.ArgumentParser:
    """Construct and configure CLI argument parser with subparsers."""
    parser = argparse.ArgumentParser(
        prog="lex",
        description="LEX Brazilian Legislation Ingestion & Digestion Engine CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # init-db sub-command
    subparsers.add_parser(
        "init-db",
        help="Initialize database schema and LZ4 TOAST compression",
    )

    # crawl sub-command
    crawl_parser = subparsers.add_parser("crawl", help="Run a gazette spider (Default)")
    crawl_parser.add_argument(
        "spider",
        nargs="?",
        default=DEFAULT_SPIDER_NAME,
        help="Spider name (default: federal_dou). Options: federal_dou, state_sp, etc.",
    )
    crawl_parser.add_argument(
        "--date",
        "-d",
        help="Single target date (YYYY-MM-DD)",
        default=None,
    )
    crawl_parser.add_argument(
        "--start-date",
        help=f"Start date (YYYY-MM-DD, default: {EARLIEST_MODERN_DOU_DATE})",
        default=None,
    )
    crawl_parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, default: today)",
        default=None,
    )
    crawl_parser.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Crawl in ascending chronological order (oldest to newest).",
    )
    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="FORCE RE-SCRAPING AND DOWNLOADING EVEN IF ALREADY COMPLETED.",
    )

    return parser

mutants_x_build_parser__mutmut['_mutmut_orig'] = x_build_parser__mutmut_orig # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_1'] = x_build_parser__mutmut_1 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_2'] = x_build_parser__mutmut_2 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_3'] = x_build_parser__mutmut_3 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_4'] = x_build_parser__mutmut_4 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_5'] = x_build_parser__mutmut_5 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_6'] = x_build_parser__mutmut_6 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_7'] = x_build_parser__mutmut_7 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_8'] = x_build_parser__mutmut_8 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_9'] = x_build_parser__mutmut_9 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_10'] = x_build_parser__mutmut_10 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_11'] = x_build_parser__mutmut_11 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_12'] = x_build_parser__mutmut_12 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_13'] = x_build_parser__mutmut_13 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_14'] = x_build_parser__mutmut_14 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_15'] = x_build_parser__mutmut_15 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_16'] = x_build_parser__mutmut_16 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_17'] = x_build_parser__mutmut_17 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_18'] = x_build_parser__mutmut_18 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_19'] = x_build_parser__mutmut_19 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_20'] = x_build_parser__mutmut_20 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_21'] = x_build_parser__mutmut_21 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_22'] = x_build_parser__mutmut_22 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_23'] = x_build_parser__mutmut_23 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_24'] = x_build_parser__mutmut_24 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_25'] = x_build_parser__mutmut_25 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_26'] = x_build_parser__mutmut_26 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_27'] = x_build_parser__mutmut_27 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_28'] = x_build_parser__mutmut_28 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_29'] = x_build_parser__mutmut_29 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_30'] = x_build_parser__mutmut_30 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_31'] = x_build_parser__mutmut_31 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_32'] = x_build_parser__mutmut_32 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_33'] = x_build_parser__mutmut_33 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_34'] = x_build_parser__mutmut_34 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_35'] = x_build_parser__mutmut_35 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_36'] = x_build_parser__mutmut_36 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_37'] = x_build_parser__mutmut_37 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_38'] = x_build_parser__mutmut_38 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_39'] = x_build_parser__mutmut_39 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_40'] = x_build_parser__mutmut_40 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_41'] = x_build_parser__mutmut_41 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_42'] = x_build_parser__mutmut_42 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_43'] = x_build_parser__mutmut_43 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_44'] = x_build_parser__mutmut_44 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_45'] = x_build_parser__mutmut_45 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_46'] = x_build_parser__mutmut_46 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_47'] = x_build_parser__mutmut_47 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_48'] = x_build_parser__mutmut_48 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_49'] = x_build_parser__mutmut_49 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_50'] = x_build_parser__mutmut_50 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_51'] = x_build_parser__mutmut_51 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_52'] = x_build_parser__mutmut_52 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_53'] = x_build_parser__mutmut_53 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_54'] = x_build_parser__mutmut_54 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_55'] = x_build_parser__mutmut_55 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_56'] = x_build_parser__mutmut_56 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_57'] = x_build_parser__mutmut_57 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_58'] = x_build_parser__mutmut_58 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_59'] = x_build_parser__mutmut_59 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_60'] = x_build_parser__mutmut_60 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_61'] = x_build_parser__mutmut_61 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_62'] = x_build_parser__mutmut_62 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_63'] = x_build_parser__mutmut_63 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_64'] = x_build_parser__mutmut_64 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_65'] = x_build_parser__mutmut_65 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_66'] = x_build_parser__mutmut_66 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_67'] = x_build_parser__mutmut_67 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_68'] = x_build_parser__mutmut_68 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_69'] = x_build_parser__mutmut_69 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_70'] = x_build_parser__mutmut_70 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_71'] = x_build_parser__mutmut_71 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_72'] = x_build_parser__mutmut_72 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_73'] = x_build_parser__mutmut_73 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_74'] = x_build_parser__mutmut_74 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_75'] = x_build_parser__mutmut_75 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_76'] = x_build_parser__mutmut_76 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_77'] = x_build_parser__mutmut_77 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_78'] = x_build_parser__mutmut_78 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_79'] = x_build_parser__mutmut_79 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_80'] = x_build_parser__mutmut_80 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_81'] = x_build_parser__mutmut_81 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_82'] = x_build_parser__mutmut_82 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_83'] = x_build_parser__mutmut_83 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_84'] = x_build_parser__mutmut_84 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_85'] = x_build_parser__mutmut_85 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_86'] = x_build_parser__mutmut_86 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_87'] = x_build_parser__mutmut_87 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_88'] = x_build_parser__mutmut_88 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_89'] = x_build_parser__mutmut_89 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_90'] = x_build_parser__mutmut_90 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_91'] = x_build_parser__mutmut_91 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_92'] = x_build_parser__mutmut_92 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_93'] = x_build_parser__mutmut_93 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_94'] = x_build_parser__mutmut_94 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_95'] = x_build_parser__mutmut_95 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_96'] = x_build_parser__mutmut_96 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_97'] = x_build_parser__mutmut_97 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_98'] = x_build_parser__mutmut_98 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_99'] = x_build_parser__mutmut_99 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_100'] = x_build_parser__mutmut_100 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_101'] = x_build_parser__mutmut_101 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_102'] = x_build_parser__mutmut_102 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_103'] = x_build_parser__mutmut_103 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_104'] = x_build_parser__mutmut_104 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_105'] = x_build_parser__mutmut_105 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_106'] = x_build_parser__mutmut_106 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_107'] = x_build_parser__mutmut_107 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_108'] = x_build_parser__mutmut_108 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_109'] = x_build_parser__mutmut_109 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_110'] = x_build_parser__mutmut_110 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_111'] = x_build_parser__mutmut_111 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_112'] = x_build_parser__mutmut_112 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_113'] = x_build_parser__mutmut_113 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_114'] = x_build_parser__mutmut_114 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_115'] = x_build_parser__mutmut_115 # type: ignore # mutmut generated
mutants_x_build_parser__mutmut['x_build_parser__mutmut_116'] = x_build_parser__mutmut_116 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_parse_cli_args__mutmut)
def parse_cli_args(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_orig(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_1(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = None

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_2(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(None) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_3(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[2:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_4(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is not None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_5(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(None)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_6(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_7(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = None
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_8(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["XXcrawlXX", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_9(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["CRAWL", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_10(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[1] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_11(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_12(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("XXinit-dbXX", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_13(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("INIT-DB", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_14(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "XXcrawlXX", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_15(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "CRAWL", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_16(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "XX-hXX", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_17(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-H", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_18(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "XX--helpXX"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_19(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--HELP"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_20(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_21(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith(None):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_22(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[1].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_23(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("XX-XX"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_24(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = None
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_25(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] - raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_26(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["XXcrawlXX"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_27(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["CRAWL"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_28(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = None

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_29(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] - raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_30(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["XXcrawlXX", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_31(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["CRAWL", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_32(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = None
    return parser.parse_args(raw_args)


def x_parse_cli_args__mutmut_33(args: list[str] | None = None) -> argparse.Namespace:
    """Pre-process CLI arguments and parse via ArgumentParser."""
    raw_args = list(sys.argv[1:]) if args is None else list(args)

    # Pre-process arguments to allow 'crawl' as default command
    if not raw_args:
        raw_args = ["crawl", DEFAULT_SPIDER_NAME]
    elif raw_args[0] not in ("init-db", "crawl", "-h", "--help"):
        if not raw_args[0].startswith("-"):
            # First argument is spider name (e.g. `lex state_sp`)
            raw_args = ["crawl"] + raw_args
        else:
            # First argument is a flag (e.g. `lex --date 2024-01-15`)
            raw_args = ["crawl", DEFAULT_SPIDER_NAME] + raw_args

    parser = build_parser()
    return parser.parse_args(None)

mutants_x_parse_cli_args__mutmut['_mutmut_orig'] = x_parse_cli_args__mutmut_orig # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_1'] = x_parse_cli_args__mutmut_1 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_2'] = x_parse_cli_args__mutmut_2 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_3'] = x_parse_cli_args__mutmut_3 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_4'] = x_parse_cli_args__mutmut_4 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_5'] = x_parse_cli_args__mutmut_5 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_6'] = x_parse_cli_args__mutmut_6 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_7'] = x_parse_cli_args__mutmut_7 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_8'] = x_parse_cli_args__mutmut_8 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_9'] = x_parse_cli_args__mutmut_9 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_10'] = x_parse_cli_args__mutmut_10 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_11'] = x_parse_cli_args__mutmut_11 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_12'] = x_parse_cli_args__mutmut_12 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_13'] = x_parse_cli_args__mutmut_13 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_14'] = x_parse_cli_args__mutmut_14 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_15'] = x_parse_cli_args__mutmut_15 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_16'] = x_parse_cli_args__mutmut_16 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_17'] = x_parse_cli_args__mutmut_17 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_18'] = x_parse_cli_args__mutmut_18 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_19'] = x_parse_cli_args__mutmut_19 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_20'] = x_parse_cli_args__mutmut_20 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_21'] = x_parse_cli_args__mutmut_21 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_22'] = x_parse_cli_args__mutmut_22 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_23'] = x_parse_cli_args__mutmut_23 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_24'] = x_parse_cli_args__mutmut_24 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_25'] = x_parse_cli_args__mutmut_25 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_26'] = x_parse_cli_args__mutmut_26 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_27'] = x_parse_cli_args__mutmut_27 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_28'] = x_parse_cli_args__mutmut_28 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_29'] = x_parse_cli_args__mutmut_29 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_30'] = x_parse_cli_args__mutmut_30 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_31'] = x_parse_cli_args__mutmut_31 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_32'] = x_parse_cli_args__mutmut_32 # type: ignore # mutmut generated
mutants_x_parse_cli_args__mutmut['x_parse_cli_args__mutmut_33'] = x_parse_cli_args__mutmut_33 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_orig(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_1(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = None

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_2(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(None)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_3(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command != "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_4(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "XXinit-dbXX":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_5(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "INIT-DB":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_6(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command != "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_7(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "XXcrawlXX":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_8(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "CRAWL":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_9(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=None,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_10(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=None,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_11(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=None,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_12(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=None,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_13(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=None,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_14(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=None,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_15(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_16(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_17(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_18(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            force=parsed_args.force,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_19(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            reverse=not parsed_args.ascending,
        )
    else:
        build_parser().print_help()


def x_main__mutmut_20(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            )
    else:
        build_parser().print_help()


def x_main__mutmut_21(args: list[str] | None = None) -> None:
    """CLI routing entrypoint with 'crawl' as default action."""
    parsed_args = parse_cli_args(args)

    if parsed_args.command == "init-db":
        init_db()
    elif parsed_args.command == "crawl":
        run_crawler(
            spider_name=parsed_args.spider,
            start_date=parsed_args.start_date,
            end_date=parsed_args.end_date,
            single_date=parsed_args.date,
            force=parsed_args.force,
            reverse=parsed_args.ascending,
        )
    else:
        build_parser().print_help()

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_5'] = x_main__mutmut_5 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_6'] = x_main__mutmut_6 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_7'] = x_main__mutmut_7 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_8'] = x_main__mutmut_8 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_9'] = x_main__mutmut_9 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_10'] = x_main__mutmut_10 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_11'] = x_main__mutmut_11 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_12'] = x_main__mutmut_12 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_13'] = x_main__mutmut_13 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_14'] = x_main__mutmut_14 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_15'] = x_main__mutmut_15 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_16'] = x_main__mutmut_16 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_17'] = x_main__mutmut_17 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_18'] = x_main__mutmut_18 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_19'] = x_main__mutmut_19 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_20'] = x_main__mutmut_20 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_21'] = x_main__mutmut_21 # type: ignore # mutmut generated


if __name__ == "__main__":
    main()
    print("Done!")
