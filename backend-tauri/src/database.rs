use anyhow::Result;
use chrono::{DateTime, Utc};
use directories::ProjectDirs;
use log::{info, warn};
use rusqlite::{params, Connection, OpenFlags, Row, TransactionBehavior};
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use uuid::Uuid;

#[derive(Debug, Serialize, Deserialize)]
pub struct Project {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
    pub research_question: Option<String>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub status: String,
    pub tags: String, // JSON array
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Document {
    pub id: String,
    pub project_id: Option<String>,
    pub filename: String,
    pub file_path: String,
    pub file_type: String,
    pub file_size: u64,
    pub title: Option<String>,
    pub author: Option<String>,
    pub created_at: DateTime<Utc>,
    pub processed_at: Option<DateTime<Utc>>,
    pub status: String,
    pub error: Option<String>,
    pub page_count: Option<i32>,
    pub word_count: Option<i32>,
    pub checksum: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Experiment {
    pub id: String,
    pub project_id: String,
    pub name: String,
    pub description: Option<String>,
    pub hypothesis: Option<String>,
    pub status: String,
    pub created_at: DateTime<Utc>,
    pub started_at: Option<DateTime<Utc>>,
    pub completed_at: Option<DateTime<Utc>>,
    pub parameters: String, // JSON
    pub random_seed: Option<i64>,
    pub environment: String, // JSON
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Dataset {
    pub id: String,
    pub project_id: String,
    pub name: String,
    pub description: Option<String>,
    pub file_path: String,
    pub file_type: String,
    pub row_count: i64,
    pub column_count: i32,
    pub columns: String, // JSON array
    pub created_at: DateTime<Utc>,
    pub checksum: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Flashcard {
    pub id: String,
    pub deck_id: String,
    pub front: String,
    pub back: String,
    pub source_note_id: Option<String>,
    pub tags: String, // JSON array
    pub difficulty: f64,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Citation {
    pub id: String,
    pub source_id: String,
    pub authors: String, // JSON array
    pub title: String,
    pub year: Option<i32>,
    pub doi: Option<String>,
    pub url: Option<String>,
    pub citation_type: String, // e.g., "article", "book"
    pub metadata: String, // JSON
}

pub struct Database {
    connection: Mutex<Connection>,
}

impl Database {
    pub fn new() -> Result<Self> {
        let dirs = ProjectDirs::from("com", "atlaslab", "atlas-lab")
            .expect("Failed to get project directories");

        let data_dir = dirs.data_dir();
        std::fs::create_dir_all(data_dir)?;

        let db_path = data_dir.join("atlas_lab.db");
        info!("Initializing database at: {:?}", db_path);

        let conn = Connection::open_with_flags(
            &db_path,
            OpenFlags::SQLITE_OPEN_READ_WRITE | OpenFlags::SQLITE_OPEN_CREATE,
        )?;

        // Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON", [])?;

        // Initialize schema
        Self::initialize_schema(&conn)?;

        Ok(Self {
            connection: Mutex::new(conn),
        })
    }

    fn initialize_schema(conn: &Connection) -> Result<()> {
        let tx = conn.transaction_with_behavior(TransactionBehavior::Immediate)?;

        // Projects table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                research_question TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status TEXT NOT NULL,
                tags TEXT
            )",
            [],
        )?;

        // Documents table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                title TEXT,
                author TEXT,
                created_at TEXT NOT NULL,
                processed_at TEXT,
                status TEXT NOT NULL,
                error TEXT,
                page_count INTEGER,
                word_count INTEGER,
                checksum TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
            )",
            [],
        )?;

        // Experiments table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS experiments (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                hypothesis TEXT,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                parameters TEXT,
                random_seed INTEGER,
                environment TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )",
            [],
        )?;

        // Datasets table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS datasets (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                row_count INTEGER NOT NULL,
                column_count INTEGER NOT NULL,
                columns TEXT,
                created_at TEXT NOT NULL,
                checksum TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )",
            [],
        )?;

        // Flashcards table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS flashcards (
                id TEXT PRIMARY KEY,
                deck_id TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                source_note_id TEXT,
                tags TEXT,
                difficulty REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )",
            [],
        )?;

        // Citations table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS citations (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                authors TEXT,
                title TEXT NOT NULL,
                year INTEGER,
                doi TEXT,
                url TEXT,
                citation_type TEXT,
                metadata TEXT
            )",
            [],
        )?;

        // Knowledge graph nodes table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS knowledge_nodes (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                label TEXT NOT NULL,
                description TEXT,
                properties TEXT,
                x REAL,
                y REAL
            )",
            [],
        )?;

        // Knowledge graph edges table
        tx.execute(
            "CREATE TABLE IF NOT EXISTS knowledge_edges (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship TEXT NOT NULL,
                weight REAL NOT NULL DEFAULT 1.0,
                properties TEXT,
                FOREIGN KEY (source_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
                FOREIGN KEY (target_id) REFERENCES knowledge_nodes(id) ON DELETE CASCADE
            )",
            [],
        )?;

        // Indexes for better performance
        tx.execute("CREATE INDEX IF NOT EXISTS idx_documents_project_id ON documents(project_id)", [])?;
        tx.execute("CREATE INDEX IF NOT EXISTS idx_experiments_project_id ON experiments(project_id)", [])?;
        tx.execute("CREATE INDEX IF NOT EXISTS idx_datasets_project_id ON datasets(project_id)", [])?;
        tx.execute("CREATE INDEX IF NOT EXISTS idx_flashcards_deck_id ON flashcards(deck_id)", [])?;
        tx.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_nodes_type ON knowledge_nodes(type)", [])?;
        tx.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_edges_source ON knowledge_edges(source_id)", [])?;
        tx.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_edges_target ON knowledge_edges(target_id)", [])?;

        tx.commit()?;
        Ok(())
    }

    // Project CRUD operations
    pub fn create_project(&self, project: Project) -> Result<()> {
        let conn = self.connection.lock().unwrap();
        conn.execute(
            "INSERT INTO projects (id, name, description, research_question, created_at, updated_at, status, tags)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)",
            params![
                project.id,
                project.name,
                project.description,
                project.research_question,
                project.created_at.to_rfc3339(),
                project.updated_at.to_rfc3339(),
                project.status,
                project.tags
            ],
        )?;
        Ok(())
    }

    pub fn get_projects(&self) -> Result<Vec<Project>> {
        let conn = self.connection.lock().unwrap();
        let mut stmt = conn.prepare(
            "SELECT id, name, description, research_question, created_at, updated_at, status, tags
             FROM projects
             ORDER BY updated_at DESC"
        )?;

        let projects = stmt.query_map([], |row| {
            Ok(Project {
                id: row.get(0)?,
                name: row.get(1)?,
                description: row.get(2)?,
                research_question: row.get(3)?,
                created_at: DateTime::parse_from_rfc3339(&row.get::<_, String>(4)?)
                    .unwrap()
                    .with_timezone(&Utc),
                updated_at: DateTime::parse_from_rfc3339(&row.get::<_, String>(5)?)
                    .unwrap()
                    .with_timezone(&Utc),
                status: row.get(6)?,
                tags: row.get(7)?,
            })
        })?.collect::<Result<Vec<_>, _>>()?;

        Ok(projects)
    }

    pub fn get_project(&self, id: &str) -> Result<Option<Project>> {
        let conn = self.connection.lock().unwrap();
        let mut stmt = conn.prepare(
            "SELECT id, name, description, research_question, created_at, updated_at, status, tags
             FROM projects
             WHERE id = ?1"
        )?;

        let project = stmt.query_row(params![id], |row| {
            Ok(Project {
                id: row.get(0)?,
                name: row.get(1)?,
                description: row.get(2)?,
                research_question: row.get(3)?,
                created_at: DateTime::parse_from_rfc3339(&row.get::<_, String>(4)?)
                    .unwrap()
                    .with_timezone(&Utc),
                updated_at: DateTime::parse_from_rfc3339(&row.get::<_, String>(5)?)
                    .unwrap()
                    .with_timezone(&Utc),
                status: row.get(6)?,
                tags: row.get(7)?,
            })
        }).optional()?;

        Ok(project)
    }

    // Document operations
    pub fn create_document(&self, document: Document) -> Result<()> {
        let conn = self.connection.lock().unwrap();
        conn.execute(
            "INSERT INTO documents (
                id, project_id, filename, file_path, file_type, file_size, title, author,
                created_at, processed_at, status, error, page_count, word_count, checksum
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15)",
            params![
                document.id,
                document.project_id,
                document.filename,
                document.file_path,
                document.file_type,
                document.file_size,
                document.title,
                document.author,
                document.created_at.to_rfc3339(),
                document.processed_at.map(|dt| dt.to_rfc3339()),
                document.status,
                document.error,
                document.page_count,
                document.word_count,
                document.checksum
            ],
        )?;
        Ok(())
    }

    pub fn get_documents(&self, project_id: Option<&str>) -> Result<Vec<Document>> {
        let conn = self.connection.lock().unwrap();
        let mut stmt = if let Some(pid) = project_id {
            conn.prepare(
                "SELECT id, project_id, filename, file_path, file_type, file_size, title, author,
                        created_at, processed_at, status, error, page_count, word_count, checksum
                 FROM documents
                 WHERE project_id = ?1
                 ORDER BY created_at DESC"
            )?
        } else {
            conn.prepare(
                "SELECT id, project_id, filename, file_path, file_type, file_size, title, author,
                        created_at, processed_at, status, error, page_count, word_count, checksum
                 FROM documents
                 ORDER BY created_at DESC"
            )?
        };

        let documents = match project_id {
            Some(pid) => stmt.query_map(params![pid], Self::document_from_row)?,
            None => stmt.query_map([], Self::document_from_row)?,
        };

        let mut result = Vec::new();
        for doc in documents {
            result.push(doc?);
        }
        Ok(result)
    }

    fn document_from_row(row: &Row) -> Result<Document> {
        Ok(Document {
            id: row.get(0)?,
            project_id: row.get(1)?,
            filename: row.get(2)?,
            file_path: row.get(3)?,
            file_type: row.get(4)?,
            file_size: row.get(5)?,
            title: row.get(6)?,
            author: row.get(7)?,
            created_at: DateTime::parse_from_rfc3339(&row.get::<_, String>(8)?)
                .unwrap()
                .with_timezone(&Utc),
            processed_at: row.get::<_, Option<String>>(9)?.map(|dt| {
                DateTime::parse_from_rfc3339(&dt).unwrap().with_timezone(&Utc)
            }),
            status: row.get(10)?,
            error: row.get(11)?,
            page_count: row.get(12)?,
            word_count: row.get(13)?,
            checksum: row.get(14)?,
        })
    }

    // Experiment operations
    pub fn create_experiment(&self, experiment: Experiment) -> Result<()> {
        let conn = self.connection.lock().unwrap();
        conn.execute(
            "INSERT INTO experiments (
                id, project_id, name, description, hypothesis, status, created_at,
                started_at, completed_at, parameters, random_seed, environment
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12)",
            params![
                experiment.id,
                experiment.project_id,
                experiment.name,
                experiment.description,
                experiment.hypothesis,
                experiment.status,
                experiment.created_at.to_rfc3339(),
                experiment.started_at.map(|dt| dt.to_rfc3339()),
                experiment.completed_at.map(|dt| dt.to_rfc3339()),
                experiment.parameters,
                experiment.random_seed,
                experiment.environment
            ],
        )?;
        Ok(())
    }

    // Health check
    pub fn health_check(&self) -> Result<bool> {
        let conn = self.connection.lock().unwrap();
        let result: i32 = conn.query_row("SELECT 1", [], |row| row.get(0))?;
        Ok(result == 1)
    }
}