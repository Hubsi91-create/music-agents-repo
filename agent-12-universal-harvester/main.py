"""
Universal Harvester - Main Entry Point

Provides CLI interface and HTTP server for harvesting operations.

Usage:
    python main.py harvest --type=trend
    python main.py harvest --type=all
    python main.py status
    python main.py serve

Author: Universal Harvester System
Version: 1.0.0
"""

import argparse
import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import (
    TrendHarvester,
    AudioHarvester,
    ScreenplayHarvester,
    CreatorHarvester,
    DistributionHarvester,
    SoundHarvester
)
from database.harvested_data import HarvestedDataDB

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UniversalHarvester")

# ============================================================
# CONFIGURATION
# ============================================================

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    if not os.path.exists(config_path):
        logger.error("config.json not found")
        return {}

    with open(config_path, 'r') as f:
        return json.load(f)

# ============================================================
# HARVESTER FACTORY
# ============================================================

class UniversalHarvester:
    """Main harvester orchestrator."""

    def __init__(self):
        """Initialize all harvesters."""
        self.config = load_config()
        self.db = HarvestedDataDB(
            db_path=self.config.get('database', {}).get('path', './database/harvested_data.db')
        )

        # Initialize harvesters
        self.harvesters = {}

        harvester_config = self.config.get('harvesters', {})

        if harvester_config.get('trend', {}).get('enabled', True):
            self.harvesters['trend'] = TrendHarvester(harvester_config.get('trend', {}))

        if harvester_config.get('audio', {}).get('enabled', True):
            self.harvesters['audio'] = AudioHarvester(harvester_config.get('audio', {}))

        if harvester_config.get('screenplay', {}).get('enabled', True):
            self.harvesters['screenplay'] = ScreenplayHarvester(harvester_config.get('screenplay', {}))

        if harvester_config.get('creator', {}).get('enabled', True):
            self.harvesters['creator'] = CreatorHarvester(harvester_config.get('creator', {}))

        if harvester_config.get('distribution', {}).get('enabled', True):
            self.harvesters['distribution'] = DistributionHarvester(harvester_config.get('distribution', {}))

        if harvester_config.get('sound', {}).get('enabled', True):
            self.harvesters['sound'] = SoundHarvester(harvester_config.get('sound', {}))

        logger.info(f"Initialized {len(self.harvesters)} harvesters")

    def harvest(self, harvester_type: str, force: bool = False) -> Dict[str, Any]:
        """
        Run a specific harvester.

        Args:
            harvester_type: Type of harvester ('trend', 'audio', etc.)
            force: Force fresh harvest (bypass cache)

        Returns:
            Harvest result dict
        """
        if harvester_type not in self.harvesters:
            return {
                'status': 'error',
                'error': f"Harvester '{harvester_type}' not found or not enabled"
            }

        logger.info(f"Running {harvester_type} harvester (force={force})")
        harvester = self.harvesters[harvester_type]
        result = harvester.harvest(force=force)

        return result

    def harvest_all(self, force: bool = False) -> Dict[str, Any]:
        """
        Run all enabled harvesters.

        Args:
            force: Force fresh harvest for all

        Returns:
            Dict with results for each harvester
        """
        results = {}

        for harvester_type in self.harvesters:
            logger.info(f"Running {harvester_type} harvester...")
            results[harvester_type] = self.harvest(harvester_type, force=force)

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get status of all harvesters."""
        status = {
            'harvesters': list(self.harvesters.keys()),
            'database': {
                'path': self.db.db_path,
                'data_counts': {}
            },
            'statistics': {}
        }

        # Get data counts
        for harvester_type in self.harvesters:
            count = self.db.get_data_count(f"{harvester_type}_harvester")
            status['database']['data_counts'][harvester_type] = count

        # Get harvest statistics
        status['statistics'] = self.db.get_harvest_stats()

        return status

    def cleanup(self, days: int = 30) -> Dict[str, Any]:
        """Cleanup old data."""
        deleted_count = self.db.cleanup_old_data(days=days)
        self.db.vacuum_database()

        return {
            'status': 'success',
            'deleted_records': deleted_count,
            'cleanup_days': days
        }

# ============================================================
# CLI INTERFACE
# ============================================================

def cli_harvest(args):
    """CLI: Harvest command."""
    harvester = UniversalHarvester()

    if args.type == 'all':
        results = harvester.harvest_all(force=args.force)
        print(json.dumps(results, indent=2))
    else:
        result = harvester.harvest(args.type, force=args.force)
        print(json.dumps(result, indent=2))

def cli_status(args):
    """CLI: Status command."""
    harvester = UniversalHarvester()
    status = harvester.get_status()
    print(json.dumps(status, indent=2))

def cli_cleanup(args):
    """CLI: Cleanup command."""
    harvester = UniversalHarvester()
    result = harvester.cleanup(days=args.days)
    print(json.dumps(result, indent=2))

def cli_analyze(args):
    """CLI: Analyze command."""
    harvester = UniversalHarvester()
    db = harvester.db

    # Get latest data
    data = db.get_latest_data(f"{args.type}_harvester", limit=100, max_age_hours=24)

    if not data:
        print(f"No data found for {args.type}")
        return

    print(f"Found {len(data)} items for {args.type}")
    print(json.dumps(data[:5], indent=2))  # Show first 5

# ============================================================
# HTTP SERVER
# ============================================================

app = Flask(__name__)
harvester_instance = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'universal-harvester'})

@app.route('/harvest', methods=['POST'])
def api_harvest():
    """Harvest endpoint."""
    data = request.get_json() or {}
    harvester_type = data.get('type', 'all')
    force = data.get('force', False)

    if harvester_type == 'all':
        result = harvester_instance.harvest_all(force=force)
    else:
        result = harvester_instance.harvest(harvester_type, force=force)

    return jsonify(result)

@app.route('/data/<source_type>', methods=['GET'])
def api_get_data(source_type):
    """Get harvested data endpoint."""
    limit = request.args.get('limit', 100, type=int)
    max_age_hours = request.args.get('max_age_hours', 24, type=int)
    min_score = request.args.get('min_score', None, type=float)

    db = harvester_instance.db

    if min_score:
        data = db.get_by_quality(f"{source_type}_harvester", min_score=min_score, limit=limit)
    else:
        data = db.get_latest_data(f"{source_type}_harvester", limit=limit, max_age_hours=max_age_hours)

    return jsonify({
        'source_type': source_type,
        'count': len(data),
        'data': data
    })

@app.route('/stats', methods=['GET'])
def api_stats():
    """Statistics endpoint."""
    status = harvester_instance.get_status()
    return jsonify(status)

@app.route('/cleanup', methods=['POST'])
def api_cleanup():
    """Cleanup endpoint."""
    data = request.get_json() or {}
    days = data.get('days', 30)

    result = harvester_instance.cleanup(days=days)
    return jsonify(result)

def serve(port: int = 5003):
    """Start HTTP server."""
    global harvester_instance
    harvester_instance = UniversalHarvester()

    logger.info(f"Starting Universal Harvester server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Universal Harvester - Data Collection System')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Harvest command
    harvest_parser = subparsers.add_parser('harvest', help='Run harvester')
    harvest_parser.add_argument('--type', default='all',
                               choices=['all', 'trend', 'audio', 'screenplay', 'creator', 'distribution', 'sound'],
                               help='Harvester type to run')
    harvest_parser.add_argument('--force', action='store_true', help='Force fresh harvest (bypass cache)')
    harvest_parser.set_defaults(func=cli_harvest)

    # Status command
    status_parser = subparsers.add_parser('status', help='Show harvester status')
    status_parser.set_defaults(func=cli_status)

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze harvested data')
    analyze_parser.add_argument('--type', required=True,
                               choices=['trend', 'audio', 'screenplay', 'creator', 'distribution', 'sound'],
                               help='Data type to analyze')
    analyze_parser.set_defaults(func=cli_analyze)

    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup old data')
    cleanup_parser.add_argument('--days', type=int, default=30, help='Delete data older than N days')
    cleanup_parser.set_defaults(func=cli_cleanup)

    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Start HTTP server')
    serve_parser.add_argument('--port', type=int, default=5003, help='Server port')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'serve':
        serve(port=args.port)
    else:
        args.func(args)

if __name__ == '__main__':
    main()