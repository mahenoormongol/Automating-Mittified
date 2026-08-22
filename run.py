"""
Mittified — Automated Pakistani Drama/News Instagram Pipeline
Entry point: starts the scheduler + FastAPI web dashboard.
"""

import sys
import os
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger


def setup_logging():
    """Configure loguru logging."""
    from config.settings import settings
    log_dir = PROJECT_ROOT / "data"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan> - {message}",
    )
    logger.add(
        log_dir / "mittified.log",
        rotation="5 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{line} - {message}",
    )


def init_directories():
    """Ensure required data directories exist."""
    from config.settings import settings
    settings.media_dir.mkdir(parents=True, exist_ok=True)
    settings.browser_sessions_dir.mkdir(parents=True, exist_ok=True)
    (settings.media_dir / "generated").mkdir(exist_ok=True)
    (settings.media_dir / "carousels").mkdir(exist_ok=True)
    (settings.media_dir / "stories").mkdir(exist_ok=True)
    (settings.media_dir / "thumbnails").mkdir(exist_ok=True)
    (settings.media_dir / "videos").mkdir(exist_ok=True)


def check_env():
    """Check .env file and warn about missing credentials (non-blocking)."""
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        # Create from example if available
        example = PROJECT_ROOT / ".env.example"
        if example.exists():
            import shutil
            shutil.copy(example, env_path)
            logger.info("Created .env from .env.example — configure via dashboard")
        else:
            logger.warning("No .env file found — creating empty one")
            env_path.write_text("# Mittified configuration — edit via dashboard at http://localhost:8000\n")

    from config.settings import settings
    missing = []
    if not settings.groq_api_key:
        missing.append("GROQ_API_KEY")
    if not settings.instagram_access_token:
        missing.append("INSTAGRAM_ACCESS_TOKEN")
    if not settings.instagram_business_account_id:
        missing.append("INSTAGRAM_BUSINESS_ACCOUNT_ID")

    if missing:
        logger.warning(
            f"Missing credentials: {', '.join(missing)} — "
            f"Open http://localhost:8000 and go to the Setup tab to configure"
        )
    else:
        logger.info("All required credentials configured")


def main():
    """Start the full Mittified system."""
    setup_logging()
    init_directories()
    check_env()
    logger.info("Starting Mittified...")

    # Initialize database
    from src.database.engine import init_db
    init_db()
    logger.info("Database initialized")

    # Start scheduler (jobs will gracefully skip if credentials are missing)
    try:
        from src.scheduler.manager import start_scheduler
        start_scheduler()
        logger.info("Scheduler started")
    except Exception as e:
        logger.warning(f"Scheduler start issue (non-fatal): {e}")

    # Start FastAPI dashboard
    import uvicorn
    from src.ui.app import create_app
    from config.settings import settings

    app = create_app()

    print()
    print("  +---------------------------------------+")
    print("  |          MITTIFIED IS RUNNING          |")
    print(f"  |  Dashboard: http://localhost:{settings.port}      |")
    print("  +---------------------------------------+")
    print()

    uvicorn.run(app, host=settings.host, port=settings.port, log_level="warning")


if __name__ == "__main__":
    main()
