from __future__ import annotations

import argparse
import random
from datetime import date, datetime, timedelta
from typing import Any

import factory
import factory.random
from faker import Faker
from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session as DbSession

from app.database.session import SessionLocal, init_db
from app.models import AstroObject, EnrichmentSource, File, FileRole, Project
from app.models.session import Session as ImagingSession

fake = Faker()

TARGETS: list[dict[str, Any]] = [
    {
        "primary_name": "M31",
        "display_name": "Andromeda Galaxy",
        "object_type": "Galaxy",
        "constellation": "Andromeda",
        "distance_ly": 2537000,
        "angular_size_arcmin": 190.0,
        "magnitude": 3.44,
        "ra": 10.6847,
        "dec": 41.2692,
        "aliases": ["NGC 224", "Messier 31"],
        "catalog_ids": {"M": "31", "NGC": "224"},
    },
    {
        "primary_name": "M42",
        "display_name": "Orion Nebula",
        "object_type": "Emission Nebula",
        "constellation": "Orion",
        "distance_ly": 1344,
        "angular_size_arcmin": 65.0,
        "magnitude": 4.0,
        "ra": 83.8221,
        "dec": -5.3911,
        "aliases": ["NGC 1976", "Messier 42"],
        "catalog_ids": {"M": "42", "NGC": "1976"},
    },
    {
        "primary_name": "M45",
        "display_name": "Pleiades",
        "object_type": "Open Cluster",
        "constellation": "Taurus",
        "distance_ly": 444,
        "angular_size_arcmin": 110.0,
        "magnitude": 1.6,
        "ra": 56.75,
        "dec": 24.1167,
        "aliases": ["Seven Sisters", "Melotte 22"],
        "catalog_ids": {"M": "45"},
    },
    {
        "primary_name": "M51",
        "display_name": "Whirlpool Galaxy",
        "object_type": "Galaxy",
        "constellation": "Canes Venatici",
        "distance_ly": 23000000,
        "angular_size_arcmin": 11.2,
        "magnitude": 8.4,
        "ra": 202.4696,
        "dec": 47.1952,
        "aliases": ["NGC 5194", "Messier 51"],
        "catalog_ids": {"M": "51", "NGC": "5194"},
    },
    {
        "primary_name": "M81",
        "display_name": "Bode's Galaxy",
        "object_type": "Galaxy",
        "constellation": "Ursa Major",
        "distance_ly": 12000000,
        "angular_size_arcmin": 26.9,
        "magnitude": 6.9,
        "ra": 148.8882,
        "dec": 69.0653,
        "aliases": ["NGC 3031", "Messier 81"],
        "catalog_ids": {"M": "81", "NGC": "3031"},
    },
    {
        "primary_name": "M101",
        "display_name": "Pinwheel Galaxy",
        "object_type": "Galaxy",
        "constellation": "Ursa Major",
        "distance_ly": 21000000,
        "angular_size_arcmin": 28.8,
        "magnitude": 7.9,
        "ra": 210.8023,
        "dec": 54.3489,
        "aliases": ["NGC 5457", "Messier 101"],
        "catalog_ids": {"M": "101", "NGC": "5457"},
    },
    {
        "primary_name": "NGC 7000",
        "display_name": "North America Nebula",
        "object_type": "Emission Nebula",
        "constellation": "Cygnus",
        "distance_ly": 2590,
        "angular_size_arcmin": 120.0,
        "magnitude": 4.0,
        "ra": 314.75,
        "dec": 44.3333,
        "aliases": ["Caldwell 20"],
        "catalog_ids": {"NGC": "7000", "C": "20"},
    },
    {
        "primary_name": "IC 434",
        "display_name": "Horsehead Nebula",
        "object_type": "Dark Nebula",
        "constellation": "Orion",
        "distance_ly": 1375,
        "angular_size_arcmin": 8.0,
        "magnitude": 6.8,
        "ra": 85.2458,
        "dec": -2.4583,
        "aliases": ["Barnard 33"],
        "catalog_ids": {"IC": "434", "B": "33"},
    },
    {
        "primary_name": "IC 1396",
        "display_name": "Elephant's Trunk Nebula",
        "object_type": "Emission Nebula",
        "constellation": "Cepheus",
        "distance_ly": 2400,
        "angular_size_arcmin": 170.0,
        "magnitude": 3.5,
        "ra": 324.75,
        "dec": 57.5,
        "aliases": ["LBN 452"],
        "catalog_ids": {"IC": "1396"},
    },
    {
        "primary_name": "NGC 6888",
        "display_name": "Crescent Nebula",
        "object_type": "Emission Nebula",
        "constellation": "Cygnus",
        "distance_ly": 5000,
        "angular_size_arcmin": 18.0,
        "magnitude": 7.4,
        "ra": 303.025,
        "dec": 38.3542,
        "aliases": ["Caldwell 27"],
        "catalog_ids": {"NGC": "6888", "C": "27"},
    },
    {
        "primary_name": "M13",
        "display_name": "Great Globular Cluster in Hercules",
        "object_type": "Globular Cluster",
        "constellation": "Hercules",
        "distance_ly": 22200,
        "angular_size_arcmin": 20.0,
        "magnitude": 5.8,
        "ra": 250.4235,
        "dec": 36.4613,
        "aliases": ["NGC 6205", "Messier 13"],
        "catalog_ids": {"M": "13", "NGC": "6205"},
    },
    {
        "primary_name": "M27",
        "display_name": "Dumbbell Nebula",
        "object_type": "Planetary Nebula",
        "constellation": "Vulpecula",
        "distance_ly": 1360,
        "angular_size_arcmin": 8.0,
        "magnitude": 7.5,
        "ra": 299.9016,
        "dec": 22.721,
        "aliases": ["NGC 6853", "Messier 27"],
        "catalog_ids": {"M": "27", "NGC": "6853"},
    },
]

FILTERS = ["L", "R", "G", "B", "Ha", "OIII", "SII"]
SCOPES = ["Esprit 100ED", "RedCat 51", "Celestron RASA 8", "EdgeHD 8", "Newtonian 200PDS"]
CAMERAS = ["ASI2600MM Pro", "ASI533MC Pro", "QHY268M", "Canon EOS Ra"]
MOUNTS = ["EQ6-R Pro", "AM5", "CEM40", "HEQ5 Pro"]


def slugify(value: str) -> str:
    return value.lower().replace("'", "").replace(" ", "-").replace("_", "-").replace(".", "")


def format_distance(distance_ly: float | None) -> str | None:
    if distance_ly is None:
        return None
    if distance_ly >= 1_000_000:
        return f"{distance_ly / 1_000_000:.1f} million ly"
    if distance_ly >= 1_000:
        return f"{distance_ly / 1_000:.1f} kly"
    return f"{distance_ly:.0f} ly"


def format_angular_size(size_arcmin: float | None) -> str | None:
    if size_arcmin is None:
        return None
    if size_arcmin >= 60:
        return f"{size_arcmin / 60:.1f} deg"
    return f"{size_arcmin:.1f} arcmin"


class AstroObjectFactory(factory.Factory):
    class Meta:
        model = AstroObject

    slug = factory.LazyAttribute(lambda obj: slugify(obj.primary_name))
    primary_name = factory.Sequence(lambda n: f"NGC {7000 + n}")
    display_name = factory.LazyAttribute(lambda obj: obj.primary_name)
    object_type = factory.Iterator(
        ["Galaxy", "Emission Nebula", "Open Cluster", "Globular Cluster", "Planetary Nebula"]
    )
    constellation = factory.Faker("word")
    distance_ly = factory.LazyFunction(lambda: fake.pyfloat(min_value=400, max_value=30_000_000))
    distance_display = factory.LazyAttribute(lambda obj: format_distance(obj.distance_ly))
    angular_size_arcmin = factory.LazyFunction(lambda: round(random.uniform(6.0, 160.0), 1))
    angular_size_display = factory.LazyAttribute(
        lambda obj: format_angular_size(obj.angular_size_arcmin)
    )
    magnitude = factory.LazyFunction(lambda: round(random.uniform(1.5, 12.5), 1))
    ra = factory.LazyFunction(lambda: round(random.uniform(0.0, 360.0), 4))
    dec = factory.LazyFunction(lambda: round(random.uniform(-70.0, 75.0), 4))
    coordinate_system = "ICRS"
    aliases = factory.List([])
    catalog_ids = factory.Dict({})
    description = factory.LazyAttribute(
        lambda obj: (
            f"{obj.display_name or obj.primary_name} is a {obj.object_type.lower()} in "
            f"{obj.constellation}, commonly framed for deep-sky imaging projects."
        )
    )
    enrichment_sources = factory.LazyFunction(
        lambda: random.sample(list(EnrichmentSource), k=random.randint(1, len(EnrichmentSource)))
    )
    last_enriched_at = factory.LazyFunction(
        lambda: fake.date_time_between(start_date="-90d", end_date="now")
    )


class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    object = factory.SubFactory(AstroObjectFactory)
    name = factory.LazyAttribute(
        lambda obj: f"{obj.object.display_name or obj.object.primary_name} LRGB"
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    path = factory.LazyAttribute(lambda obj: f"/astro-library/{obj.object.slug}/{obj.slug}")


class SessionFactory(factory.Factory):
    class Meta:
        model = ImagingSession

    project = factory.SubFactory(ProjectFactory)
    date = factory.LazyFunction(lambda: fake.date_between(start_date="-18M", end_date="today"))
    path = factory.LazyAttribute(lambda obj: f"{obj.project.path}/sessions/{obj.date.isoformat()}")
    integration_seconds = factory.LazyFunction(
        lambda: random.randint(24, 180) * random.choice([120, 180, 300, 600])
    )
    notes = factory.LazyFunction(
        lambda: (
            f"{random.choice(SCOPES)} with {random.choice(CAMERAS)} on "
            f"{random.choice(MOUNTS)}. Seeing {random.choice(['fair', 'good', 'steady'])}; "
            f"{random.choice(['thin haze early', 'clear all night', 'moon below horizon'])}."
        )
    )


class FileFactory(factory.Factory):
    class Meta:
        model = File

    project = factory.SubFactory(ProjectFactory)
    session = None
    relative_path = factory.LazyAttribute(lambda obj: f"{obj.project.slug}/{obj.filename}")
    filename = factory.LazyFunction(lambda: fake.file_name(extension="fits"))
    extension = factory.LazyAttribute(lambda obj: obj.filename.rsplit(".", maxsplit=1)[-1])
    file_role = FileRole.UNKNOWN
    size_bytes = factory.LazyFunction(lambda: random.randint(18_000_000, 65_000_000))
    modified_at = factory.LazyFunction(
        lambda: fake.date_time_between(start_date="-18M", end_date="now")
    )
    width = factory.LazyFunction(lambda: random.choice([3008, 4144, 6248, 9576]))
    height = factory.LazyFunction(lambda: random.choice([3008, 2822, 4176, 6388]))


def clear_seeded_data(db: DbSession) -> None:
    db.execute(update(AstroObject).values(hero_file_id=None))
    db.execute(update(Project).values(hero_file_id=None))
    db.execute(delete(File))
    db.execute(delete(ImagingSession))
    db.execute(delete(Project))
    db.execute(delete(AstroObject))
    db.flush()


def build_project_name(target: dict[str, Any], index: int) -> str:
    suffixes = ["LRGB", "Narrowband", "Widefield", "High Resolution", "HaRGB"]
    base = target.get("display_name") or target["primary_name"]
    return f"{base} {suffixes[index % len(suffixes)]}"


def make_session_files(
    project: Project,
    session: ImagingSession,
    *,
    light_count: int,
    dark_count: int,
    flat_count: int,
    flat_calibration_role: FileRole,
    flat_calibration_count: int,
) -> list[File]:
    files: list[File] = []
    session_dir = f"{project.slug}/sessions/{session.date.isoformat()}"
    exposure = (session.integration_seconds or 0) // max(light_count, 1)

    for index in range(light_count):
        image_filter = random.choice(FILTERS)
        filename = (
            f"{project.slug}_{session.date:%Y%m%d}_{image_filter}_"
            f"{exposure}s_light_{index + 1:03}.fits"
        )
        files.append(
            FileFactory(
                project=project,
                session=session,
                relative_path=f"{session_dir}/lights/{filename}",
                filename=filename,
                file_role=FileRole.LIGHT,
                modified_at=datetime.combine(session.date, fake.time_object())
                + timedelta(minutes=index * 4),
            )
        )

    calibration_specs = [
        (FileRole.DARK, dark_count, "darks"),
        (FileRole.FLAT, flat_count, "flats"),
        (
            flat_calibration_role,
            flat_calibration_count,
            "bias" if flat_calibration_role == FileRole.BIAS else "dark-flats",
        ),
    ]
    for role, count, folder in calibration_specs:
        for index in range(min(count, 12)):
            filename = (
                f"{project.slug}_{session.date:%Y%m%d}_{role.value.lower()}_{index + 1:03}.fits"
            )
            files.append(
                FileFactory(
                    project=project,
                    session=session,
                    relative_path=f"{session_dir}/{folder}/{filename}",
                    filename=filename,
                    file_role=role,
                    modified_at=datetime.combine(session.date, fake.time_object()),
                )
            )

    log_name = f"{project.slug}_{session.date:%Y%m%d}_capture.log"
    files.append(
        FileFactory(
            project=project,
            session=session,
            relative_path=f"{session_dir}/{log_name}",
            filename=log_name,
            extension="log",
            file_role=FileRole.LOG,
            size_bytes=random.randint(24_000, 180_000),
            width=None,
            height=None,
        )
    )
    return files


def make_project_files(project: Project) -> list[File]:
    files: list[File] = []
    for role, extension in [(FileRole.EXPORT, "jpg"), (FileRole.EDIT, "tif")]:
        filename = f"{project.slug}_final.{extension}"
        files.append(
            FileFactory(
                project=project,
                relative_path=f"{project.slug}/exports/{filename}",
                filename=filename,
                extension=extension,
                file_role=role,
                size_bytes=random.randint(4_000_000, 220_000_000),
                width=random.choice([3840, 5120, 6248, 7680]),
                height=random.choice([2160, 4096, 4176, 5120]),
            )
        )
    return files


def object_slug_exists(db: DbSession, slug: str) -> bool:
    return (
        db.scalar(select(func.count()).select_from(AstroObject).where(AstroObject.slug == slug)) > 0
    )


def seed_database(
    db: DbSession,
    *,
    object_count: int,
    min_sessions: int,
    max_sessions: int,
    clear: bool,
) -> dict[str, int]:
    if clear:
        clear_seeded_data(db)

    target_pool = TARGETS[:object_count]
    while len(target_pool) < object_count:
        sequence = len(target_pool) + 1
        target_pool.append(
            {
                "primary_name": f"NGC {fake.unique.random_int(min=100, max=7999)}",
                "display_name": fake.unique.catch_phrase(),
                "object_type": random.choice(["Galaxy", "Emission Nebula", "Open Cluster"]),
                "constellation": fake.word().title(),
                "aliases": [f"Seed Target {sequence}"],
                "catalog_ids": {"SEED": str(sequence)},
            }
        )

    created_objects: list[AstroObject] = []
    created_projects: list[Project] = []
    created_sessions: list[ImagingSession] = []
    created_files: list[File] = []

    for target_index, target in enumerate(target_pool):
        object_slug = slugify(target["primary_name"])
        if not clear and object_slug_exists(db, object_slug):
            object_slug = f"{object_slug}-{fake.unique.random_int(min=1000, max=9999)}"

        astro_object = AstroObjectFactory(
            slug=object_slug,
            distance_display=format_distance(target.get("distance_ly")),
            angular_size_display=format_angular_size(target.get("angular_size_arcmin")),
            **target,
        )
        db.add(astro_object)
        created_objects.append(astro_object)

        project_total = 1 if random.random() < 0.7 else 2
        for project_index in range(project_total):
            project_name = build_project_name(target, project_index)
            project = ProjectFactory(
                object=astro_object,
                name=project_name,
                slug=slugify(project_name),
                path=f"/astro-library/{astro_object.slug}/{slugify(project_name)}",
            )
            db.add(project)
            created_projects.append(project)

            session_dates: set[date] = set()
            for _ in range(random.randint(min_sessions, max_sessions)):
                session_date = fake.date_between(start_date="-18M", end_date="today")
                while session_date in session_dates:
                    session_date = fake.date_between(start_date="-18M", end_date="today")
                session_dates.add(session_date)

                light_count = random.randint(24, 180)
                exposure_seconds = random.choice([120, 180, 300, 600])
                session = SessionFactory(
                    project=project,
                    date=session_date,
                    path=f"{project.path}/sessions/{session_date.isoformat()}",
                    integration_seconds=light_count * exposure_seconds,
                )
                db.add(session)
                created_sessions.append(session)
                session_files = make_session_files(
                    project,
                    session,
                    light_count=light_count,
                    dark_count=random.choice([20, 30, 40, 50]),
                    flat_count=random.choice([30, 40, 50]),
                    flat_calibration_role=random.choice([FileRole.BIAS, FileRole.DARK_FLAT]),
                    flat_calibration_count=random.choice([30, 40, 50, 60]),
                )
                db.add_all(session_files)
                created_files.extend(session_files)

            project_files = make_project_files(project)
            db.add_all(project_files)
            created_files.extend(project_files)
            project.hero_file = project_files[0]

        if astro_object.projects:
            astro_object.hero_file = astro_object.projects[0].hero_file

        if target_index % 4 == 0:
            db.flush()

    db.commit()

    return {
        "objects": len(created_objects),
        "projects": len(created_projects),
        "sessions": len(created_sessions),
        "files": len(created_files),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the astro library database with demo data.")
    parser.add_argument(
        "--objects",
        type=int,
        default=12,
        help="Number of astro objects to create.",
    )
    parser.add_argument(
        "--min-sessions",
        type=int,
        default=2,
        help="Minimum sessions per project.",
    )
    parser.add_argument(
        "--max-sessions",
        type=int,
        default=5,
        help="Maximum sessions per project.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatable data.")
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Append records instead of clearing objects, projects, sessions, and files first.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.objects < 1:
        raise SystemExit("--objects must be at least 1")
    if args.min_sessions < 0 or args.max_sessions < args.min_sessions:
        raise SystemExit("--max-sessions must be greater than or equal to --min-sessions")

    random.seed(args.seed)
    fake.seed_instance(args.seed)
    factory.random.reseed_random(args.seed)

    init_db()
    with SessionLocal() as db:
        counts = seed_database(
            db,
            object_count=args.objects,
            min_sessions=args.min_sessions,
            max_sessions=args.max_sessions,
            clear=not args.no_clear,
        )

        persisted = {
            "objects": db.scalar(select(func.count()).select_from(AstroObject)),
            "projects": db.scalar(select(func.count()).select_from(Project)),
            "sessions": db.scalar(select(func.count()).select_from(ImagingSession)),
            "files": db.scalar(select(func.count()).select_from(File)),
        }

    print(
        "Seeded "
        f"{counts['objects']} objects, "
        f"{counts['projects']} projects, "
        f"{counts['sessions']} sessions, "
        f"{counts['files']} files."
    )
    print(
        "Database now contains "
        f"{persisted['objects']} objects, "
        f"{persisted['projects']} projects, "
        f"{persisted['sessions']} sessions, "
        f"{persisted['files']} files."
    )


if __name__ == "__main__":
    main()
