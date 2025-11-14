#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Module for Production Dashboard
Handles SQLite database operations for metrics, events, training sessions, and system health
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import os

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'dashboard.db')


class Database:
    """SQLite database handler for dashboard metrics"""

    def __init__(self, db_path: str = DB_PATH):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Table: metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    agent_id TEXT,
                    metric_type TEXT NOT NULL,
                    value REAL NOT NULL,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table: events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    agent_id TEXT,
                    message TEXT NOT NULL,
                    severity TEXT DEFAULT 'info',
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table: training_sessions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    agents_trained INTEGER DEFAULT 0,
                    overall_improvement REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'running',
                    phase TEXT,
                    error_message TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table: system_health
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    cpu_percent REAL,
                    memory_percent REAL,
                    disk_percent REAL,
                    uptime_seconds INTEGER,
                    active_connections INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table: agent_metrics (detailed per-agent tracking)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    quality_score REAL DEFAULT 0.0,
                    processing_time_ms INTEGER DEFAULT 0,
                    error_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'online',
                    improvement REAL DEFAULT 0.0,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_agent ON metrics(agent_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_training_start ON training_sessions(start_time)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent ON agent_metrics(agent_id)")

            conn.commit()
            logger.info(f"[Database] Initialized successfully: {self.db_path}")

        except Exception as e:
            logger.error(f"[Database] Initialization failed: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()

    # ========== METRICS OPERATIONS ==========

    def save_metric(self, agent_id: Optional[str], metric_type: str, value: float,
                   notes: Optional[str] = None, timestamp: Optional[str] = None) -> int:
        """
        Save a metric to database

        Args:
            agent_id: Agent identifier (None for system metrics)
            metric_type: Type of metric (quality, speed, errors, etc.)
            value: Metric value
            notes: Optional notes
            timestamp: ISO timestamp (defaults to now)

        Returns:
            Metric ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            ts = timestamp or datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO metrics (timestamp, agent_id, metric_type, value, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (ts, agent_id, metric_type, value, notes))

            conn.commit()
            metric_id = cursor.lastrowid
            logger.debug(f"[Database] Saved metric: {metric_type}={value} for {agent_id or 'system'}")
            return metric_id

        except Exception as e:
            logger.error(f"[Database] Failed to save metric: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_metrics_history(self, metric_type: str, agent_id: Optional[str] = None,
                           limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get metrics history

        Args:
            metric_type: Type of metric to retrieve
            agent_id: Filter by agent (None for all agents)
            limit: Maximum number of records

        Returns:
            List of metric records
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if agent_id:
                cursor.execute("""
                    SELECT * FROM metrics
                    WHERE metric_type = ? AND agent_id = ?
                    ORDER BY timestamp DESC LIMIT ?
                """, (metric_type, agent_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM metrics
                    WHERE metric_type = ?
                    ORDER BY timestamp DESC LIMIT ?
                """, (metric_type, limit))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"[Database] Failed to get metrics: {str(e)}")
            return []
        finally:
            conn.close()

    # ========== EVENTS OPERATIONS ==========

    def save_event(self, event_type: str, message: str, agent_id: Optional[str] = None,
                  severity: str = 'info', metadata: Optional[Dict] = None,
                  timestamp: Optional[str] = None) -> int:
        """
        Save an event to database

        Args:
            event_type: Type of event (training, error, alert, etc.)
            message: Event message
            agent_id: Related agent (if any)
            severity: Event severity (info, warning, error)
            metadata: Additional metadata as dict
            timestamp: ISO timestamp (defaults to now)

        Returns:
            Event ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            ts = timestamp or datetime.now().isoformat()
            metadata_json = json.dumps(metadata) if metadata else None

            cursor.execute("""
                INSERT INTO events (timestamp, event_type, agent_id, message, severity, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ts, event_type, agent_id, message, severity, metadata_json))

            conn.commit()
            event_id = cursor.lastrowid
            logger.debug(f"[Database] Saved event: {event_type} - {message}")
            return event_id

        except Exception as e:
            logger.error(f"[Database] Failed to save event: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_recent_events(self, limit: int = 50, event_type: Optional[str] = None,
                         severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recent events

        Args:
            limit: Maximum number of events
            event_type: Filter by event type
            severity: Filter by severity

        Returns:
            List of event records
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM events WHERE 1=1"
            params = []

            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)

            if severity:
                query += " AND severity = ?"
                params.append(severity)

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            events = []
            for row in rows:
                event = dict(row)
                if event.get('metadata'):
                    try:
                        event['metadata'] = json.loads(event['metadata'])
                    except:
                        pass
                events.append(event)

            return events

        except Exception as e:
            logger.error(f"[Database] Failed to get events: {str(e)}")
            return []
        finally:
            conn.close()

    # ========== TRAINING SESSIONS ==========

    def create_training_session(self, phase: str = 'harvesting') -> int:
        """
        Create a new training session

        Args:
            phase: Initial phase of training

        Returns:
            Session ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            start_time = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO training_sessions (start_time, status, phase)
                VALUES (?, 'running', ?)
            """, (start_time, phase))

            conn.commit()
            session_id = cursor.lastrowid
            logger.info(f"[Database] Created training session: {session_id}")
            return session_id

        except Exception as e:
            logger.error(f"[Database] Failed to create training session: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def update_training_session(self, session_id: int, agents_trained: Optional[int] = None,
                               overall_improvement: Optional[float] = None,
                               status: Optional[str] = None, phase: Optional[str] = None,
                               error_message: Optional[str] = None) -> bool:
        """
        Update training session

        Args:
            session_id: Session ID to update
            agents_trained: Number of agents trained
            overall_improvement: Overall improvement percentage
            status: Session status
            phase: Current phase
            error_message: Error message if failed

        Returns:
            Success status
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            updates = []
            params = []

            if agents_trained is not None:
                updates.append("agents_trained = ?")
                params.append(agents_trained)

            if overall_improvement is not None:
                updates.append("overall_improvement = ?")
                params.append(overall_improvement)

            if status:
                updates.append("status = ?")
                params.append(status)
                if status in ['completed', 'failed']:
                    updates.append("end_time = ?")
                    params.append(datetime.now().isoformat())

            if phase:
                updates.append("phase = ?")
                params.append(phase)

            if error_message:
                updates.append("error_message = ?")
                params.append(error_message)

            if not updates:
                return True

            params.append(session_id)
            query = f"UPDATE training_sessions SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, params)
            conn.commit()

            logger.debug(f"[Database] Updated training session: {session_id}")
            return True

        except Exception as e:
            logger.error(f"[Database] Failed to update training session: {str(e)}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_training_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent training sessions"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM training_sessions
                ORDER BY start_time DESC LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"[Database] Failed to get training sessions: {str(e)}")
            return []
        finally:
            conn.close()

    # ========== SYSTEM HEALTH ==========

    def save_system_health(self, cpu: float, memory: float, disk: float,
                          uptime: int, connections: int = 0) -> int:
        """Save system health snapshot"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            timestamp = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO system_health
                (timestamp, cpu_percent, memory_percent, disk_percent, uptime_seconds, active_connections)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, cpu, memory, disk, uptime, connections))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            logger.error(f"[Database] Failed to save system health: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_system_health_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get system health history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM system_health
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"[Database] Failed to get system health: {str(e)}")
            return []
        finally:
            conn.close()

    # ========== AGENT METRICS ==========

    def save_agent_metrics(self, agent_id: str, quality_score: float,
                          processing_time_ms: int, error_count: int = 0,
                          status: str = 'online', improvement: float = 0.0,
                          metadata: Optional[Dict] = None) -> int:
        """Save agent metrics snapshot"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            timestamp = datetime.now().isoformat()
            metadata_json = json.dumps(metadata) if metadata else None

            cursor.execute("""
                INSERT INTO agent_metrics
                (timestamp, agent_id, quality_score, processing_time_ms, error_count, status, improvement, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (timestamp, agent_id, quality_score, processing_time_ms, error_count, status, improvement, metadata_json))

            conn.commit()
            return cursor.lastrowid

        except Exception as e:
            logger.error(f"[Database] Failed to save agent metrics: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_agent_metrics_history(self, agent_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get agent metrics history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM agent_metrics
                WHERE agent_id = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (agent_id, limit))

            rows = cursor.fetchall()
            metrics = []
            for row in rows:
                metric = dict(row)
                if metric.get('metadata'):
                    try:
                        metric['metadata'] = json.loads(metric['metadata'])
                    except:
                        pass
                metrics.append(metric)

            return metrics

        except Exception as e:
            logger.error(f"[Database] Failed to get agent metrics: {str(e)}")
            return []
        finally:
            conn.close()

    # ========== UTILITY ==========

    def cleanup_old_data(self, days: int = 30):
        """
        Cleanup data older than specified days

        Args:
            days: Keep data from last N days
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
            cutoff_str = cutoff_date.isoformat()

            tables = ['metrics', 'events', 'system_health', 'agent_metrics']
            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE timestamp < ?", (cutoff_str,))

            conn.commit()
            logger.info(f"[Database] Cleaned up data older than {days} days")

        except Exception as e:
            logger.error(f"[Database] Cleanup failed: {str(e)}")
            conn.rollback()
        finally:
            conn.close()

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            stats = {}

            # Count records in each table
            for table in ['metrics', 'events', 'training_sessions', 'system_health', 'agent_metrics']:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                stats[f'{table}_count'] = cursor.fetchone()['count']

            return stats

        except Exception as e:
            logger.error(f"[Database] Failed to get statistics: {str(e)}")
            return {}
        finally:
            conn.close()


# Singleton instance
_db_instance = None

def get_db() -> Database:
    """Get database singleton instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
