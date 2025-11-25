"""
Database models and operations for virtual prototype app
"""

import sqlite3
import aiosqlite
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DATABASE_PATH = Path("virtual_prototype.db")

async def init_database():
    """Initialize the database with required tables"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # FMU table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS fmus (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fmi_version TEXT,
                model_name TEXT,
                guid TEXT,
                description TEXT,
                author TEXT,
                version TEXT,
                generation_tool TEXT,
                supports_co_simulation BOOLEAN DEFAULT FALSE,
                supports_model_exchange BOOLEAN DEFAULT FALSE,
                supports_scheduled_execution BOOLEAN DEFAULT FALSE,
                validation_status TEXT DEFAULT 'unknown',
                metadata TEXT  -- JSON blob for additional data
            )
        """)
        
        # FMU Variables table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS fmu_variables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fmu_id TEXT NOT NULL,
                name TEXT NOT NULL,
                value_reference INTEGER,
                type TEXT,
                causality TEXT,
                variability TEXT,
                description TEXT,
                unit TEXT,
                start_value TEXT,
                min_value REAL,
                max_value REAL,
                dimensions TEXT,  -- JSON array for FMI 3.0 arrays
                FOREIGN KEY (fmu_id) REFERENCES fmus (id) ON DELETE CASCADE
            )
        """)
        
        # SSP Packages table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ssp_packages (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ssp_version TEXT,
                name TEXT,
                description TEXT,
                author TEXT,
                version TEXT,
                validation_status TEXT DEFAULT 'unknown',
                metadata TEXT  -- JSON blob for package data
            )
        """)
        
        # SSP Components table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ssp_components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ssp_id TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                source TEXT,
                description TEXT,
                position_x REAL,
                position_y REAL,
                parameters TEXT,  -- JSON blob
                FOREIGN KEY (ssp_id) REFERENCES ssp_packages (id) ON DELETE CASCADE
            )
        """)
        
        # SSP Connections table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ssp_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ssp_id TEXT NOT NULL,
                start_element TEXT NOT NULL,
                end_element TEXT NOT NULL,
                connection_type TEXT DEFAULT 'signal',
                description TEXT,
                FOREIGN KEY (ssp_id) REFERENCES ssp_packages (id) ON DELETE CASCADE
            )
        """)
        
        # Projects table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                author TEXT,
                fmus TEXT,  -- JSON array of FMU IDs
                ssp_packages TEXT,  -- JSON array of SSP IDs
                configuration TEXT,  -- JSON blob for project config
                metadata TEXT  -- JSON blob for additional data
            )
        """)
        
        # Simulation Results table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS simulation_results (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                fmu_id TEXT,
                start_time REAL,
                stop_time REAL,
                step_size REAL,
                solver TEXT,
                status TEXT,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                result_data TEXT,  -- JSON blob or path to result file
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
                FOREIGN KEY (fmu_id) REFERENCES fmus (id) ON DELETE CASCADE
            )
        """)
        
        await db.commit()
        logger.info("Database initialized successfully")

async def get_db_session():
    """Get database session (for dependency injection)"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        yield db

class DatabaseManager:
    """Database operations manager"""
    
    @staticmethod
    async def store_fmu(fmu_data: Dict[str, Any]) -> str:
        """Store FMU information in database"""
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("""
                INSERT INTO fmus (
                    id, filename, file_path, file_size, fmi_version, model_name,
                    guid, description, author, version, generation_tool,
                    supports_co_simulation, supports_model_exchange, 
                    supports_scheduled_execution, validation_status, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fmu_data['id'], fmu_data['filename'], fmu_data['file_path'],
                fmu_data['file_size'], fmu_data['fmi_version'], fmu_data['model_name'],
                fmu_data['guid'], fmu_data['description'], fmu_data['author'],
                fmu_data['version'], fmu_data['generation_tool'],
                fmu_data['supports_co_simulation'], fmu_data['supports_model_exchange'],
                fmu_data['supports_scheduled_execution'], fmu_data['validation_status'],
                json.dumps(fmu_data.get('metadata', {}))
            ))
            
            # Store variables
            for var in fmu_data.get('variables', []):
                await db.execute("""
                    INSERT INTO fmu_variables (
                        fmu_id, name, value_reference, type, causality, variability,
                        description, unit, start_value, min_value, max_value, dimensions
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fmu_data['id'], var['name'], var['value_reference'], var['type'],
                    var['causality'], var['variability'], var['description'],
                    var['unit'], str(var['start_value']) if var['start_value'] is not None else None,
                    var['min_value'], var['max_value'], 
                    json.dumps(var['dimensions']) if var['dimensions'] else None
                ))
            
            await db.commit()
            return fmu_data['id']
    
    @staticmethod
    async def get_fmu(fmu_id: str) -> Optional[Dict[str, Any]]:
        """Get FMU information from database"""
        async with aiosqlite.connect(DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row
            
            # Get FMU info
            cursor = await db.execute(
                "SELECT * FROM fmus WHERE id = ?", (fmu_id,)
            )
            fmu_row = await cursor.fetchone()
            
            if not fmu_row:
                return None
            
            # Get variables
            cursor = await db.execute(
                "SELECT * FROM fmu_variables WHERE fmu_id = ?", (fmu_id,)
            )
            var_rows = await cursor.fetchall()
            
            # Convert to dict
            fmu_data = dict(fmu_row)
            fmu_data['variables'] = [dict(row) for row in var_rows]
            
            # Parse JSON fields
            if fmu_data['metadata']:
                fmu_data['metadata'] = json.loads(fmu_data['metadata'])
            
            for var in fmu_data['variables']:
                if var['dimensions']:
                    var['dimensions'] = json.loads(var['dimensions'])
            
            return fmu_data
    
    @staticmethod
    async def list_fmus(skip: int = 0, limit: int = 100, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List FMUs with pagination and filtering"""
        async with aiosqlite.connect(DATABASE_PATH) as db:
            db.row_factory = aiosqlite.Row
            
            query = "SELECT * FROM fmus"
            params = []
            
            if filter_type:
                query += " WHERE fmi_version = ?"
                params.append(filter_type)
            
            query += " ORDER BY upload_time DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])
            
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            
            return [dict(row) for row in rows]
    
    @staticmethod
    async def delete_fmu(fmu_id: str) -> bool:
        """Delete FMU from database"""
        async with aiosqlite.connect(DATABASE_PATH) as db:
            cursor = await db.execute("DELETE FROM fmus WHERE id = ?", (fmu_id,))
            await db.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    async def store_ssp_package(ssp_data: Dict[str, Any]) -> str:
        """Store SSP package information in database"""
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("""
                INSERT INTO ssp_packages (
                    id, filename, file_path, file_size, ssp_version, name,
                    description, author, version, validation_status, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ssp_data['id'], ssp_data['filename'], ssp_data['file_path'],
                ssp_data['file_size'], ssp_data['ssp_version'], ssp_data['name'],
                ssp_data['description'], ssp_data['author'], ssp_data['version'],
                ssp_data['validation_status'], json.dumps(ssp_data.get('metadata', {}))
            ))
            
            # Store components
            for comp in ssp_data.get('components', []):
                await db.execute("""
                    INSERT INTO ssp_components (
                        ssp_id, name, type, source, description, position_x, position_y, parameters
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ssp_data['id'], comp['name'], comp['type'], comp['source'],
                    comp['description'], comp.get('position_x'), comp.get('position_y'),
                    json.dumps(comp.get('parameters', {}))
                ))
            
            # Store connections
            for conn in ssp_data.get('connections', []):
                await db.execute("""
                    INSERT INTO ssp_connections (
                        ssp_id, start_element, end_element, connection_type, description
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    ssp_data['id'], conn['start_element'], conn['end_element'],
                    conn['connection_type'], conn['description']
                ))
            
            await db.commit()
            return ssp_data['id']