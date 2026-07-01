"""News Hub - Main entry point for generating AI news reels with Oggy & Jack."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from news_hub.config.settings import settings
from news_hub.pipeline.news_fetcher import get_top_stories
from news_hub.pipeline.script_generator import generate_scripts_for_stories
from news_hub.pipeline.video_generator import generate_reels_from_scripts
from news_hub.pipeline.social_uploader import upload_reels

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging based on settings."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(settings.output_dir / "news_hub.log"),
        ]
    )


def main() -> None:
    """Main function to generate and upload news reels."""
    parser = argparse.ArgumentParser(
        description="Generate AI news reels with Oggy & Jack and upload to social media"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=settings.reels_per_day,
        help="Number of reels to generate (default: from settings)"
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Generate reels but don't upload to social media"
    )
    parser.add_argument(
        "--skip-video",
        action="store_true",
        help="Only fetch news and generate scripts, don't create videos"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode with sample data"
    )
    parser.add_argument(
        "--upload-only",
        action="store_true",
        help="Only upload existing reels, don't generate new ones"
    )
    parser.add_argument(
        "--only-upload",
        action="store_true",
        help="Alias for --upload-only"
    )
    
    args = parser.parse_args()
    
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("News Hub - Oggy & Jack AI News Reels Generator")
    logger.info("=" * 60)
    
    try:
        # Upload-only mode: skip generation, only upload existing reels
        if args.upload_only or args.only_upload:
            logger.info("Running in upload-only mode...")
            from pathlib import Path
            output_dir = Path(settings.output_dir)
            reels = list(output_dir.glob("*.mp4"))
            
            if not reels:
                logger.info("No reels found in output directory for upload")
                sys.exit(0)
            
            logger.info(f"Found {len(reels)} reels to upload")
            news_titles = ["Auto-uploaded reel" for _ in reels]
            categories = ["automated" for _ in reels]
            
            upload_results = upload_reels(reels, news_titles, categories)
            
            # Print upload results
            logger.info("\n" + "=" * 60)
            logger.info("Upload Results:")
            logger.info("=" * 60)
            
            for i, (reel, results) in enumerate(zip(reels, upload_results), 1):
                logger.info(f"\nReel {i}: {reel.name}")
                for result in results:
                    if result.success:
                        logger.info(f"  ✓ {result.platform}: {result.url}")
                    else:
                        logger.info(f"  ✗ {result.platform}: {result.error}")
            
            total_uploads = sum(len(r) for r in upload_results)
            successful_uploads = sum(1 for r in upload_results for res in r if res.success)
            
            logger.info(f"\nTotal uploads attempted: {total_uploads}")
            logger.info(f"Successful uploads: {successful_uploads}")
            
            if successful_uploads == total_uploads:
                logger.info("✓ All uploads successful!")
            else:
                logger.warning(f"⚠ {total_uploads - successful_uploads} uploads failed")
            
            sys.exit(0)
        
        # Step 1: Fetch top news stories
        logger.info("Fetching top Indian news stories...")
        stories = get_top_stories(count=args.count)
        
        if not stories:
            logger.error("No news stories found! Check your internet connection and news sources.")
            sys.exit(1)
        
        logger.info(f"Fetched {len(stories)} news stories:")
        for i, story in enumerate(stories, 1):
            logger.info(f"  {i}. {story.title[:60]} ({story.category})")
        
        # Step 2: Generate scripts
        logger.info("Generating Oggy & Jack dialogue scripts...")
        scripts = generate_scripts_for_stories(stories)
        
        logger.info(f"Generated {len(scripts)} scripts")
        
        if args.skip_video:
            logger.info("Skipping video generation (--skip-video flag)")
            # Print scripts to console
            for i, (script, story) in enumerate(zip(scripts, stories), 1):
                logger.info(f"\n{'='*60}")
                logger.info(f"Reel {i}: {story.title}")
                logger.info(f"{'='*60}")
                logger.info(script)
            sys.exit(0)
        
        # Step 3: Generate video reels
        logger.info("Generating video reels...")
        reels = generate_reels_from_scripts(scripts)
        
        logger.info(f"Generated {len(reels)} video reels:")
        for reel in reels:
            logger.info(f"  - {reel}")
        
        if args.no_upload:
            logger.info("Skipping social media upload (--no-upload flag)")
            sys.exit(0)
        
        # Step 4: Upload to social media
        logger.info("Uploading to social media platforms...")
        
        news_titles = [story.title for story in stories]
        categories = [story.category for story in stories]
        
        upload_results = upload_reels(reels, news_titles, categories)
        
        # Print upload results
        logger.info("\n" + "=" * 60)
        logger.info("Upload Results:")
        logger.info("=" * 60)
        
        for i, (reel, results) in enumerate(zip(reels, upload_results), 1):
            logger.info(f"\nReel {i}: {reel.name}")
            for result in results:
                if result.success:
                    logger.info(f"  ✓ {result.platform}: {result.url}")
                else:
                    logger.info(f"  ✗ {result.platform}: {result.error}")
        
        # Count successful uploads
        total_uploads = sum(len(r) for r in upload_results)
        successful_uploads = sum(1 for r in upload_results for res in r if res.success)
        
        logger.info(f"\nTotal uploads attempted: {total_uploads}")
        logger.info(f"Successful uploads: {successful_uploads}")
        
        if successful_uploads == total_uploads:
            logger.info("✓ All uploads successful!")
        else:
            logger.warning(f"⚠ {total_uploads - successful_uploads} uploads failed")
        
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
