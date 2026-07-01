"""News Hub - Scheduled daily execution for Oggy & Jack news reels."""

from __future__ import annotations

import logging
import sys
import time
from datetime import datetime, timedelta

import schedule as schedule_lib

from news_hub.config.settings import settings
from news_hub.main import main

logger = logging.getLogger(__name__)


def setup_schedule_logging() -> None:
    """Configure logging for scheduler."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(settings.output_dir / "scheduler.log"),
        ]
    )


def job() -> None:
    """Job to run the news reel generation and upload."""
    logger.info("=" * 60)
    logger.info("Scheduled Job Started: %s", datetime.now())
    logger.info("=" * 60)
    
    try:
        # Run main with default settings (all steps)
        import argparse
        sys.argv = ["news-hub"]  # Reset args
        main()
    except Exception as e:
        logger.error("Scheduled job failed: %s", e, exc_info=True)
    finally:
        logger.info("Scheduled job completed at: %s", datetime.now())


def schedule_jobs() -> None:
    """Schedule jobs based on settings."""
    times = settings.reel_schedule_times
    
    for time_str in times:
        try:
            # Parse time (HH:MM format)
            hour, minute = map(int, time_str.split(":"))
            
            # Schedule job at this time every day
            schedule_lib.every().day.at(f"{hour:02d}:{minute:02d}").do(job)
            
            logger.info("Scheduled job at %s daily", time_str)
        except Exception as e:
            logger.error("Invalid schedule time format '%s': %s", time_str, e)


def run_scheduler() -> None:
    """Run the scheduler in an infinite loop."""
    setup_schedule_logging()
    
    logger.info("=" * 60)
    logger.info("News Hub Scheduler Started")
    logger.info("=" * 60)
    logger.info("Configured to generate %d reels per day at: %s", 
                settings.reels_per_day, ", ".join(settings.reel_schedule_times))
    
    # Schedule jobs
    schedule_jobs()
    
    # Initial run if it's time
    job()
    
    # Run scheduler
    while True:
        try:
            schedule_lib.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            sys.exit(0)
        except Exception as e:
            logger.error("Scheduler error: %s", e)
            time.sleep(60)  # Wait before retrying


def main() -> None:
    """Main entry point for scheduler."""
    run_scheduler()


if __name__ == "__main__":
    main()
