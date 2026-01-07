import os
import sys
import subprocess
import shutil
import django
import time
from pathlib import Path
from threading import Thread
from django.db import connections
import psycopg2
from django.conf import settings


# ======================================================
# Spinner
# ======================================================
class Spinner:
    def __init__(self, message="Processing..."):
        self.message = message
        self.running = False
        self.spinner_cycle = ["|", "/", "-", "\\"]

    def start(self):
        self.running = True
        Thread(target=self._spin, daemon=True).start()

    def _spin(self):
        idx = 0
        while self.running:
            print(
                f"\r{self.message} {self.spinner_cycle[idx % len(self.spinner_cycle)]}",
                end="",
            )
            idx += 1
            time.sleep(0.08)

    def stop(self):
        self.running = False
        print("\r", end="")


# ======================================================
# Timer
# ======================================================
class Timer:
    def __init__(self, label="Elapsed"):
        self.label = label
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            print("⚠️ Timer not started.")
            return None
        elapsed = time.time() - self.start_time
        print(f"⏱️ {self.label}: {elapsed:.2f} seconds")
        return elapsed


# ======================================================
# Helpers
# ======================================================
def run_cmd(cmd, show_spinner=False, message=None):
    if show_spinner and message:
        spinner = Spinner(message)
        spinner.start()
        result = subprocess.run(cmd, shell=True)
        spinner.stop()
    else:
        result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(result.returncode)


def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created folder: {path}")


# ======================================================
# Cleaners
# ======================================================
class Cleaner:
    def __init__(self, path: Path):
        self.path = path

    def exists(self) -> bool:
        return self.path.exists()


class DatabaseAutoSwitcher:
    """
    Automatically switch to SQLite if PostgreSQL is unavailable.
    Runs BEFORE django.setup()
    """

    def __init__(self, timeout=2):
        self.timeout = timeout

    def postgres_available(self, db):
        try:
            psycopg2.connect(
                dbname=db["NAME"],
                user=db["USER"],
                password=db["PASSWORD"],
                host=db.get("HOST", "localhost"),
                port=db.get("PORT", 5432),
                connect_timeout=self.timeout,
            ).close()
            return True
        except Exception:
            return False

    def switch_if_needed(self):
        db = settings.DATABASES["default"]
        engine = db["ENGINE"]

        # Only care if PostgreSQL is configured
        if "postgresql" not in engine:
            print("ℹ️ PostgreSQL not configured — using existing DB")
            return

        print("🔍 Checking PostgreSQL availability...")

        if self.postgres_available(db):
            print("🐘 PostgreSQL is running")
            return

        print("⚠️ PostgreSQL NOT running — falling back to SQLite")

        sqlite_path = Path("./database/db.sqlite3")
        sqlite_path.parent.mkdir(exist_ok=True)

        settings.DATABASES["default"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(sqlite_path),
        }

        print(f"🪶 SQLite activated at {sqlite_path}")


class CrossDatabaseCleaner:
    """
    Cross-database cleaner for Django projects.

    ✔ Supports SQLite & PostgreSQL
    ✔ Automatically detects active DB engine
    ✔ Refuses to run outside DEBUG mode (safety)

    ------------------------------------------------
    🔐 ENV REFERENCE (DO NOT COMMIT REAL SECRETS)
    ------------------------------------------------
    DEBUG=True
    ALLOWED_HOSTS=*
    SECRET_KEY=django-insecure-56%_hh9#xap(yrbv+_yjn_286)t(@blufv77)a%yof89#awv^6

    DB_NAME=portfolio
    DB_USER=postgres
    DB_PASS=admin
    DB_HOST=localhost
    DB_PORT=5432
    ------------------------------------------------
    """

    def clean(self):
        # ------------------------------------------------
        # SAFETY GUARD — NEVER RESET DB IN PROD
        # ------------------------------------------------
        if not settings.DEBUG:
            raise RuntimeError(
                "❌ Refusing to reset database because DEBUG=False. "
                "This operation is allowed only in development."
            )

        db = settings.DATABASES["default"]
        engine = db["ENGINE"]

        # Close all active Django DB connections
        try:
            connections.close_all()
        except Exception:
            pass

        # ------------------------------------------------
        # SQLITE CLEANUP
        # ------------------------------------------------
        if "sqlite3" in engine:
            db_path = Path(db["NAME"])

            if db_path.exists():
                db_path.unlink()
                print(f"🗑️ SQLite database deleted: {db_path}")
            else:
                print("ℹ️ SQLite database not found")

        # ------------------------------------------------
        # POSTGRESQL CLEANUP
        # ------------------------------------------------
        elif "postgresql" in engine:
            db_name = db["NAME"]
            db_user = db.get("USER", "postgres")

            print("🗑️ Resetting PostgreSQL database...")

            subprocess.run(
                f'psql -U {db_user} -c "DROP DATABASE IF EXISTS {db_name};"',
                shell=True,
                check=False,
            )
            subprocess.run(
                f'psql -U {db_user} -c "CREATE DATABASE {db_name};"',
                shell=True,
                check=False,
            )

            print("✅ PostgreSQL database recreated")

        # ------------------------------------------------
        # UNSUPPORTED DATABASE
        # ------------------------------------------------
        else:
            raise RuntimeError(f"❌ Unsupported DB engine: {engine}")


# class PycacheCleaner(Cleaner):
#     def clean(self):
#         for p in self.path.rglob("__pycache__"):
#             if p.is_dir():
#                 shutil.rmtree(p)
#                 print("🧹 Removed:", p)


class PycacheCleaner(Cleaner):
    """
    Removes ALL __pycache__ directories recursively.
    """

    def clean(self):
        if not self.exists():
            print("❌ Path does not exist")
            return

        removed = False

        for p in self.path.rglob("__pycache__"):
            if p.is_dir():
                shutil.rmtree(p)
                print("🧹 Removed:", p)
                removed = True

        if not removed:
            print("✔️ No __pycache__ folders found")


class MigrationsCleaner(Cleaner):
    """
    Safely removes ONLY Django-generated migration files.
    Keeps:
      ✔ migrations/ directory
      ✔ __init__.py
    """

    def clean(self):
        if not self.exists():
            print("❌ Apps path does not exist")
            return

        removed_any = False

        for app_dir in self.path.iterdir():
            migrations_dir = app_dir / "migrations"

            if not migrations_dir.is_dir():
                continue

            for file in migrations_dir.iterdir():
                # Keep __init__.py ALWAYS
                if file.name == "__init__.py":
                    continue

                # Remove only .py migration files like 0001_*.py
                if file.is_file() and file.suffix == ".py" and file.name[0:4].isdigit():
                    file.unlink()
                    print("🧹 Removed migration:", file)
                    removed_any = True

                # Also remove compiled leftovers safely
                if file.suffix in {".pyc"}:
                    file.unlink()
                    print("🧹 Removed cache:", file)
                    removed_any = True

        if not removed_any:
            print("✔️ No generated migration files found")


# ======================================================
# Migration + Superuser
# ======================================================
class MigrationAndSuperuser:
    def run(self):
        run_cmd(
            "python manage.py makemigrations",
            show_spinner=True,
            message="Making migrations",
        )
        run_cmd(
            "python manage.py migrate", show_spinner=True, message="Applying migrations"
        )

        print("Checking superuser...")
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="admin", email="admin@gmail.com", password="admin"
            )
            print("👑 Superuser created")
        else:
            print("✔️ Superuser already exists")


# ======================================================
# Fixture Loader
# ======================================================
class FixtureLoader:
    def __init__(self, fixture_path, retries=3, delay=1.5):
        self.fixture_path = fixture_path
        self.retries = retries
        self.delay = delay

    def load(self):
        attempt = 1
        while attempt <= self.retries:
            result = subprocess.run(
                f"python manage.py loaddata {self.fixture_path}", shell=True
            )
            if result.returncode == 0:
                print("📦 Fixtures loaded successfully")
                return
            time.sleep(self.delay)
            attempt += 1
        print("❌ Failed loading fixtures")


# ======================================================
# NEW CLASS: GenerateFixtures
# ======================================================
class GenerateFixtures:
    """Reusable fixture generator class for future projects."""

    def run(self):
        print("🔄 Generating fixtures...")
        run_cmd("uv run manage.py generate_fixtures")
        run_cmd("uv run manage.py generate_homepage_fixtures")
        print("✨ Fixture generation completed!")


# ======================================================
# MENU
# ======================================================
def menu():
    print("\n=== Automation Menu ===")
    print("1️⃣ Remove DB")
    print("2️⃣ Remove __pycache__")
    print("3️⃣ Remove migration files")
    print("4️⃣ Run migrations + Ensure Superuser")
    print("5️⃣ Load Products Fixture")
    print("6️⃣ FULL RESET (DB + Pycache + Migrations + Migrate)")
    print("7️⃣ Generate Fixtures (NEW)")
    print("0️⃣ Exit")
    return input("Choose: ").strip()


# ======================================================
# MAIN LOOP
# ======================================================
if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")

    # 🔥 MUST run before django.setup()
    from django.conf import settings

    DatabaseAutoSwitcher().switch_if_needed()

    django.setup()

    # apps_path = Path("./apps")
    db_file = Path("./database/db.sqlite3")

    apps_path = Path("./apps")
    db_folder = Path("./database")

    # Ensure required folders exist
    # ensure_dir(apps_path)
    ensure_dir(db_folder)
    # ensure_dir(fixtures_folder)

    while True:
        choice = menu()

        if choice == "1":
            # DatabaseCleaner(db_file).clean()
            CrossDatabaseCleaner().clean()

        elif choice == "2":
            PycacheCleaner(apps_path).clean()

        elif choice == "3":
            MigrationsCleaner(apps_path).clean()

        elif choice == "4":
            MigrationAndSuperuser().run()

        elif choice == "5":
            FixtureLoader("fixtures/products_fixture.json").load()

        elif choice == "6":
            print("⚠️ FULL RESET...")
            # DatabaseCleaner(db_file).clean()
            CrossDatabaseCleaner().clean()
            PycacheCleaner(apps_path).clean()
            MigrationsCleaner(apps_path).clean()
            # MigrationAndSuperuser().run()
            print("🚀 FULL RESET DONE!")

        elif choice == "7":
            MigrationAndSuperuser().run()
            GenerateFixtures().run()

        elif choice == "0":
            print("Bye 👋")
            break

        else:
            print("Invalid option!")
