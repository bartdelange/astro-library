"""Create initial schema.

Revision ID: 20260708_0001
Revises:
Create Date: 2026-07-08 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260708_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "app_meta",
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_table(
        "objects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("primary_name", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("object_type", sa.String(), nullable=True),
        sa.Column("constellation", sa.String(), nullable=True),
        sa.Column("distance_ly", sa.Float(), nullable=True),
        sa.Column("distance_display", sa.String(), nullable=True),
        sa.Column("angular_size_arcmin", sa.Float(), nullable=True),
        sa.Column("angular_size_display", sa.String(), nullable=True),
        sa.Column("magnitude", sa.Float(), nullable=True),
        sa.Column("ra", sa.Float(), nullable=True),
        sa.Column("dec", sa.Float(), nullable=True),
        sa.Column("coordinate_system", sa.String(), nullable=True),
        sa.Column("aliases", sa.JSON(), nullable=False),
        sa.Column("catalog_ids", sa.JSON(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("enrichment_sources", sa.JSON(), nullable=False),
        sa.Column("last_enriched_at", sa.DateTime(), nullable=True),
        sa.Column("hero_file_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hero_file_id"],
            ["files.id"],
            name="fk_objects_hero_file_id_files",
            use_alter=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_objects_constellation"), "objects", ["constellation"], unique=False)
    op.create_index(op.f("ix_objects_hero_file_id"), "objects", ["hero_file_id"], unique=False)
    op.create_index(op.f("ix_objects_object_type"), "objects", ["object_type"], unique=False)
    op.create_index(op.f("ix_objects_primary_name"), "objects", ["primary_name"], unique=False)
    op.create_index(op.f("ix_objects_slug"), "objects", ["slug"], unique=True)
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("object_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("hero_file_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hero_file_id"],
            ["files.id"],
            name="fk_projects_hero_file_id_files",
            use_alter=True,
        ),
        sa.ForeignKeyConstraint(["object_id"], ["objects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    op.create_index(op.f("ix_projects_hero_file_id"), "projects", ["hero_file_id"], unique=False)
    op.create_index(op.f("ix_projects_object_id"), "projects", ["object_id"], unique=False)
    op.create_index(op.f("ix_projects_slug"), "projects", ["slug"], unique=False)
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("integration_seconds", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
    )
    op.create_index(op.f("ix_sessions_date"), "sessions", ["date"], unique=False)
    op.create_index(op.f("ix_sessions_project_id"), "sessions", ["project_id"], unique=False)
    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=True),
        sa.Column("relative_path", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("extension", sa.String(), nullable=True),
        sa.Column(
            "file_role",
            sa.Enum(
                "LIGHT",
                "DARK",
                "FLAT",
                "BIAS",
                "DARK_FLAT",
                "EXPORT",
                "EDIT",
                "INTERMEDIATE",
                "PROJECT_METADATA",
                "SESSION_METADATA",
                "NOTE",
                "LOG",
                "UNKNOWN",
                name="filerole",
            ),
            nullable=False,
        ),
        sa.Column("size_bytes", sa.Integer(), nullable=True),
        sa.Column("modified_at", sa.DateTime(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_files_extension"), "files", ["extension"], unique=False)
    op.create_index(op.f("ix_files_file_role"), "files", ["file_role"], unique=False)
    op.create_index(op.f("ix_files_filename"), "files", ["filename"], unique=False)
    op.create_index(op.f("ix_files_modified_at"), "files", ["modified_at"], unique=False)
    op.create_index(op.f("ix_files_project_id"), "files", ["project_id"], unique=False)
    op.create_index(op.f("ix_files_relative_path"), "files", ["relative_path"], unique=False)
    op.create_index(op.f("ix_files_session_id"), "files", ["session_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_files_session_id"), table_name="files")
    op.drop_index(op.f("ix_files_relative_path"), table_name="files")
    op.drop_index(op.f("ix_files_project_id"), table_name="files")
    op.drop_index(op.f("ix_files_modified_at"), table_name="files")
    op.drop_index(op.f("ix_files_filename"), table_name="files")
    op.drop_index(op.f("ix_files_file_role"), table_name="files")
    op.drop_index(op.f("ix_files_extension"), table_name="files")
    op.drop_table("files")
    op.drop_index(op.f("ix_sessions_project_id"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_date"), table_name="sessions")
    op.drop_table("sessions")
    op.drop_index(op.f("ix_projects_slug"), table_name="projects")
    op.drop_index(op.f("ix_projects_object_id"), table_name="projects")
    op.drop_index(op.f("ix_projects_hero_file_id"), table_name="projects")
    op.drop_table("projects")
    op.drop_index(op.f("ix_objects_slug"), table_name="objects")
    op.drop_index(op.f("ix_objects_primary_name"), table_name="objects")
    op.drop_index(op.f("ix_objects_object_type"), table_name="objects")
    op.drop_index(op.f("ix_objects_hero_file_id"), table_name="objects")
    op.drop_index(op.f("ix_objects_constellation"), table_name="objects")
    op.drop_table("objects")
    op.drop_table("app_meta")
