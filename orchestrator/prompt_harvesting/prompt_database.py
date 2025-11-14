#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prompt Database Module - SQLite Management
Manages persistent storage of harvested and analyzed prompts
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class PromptDatabase:
    """
    SQLite database for prompt storage and retrieval
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'prompt_database.db')

        self.db_path = db_path
        self.conn = None
        self.cursor = None

        self._connect()
        self._create_tables()

        logger.info(f"[Database] Initialized at: {self.db_path}")

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.error(f"[Database] Connection error: {e}")
            raise

    def _create_tables(self):
        """Create database tables if they don't exist"""
        try:
            # Main prompts table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    source_id TEXT,
                    prompt_text TEXT NOT NULL,
                    title TEXT,
                    url TEXT,
                    model_type TEXT,
                    quality_score REAL DEFAULT 0.0,
                    community_score INTEGER DEFAULT 0,
                    gemini_analysis TEXT,
                    patterns TEXT,
                    category TEXT,
                    genre TEXT,
                    upvotes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    views INTEGER DEFAULT 0,
                    harvested_at TEXT NOT NULL,
                    analyzed_at TEXT,
                    used_for_training INTEGER DEFAULT 0,
                    training_iterations INTEGER DEFAULT 0,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Pattern library table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_value TEXT NOT NULL,
                    occurrences INTEGER DEFAULT 1,
                    model_type TEXT,
                    quality_score REAL,
                    extracted_at TEXT NOT NULL,
                    last_updated TEXT,
                    metadata TEXT,
                    UNIQUE(pattern_type, pattern_value, model_type)
                )
            """)

            # Training history table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS training_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id INTEGER,
                    agent_name TEXT NOT NULL,
                    training_date TEXT NOT NULL,
                    iterations INTEGER DEFAULT 1,
                    success INTEGER DEFAULT 1,
                    notes TEXT,
                    FOREIGN KEY (prompt_id) REFERENCES prompts(id)
                )
            """)

            # Create indexes for better performance
            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_quality_score
                ON prompts(quality_score DESC)
            """)

            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_model_type
                ON prompts(model_type)
            """)

            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_source
                ON prompts(source)
            """)

            self.cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_used_training
                ON prompts(used_for_training)
            """)

            self.conn.commit()
            logger.info("[Database] Tables created/verified successfully")

        except Exception as e:
            logger.error(f"[Database] Table creation error: {e}")
            raise

    def save_prompt(self, data: Dict) -> Optional[int]:
        """
        Save a single prompt to database

        Args:
            data: Prompt data dictionary

        Returns:
            Prompt ID if successful, None otherwise
        """
        try:
            # Extract and serialize complex fields
            gemini_analysis = json.dumps(data.get('analysis', {})) if 'analysis' in data else None
            patterns = json.dumps(data.get('patterns', [])) if 'patterns' in data else None
            metadata = json.dumps(data.get('metadata', {})) if 'metadata' in data else None

            # Get prompt text
            prompt_text = ""
            if 'prompts' in data and data['prompts']:
                prompt_text = data['prompts'][0] if isinstance(data['prompts'], list) else data['prompts']
            elif 'text' in data:
                prompt_text = data['text']
            elif 'prompt_text' in data:
                prompt_text = data['prompt_text']

            if not prompt_text:
                logger.warning("[Database] No prompt text found, skipping")
                return None

            # Insert prompt
            self.cursor.execute("""
                INSERT INTO prompts (
                    source, source_id, prompt_text, title, url,
                    model_type, quality_score, community_score,
                    gemini_analysis, patterns, category, genre,
                    upvotes, comments, views, harvested_at,
                    analyzed_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('source', 'unknown'),
                data.get('source_id', ''),
                prompt_text,
                data.get('title', ''),
                data.get('url', ''),
                data.get('model_type', ''),
                data.get('quality_score', 0.0),
                data.get('community_score', 0),
                gemini_analysis,
                patterns,
                data.get('category', ''),
                data.get('genre', ''),
                data.get('upvotes', 0),
                data.get('comments', 0),
                data.get('views', 0),
                data.get('harvested_at', datetime.now().isoformat()),
                data.get('analyzed_at', ''),
                metadata
            ))

            self.conn.commit()
            prompt_id = self.cursor.lastrowid

            logger.info(f"[Database] Saved prompt ID: {prompt_id}")
            return prompt_id

        except sqlite3.IntegrityError as e:
            logger.warning(f"[Database] Duplicate prompt: {e}")
            return None
        except Exception as e:
            logger.error(f"[Database] Save error: {e}")
            return None

    def save_prompts(self, prompts: List[Dict]) -> Tuple[int, int]:
        """
        Save multiple prompts to database

        Args:
            prompts: List of prompt dictionaries

        Returns:
            Tuple of (successful_count, failed_count)
        """
        successful = 0
        failed = 0

        for prompt in prompts:
            prompt_id = self.save_prompt(prompt)
            if prompt_id:
                successful += 1
            else:
                failed += 1

        logger.info(f"[Database] Saved {successful} prompts, {failed} failed")
        return successful, failed

    def get_top_prompts(self, n: int = 100, min_score: float = 7.0,
                        model_type: Optional[str] = None) -> List[Dict]:
        """
        Retrieve top quality prompts

        Args:
            n: Number of prompts to retrieve
            min_score: Minimum quality score
            model_type: Filter by model type (runway, veo, etc.)

        Returns:
            List of prompt dictionaries
        """
        try:
            query = """
                SELECT * FROM prompts
                WHERE quality_score >= ?
            """
            params = [min_score]

            if model_type:
                query += " AND model_type = ?"
                params.append(model_type)

            query += " ORDER BY quality_score DESC, community_score DESC LIMIT ?"
            params.append(n)

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            prompts = []
            for row in rows:
                prompt = dict(row)
                # Deserialize JSON fields
                if prompt['gemini_analysis']:
                    prompt['analysis'] = json.loads(prompt['gemini_analysis'])
                if prompt['patterns']:
                    prompt['patterns'] = json.loads(prompt['patterns'])
                if prompt['metadata']:
                    prompt['metadata'] = json.loads(prompt['metadata'])
                prompts.append(prompt)

            logger.info(f"[Database] Retrieved {len(prompts)} top prompts")
            return prompts

        except Exception as e:
            logger.error(f"[Database] Retrieval error: {e}")
            return []

    def get_patterns_summary(self, model_type: Optional[str] = None,
                             min_occurrences: int = 2) -> Dict:
        """
        Get summary of extracted patterns

        Args:
            model_type: Filter by model type
            min_occurrences: Minimum pattern occurrences

        Returns:
            Dictionary with pattern statistics
        """
        try:
            query = """
                SELECT pattern_type, pattern_value, occurrences,
                       AVG(quality_score) as avg_score
                FROM patterns
                WHERE occurrences >= ?
            """
            params = [min_occurrences]

            if model_type:
                query += " AND model_type = ?"
                params.append(model_type)

            query += " GROUP BY pattern_type ORDER BY occurrences DESC"

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            patterns_by_type = {}
            for row in rows:
                pattern_type = row['pattern_type']
                if pattern_type not in patterns_by_type:
                    patterns_by_type[pattern_type] = []

                patterns_by_type[pattern_type].append({
                    'value': row['pattern_value'],
                    'occurrences': row['occurrences'],
                    'avg_score': round(row['avg_score'], 2) if row['avg_score'] else 0
                })

            summary = {
                'total_patterns': len(rows),
                'patterns_by_type': patterns_by_type,
                'model_type': model_type,
                'retrieved_at': datetime.now().isoformat()
            }

            logger.info(f"[Database] Retrieved {len(rows)} patterns")
            return summary

        except Exception as e:
            logger.error(f"[Database] Pattern retrieval error: {e}")
            return {'error': str(e)}

    def mark_as_trained(self, prompt_id: int, agent_name: str,
                        iterations: int = 1, success: bool = True,
                        notes: Optional[str] = None):
        """
        Mark a prompt as used for training

        Args:
            prompt_id: ID of the prompt
            agent_name: Name of the agent trained
            iterations: Number of training iterations
            success: Whether training was successful
            notes: Optional training notes
        """
        try:
            # Update prompts table
            self.cursor.execute("""
                UPDATE prompts
                SET used_for_training = 1,
                    training_iterations = training_iterations + ?
                WHERE id = ?
            """, (iterations, prompt_id))

            # Insert training history
            self.cursor.execute("""
                INSERT INTO training_history (
                    prompt_id, agent_name, training_date,
                    iterations, success, notes
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                prompt_id,
                agent_name,
                datetime.now().isoformat(),
                iterations,
                1 if success else 0,
                notes
            ))

            self.conn.commit()
            logger.info(f"[Database] Marked prompt {prompt_id} as trained by {agent_name}")

        except Exception as e:
            logger.error(f"[Database] Training mark error: {e}")

    def save_pattern(self, pattern_type: str, pattern_value: str,
                     model_type: Optional[str] = None,
                     quality_score: Optional[float] = None):
        """
        Save or update a pattern in the pattern library

        Args:
            pattern_type: Type of pattern (keyword, structure, etc.)
            pattern_value: The pattern value
            model_type: Associated model type
            quality_score: Quality score of prompt containing pattern
        """
        try:
            # Try to update existing pattern
            self.cursor.execute("""
                UPDATE patterns
                SET occurrences = occurrences + 1,
                    last_updated = ?
                WHERE pattern_type = ? AND pattern_value = ?
                AND (model_type = ? OR model_type IS NULL)
            """, (
                datetime.now().isoformat(),
                pattern_type,
                pattern_value,
                model_type
            ))

            if self.cursor.rowcount == 0:
                # Insert new pattern
                self.cursor.execute("""
                    INSERT INTO patterns (
                        pattern_type, pattern_value, model_type,
                        quality_score, extracted_at, last_updated
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    pattern_type,
                    pattern_value,
                    model_type,
                    quality_score,
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))

            self.conn.commit()

        except Exception as e:
            logger.error(f"[Database] Pattern save error: {e}")

    def get_statistics(self) -> Dict:
        """
        Get database statistics

        Returns:
            Dictionary with database stats
        """
        try:
            stats = {}

            # Total prompts
            self.cursor.execute("SELECT COUNT(*) as count FROM prompts")
            stats['total_prompts'] = self.cursor.fetchone()['count']

            # Prompts by source
            self.cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM prompts
                GROUP BY source
            """)
            stats['by_source'] = {row['source']: row['count'] for row in self.cursor.fetchall()}

            # Prompts by model
            self.cursor.execute("""
                SELECT model_type, COUNT(*) as count
                FROM prompts
                WHERE model_type != ''
                GROUP BY model_type
            """)
            stats['by_model'] = {row['model_type']: row['count'] for row in self.cursor.fetchall()}

            # Quality distribution
            self.cursor.execute("""
                SELECT
                    COUNT(CASE WHEN quality_score >= 8.0 THEN 1 END) as excellent,
                    COUNT(CASE WHEN quality_score >= 6.0 AND quality_score < 8.0 THEN 1 END) as good,
                    COUNT(CASE WHEN quality_score >= 4.0 AND quality_score < 6.0 THEN 1 END) as fair,
                    COUNT(CASE WHEN quality_score < 4.0 THEN 1 END) as poor,
                    AVG(quality_score) as avg_score
                FROM prompts
            """)
            row = self.cursor.fetchone()
            stats['quality'] = {
                'excellent': row['excellent'],
                'good': row['good'],
                'fair': row['fair'],
                'poor': row['poor'],
                'average': round(row['avg_score'], 2) if row['avg_score'] else 0
            }

            # Training usage
            self.cursor.execute("""
                SELECT
                    COUNT(CASE WHEN used_for_training = 1 THEN 1 END) as trained,
                    COUNT(CASE WHEN used_for_training = 0 THEN 1 END) as untrained
                FROM prompts
            """)
            row = self.cursor.fetchone()
            stats['training'] = {
                'trained': row['trained'],
                'untrained': row['untrained']
            }

            # Total patterns
            self.cursor.execute("SELECT COUNT(*) as count FROM patterns")
            stats['total_patterns'] = self.cursor.fetchone()['count']

            return stats

        except Exception as e:
            logger.error(f"[Database] Statistics error: {e}")
            return {'error': str(e)}

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("[Database] Connection closed")


if __name__ == '__main__':
    # Test database
    print("Prompt Database - Test Mode")
    print("="*60)

    db = PromptDatabase()

    # Test save prompt
    test_prompt = {
        'source': 'reddit',
        'prompt_text': 'Cinematic 4K shot of futuristic city',
        'title': 'Test Prompt',
        'url': 'https://reddit.com/test',
        'model_type': 'runway',
        'quality_score': 8.5,
        'upvotes': 100,
        'comments': 20,
        'harvested_at': datetime.now().isoformat()
    }

    print("\nTesting save prompt...")
    prompt_id = db.save_prompt(test_prompt)
    print(f"Saved with ID: {prompt_id}")

    print("\nTesting retrieval...")
    top_prompts = db.get_top_prompts(n=5, min_score=5.0)
    print(f"Retrieved {len(top_prompts)} prompts")

    print("\nTesting statistics...")
    stats = db.get_statistics()
    print(f"Total prompts: {stats.get('total_prompts', 0)}")
    print(f"Quality distribution: {stats.get('quality', {})}")

    db.close()

    print("\n" + "="*60)
