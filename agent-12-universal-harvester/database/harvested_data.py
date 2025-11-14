"""
Harvested Data Database - Central SQLite Storage

Manages all harvested data from all harvesters in a centralized database.
Provides data persistence, caching, and analytics.

Author: Universal Harvester System
Version: 1.0.0
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
import os

logging.basicConfig(level=logging.INFO)


class HarvestedDataDB:
    """
    Central database for all harvested data.

    Manages storage, retrieval, and cleanup of harvested data
    from all harvesters in the system.
    """

    def __init__(self, db_path: str = "./database/harvested_data.db"):
        """
        Initialize the database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = logging.getLogger("HarvestedDataDB")

        # Create database directory if needed
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Initialize database
        self._init_database()

        self.logger.info(f"Database initialized at: {db_path}")

    def _init_database(self) -> None:
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Table: harvested_data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS harvested_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_type TEXT NOT NULL,
                harvester_name TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                analyzed_data TEXT,
                quality_score REAL,
                source_url TEXT,
                harvested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                UNIQUE(source_type, source_url, harvested_at)
            )
        """)

        # Index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source_type
            ON harvested_data(source_type, harvested_at DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_quality
            ON harvested_data(quality_score DESC)
        """)

        # Table: harvest_log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS harvest_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                harvester_name TEXT NOT NULL,
                status TEXT NOT NULL,
                record_count INTEGER DEFAULT 0,
                execution_time INTEGER,
                error_message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Index for logs
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_harvester_log
            ON harvest_log(harvester_name, timestamp DESC)
        """)

        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    # ============================================================
    # DATA MANAGEMENT
    # ============================================================

    def save_harvested_data(self, harvester_name: str, data: Dict[str, Any],
                           expires_in_days: int = 30) -> int:
        """
        Save harvested data to database.

        Args:
            harvester_name: Name of harvester
            data: Data dict to save
            expires_in_days: Days until data expires

        Returns:
            ID of inserted record
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Calculate expiry
            expires_at = datetime.now() + timedelta(days=expires_in_days)

            # Extract fields
            source_type = harvester_name
            quality_score = data.get('quality_score', 0.0)
            source_url = data.get('source_url', '')

            # Separate raw and analyzed data
            analyzed_data = data.get('gemini_analysis', {})
            raw_data = {k: v for k, v in data.items() if k != 'gemini_analysis'}

            # Insert
            cursor.execute("""
                INSERT OR REPLACE INTO harvested_data
                (source_type, harvester_name, raw_data, analyzed_data,
                 quality_score, source_url, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                source_type,
                harvester_name,
                json.dumps(raw_data),
                json.dumps(analyzed_data),
                quality_score,
                source_url,
                expires_at
            ))

            record_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return record_id

        except Exception as e:
            self.logger.error(f"Failed to save data: {str(e)}")
            raise

    def get_latest_data(self, source_type: str, limit: int = 100,
                       max_age_hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get latest harvested data for a source type.

        Args:
            source_type: Harvester name
            limit: Maximum number of records
            max_age_hours: Maximum age in hours

        Returns:
            List of data dicts
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Calculate time threshold
            time_threshold = datetime.now() - timedelta(hours=max_age_hours)

            cursor.execute("""
                SELECT * FROM harvested_data
                WHERE source_type = ?
                  AND harvested_at > ?
                  AND (expires_at IS NULL OR expires_at > ?)
                ORDER BY harvested_at DESC
                LIMIT ?
            """, (source_type, time_threshold, datetime.now(), limit))

            rows = cursor.fetchall()
            conn.close()

            # Convert to dicts
            results = []
            for row in rows:
                data = json.loads(row['raw_data'])
                if row['analyzed_data']:
                    data['gemini_analysis'] = json.loads(row['analyzed_data'])
                data['quality_score'] = row['quality_score']
                data['harvested_at'] = row['harvested_at']
                results.append(data)

            return results

        except Exception as e:
            self.logger.error(f"Failed to get latest data: {str(e)}")
            return []

    def get_by_quality(self, source_type: str, min_score: float = 7.0,
                      limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get harvested data filtered by quality score.

        Args:
            source_type: Harvester name
            min_score: Minimum quality score
            limit: Maximum number of records

        Returns:
            List of high-quality data dicts
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM harvested_data
                WHERE source_type = ?
                  AND quality_score >= ?
                  AND (expires_at IS NULL OR expires_at > ?)
                ORDER BY quality_score DESC, harvested_at DESC
                LIMIT ?
            """, (source_type, min_score, datetime.now(), limit))

            rows = cursor.fetchall()
            conn.close()

            # Convert to dicts
            results = []
            for row in rows:
                data = json.loads(row['raw_data'])
                if row['analyzed_data']:
                    data['gemini_analysis'] = json.loads(row['analyzed_data'])
                data['quality_score'] = row['quality_score']
                data['harvested_at'] = row['harvested_at']
                results.append(data)

            return results

        except Exception as e:
            self.logger.error(f"Failed to get data by quality: {str(e)}")
            return []

    def cleanup_old_data(self, days: int = 30) -> int:
        """
        Delete data older than specified days or expired.

        Args:
            days: Delete data older than this

        Returns:
            Number of records deleted
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Delete expired data
            cursor.execute("""
                DELETE FROM harvested_data
                WHERE expires_at < ?
            """, (datetime.now(),))

            expired_count = cursor.rowcount

            # Delete old data
            cutoff_date = datetime.now() - timedelta(days=days)
            cursor.execute("""
                DELETE FROM harvested_data
                WHERE harvested_at < ?
            """, (cutoff_date,))

            old_count = cursor.rowcount

            total_deleted = expired_count + old_count
            conn.commit()
            conn.close()

            self.logger.info(f"Cleaned up {total_deleted} old records")
            return total_deleted

        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
            return 0

    # ============================================================
    # HARVEST LOGGING
    # ============================================================

    def log_harvest_event(self, harvester_name: str, status: str,
                         record_count: int, execution_time: int,
                         error_message: str = None) -> int:
        """
        Log a harvest event.

        Args:
            harvester_name: Name of harvester
            status: 'success', 'error', or 'warning'
            record_count: Number of records harvested
            execution_time: Execution time in milliseconds
            error_message: Error message if status='error'

        Returns:
            Log entry ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO harvest_log
                (harvester_name, status, record_count, execution_time, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (harvester_name, status, record_count, execution_time, error_message))

            log_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return log_id

        except Exception as e:
            self.logger.error(f"Failed to log harvest event: {str(e)}")
            return -1

    def get_harvest_stats(self, harvester_name: str = None) -> Dict[str, Any]:
        """
        Get harvest statistics.

        Args:
            harvester_name: Specific harvester (if None, all harvesters)

        Returns:
            Dict with statistics
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Base query
            if harvester_name:
                where_clause = "WHERE harvester_name = ?"
                params = (harvester_name,)
            else:
                where_clause = ""
                params = ()

            # Get stats
            cursor.execute(f"""
                SELECT
                    harvester_name,
                    COUNT(*) as total_runs,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_runs,
                    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as failed_runs,
                    SUM(record_count) as total_records,
                    AVG(execution_time) as avg_execution_time,
                    MAX(timestamp) as last_run
                FROM harvest_log
                {where_clause}
                GROUP BY harvester_name
            """, params)

            rows = cursor.fetchall()
            conn.close()

            # Convert to dict
            stats = {}
            for row in rows:
                stats[row['harvester_name']] = {
                    'total_runs': row['total_runs'],
                    'successful_runs': row['successful_runs'],
                    'failed_runs': row['failed_runs'],
                    'success_rate': (row['successful_runs'] / row['total_runs'] * 100) if row['total_runs'] > 0 else 0,
                    'total_records': row['total_records'],
                    'avg_execution_time_ms': round(row['avg_execution_time'], 2) if row['avg_execution_time'] else 0,
                    'last_run': row['last_run']
                }

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get stats: {str(e)}")
            return {}

    def get_recent_logs(self, harvester_name: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent harvest logs.

        Args:
            harvester_name: Specific harvester (if None, all)
            limit: Maximum number of logs

        Returns:
            List of log entries
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if harvester_name:
                cursor.execute("""
                    SELECT * FROM harvest_log
                    WHERE harvester_name = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (harvester_name, limit))
            else:
                cursor.execute("""
                    SELECT * FROM harvest_log
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))

            rows = cursor.fetchall()
            conn.close()

            # Convert to dicts
            logs = []
            for row in rows:
                logs.append({
                    'id': row['id'],
                    'harvester_name': row['harvester_name'],
                    'status': row['status'],
                    'record_count': row['record_count'],
                    'execution_time': row['execution_time'],
                    'error_message': row['error_message'],
                    'timestamp': row['timestamp']
                })

            return logs

        except Exception as e:
            self.logger.error(f"Failed to get logs: {str(e)}")
            return []

    # ============================================================
    # UTILITY METHODS
    # ============================================================

    def get_data_count(self, source_type: str = None) -> int:
        """
        Get count of harvested data records.

        Args:
            source_type: Specific harvester (if None, all)

        Returns:
            Count of records
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if source_type:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM harvested_data
                    WHERE source_type = ?
                      AND (expires_at IS NULL OR expires_at > ?)
                """, (source_type, datetime.now()))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as count FROM harvested_data
                    WHERE expires_at IS NULL OR expires_at > ?
                """, (datetime.now(),))

            count = cursor.fetchone()['count']
            conn.close()

            return count

        except Exception as e:
            self.logger.error(f"Failed to get count: {str(e)}")
            return 0

    def export_data(self, source_type: str, output_file: str) -> bool:
        """
        Export harvested data to JSON file.

        Args:
            source_type: Harvester name
            output_file: Output file path

        Returns:
            True if successful
        """
        try:
            data = self.get_latest_data(source_type, limit=1000, max_age_hours=24*30)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            self.logger.info(f"Exported {len(data)} records to {output_file}")
            return True

        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return False

    def vacuum_database(self) -> bool:
        """
        Optimize database (VACUUM).

        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            conn.execute("VACUUM")
            conn.close()

            self.logger.info("Database vacuumed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Vacuum failed: {str(e)}")
            return False

    def __repr__(self) -> str:
        return f"<HarvestedDataDB path='{self.db_path}'>"