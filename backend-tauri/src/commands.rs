use crate::database::{Database, Document, Experiment, Project};
use crate::error::AtlasError;
use serde::{Deserialize, Serialize};
use std::path::Path;
use std::sync::Mutex;
use tauri::State;

#[derive(Serialize)]
pub struct HealthResponse {
    pub status: String,
    pub service: String,
}

#[tauri::command]
pub async fn health_check() -> Result<HealthResponse, AtlasError> {
    Ok(HealthResponse {
        status: "healthy".to_string(),
        service: "atlas-lab-rust-backend".to_string(),
    })
}

#[tauri::command]
pub async fn get_system_status() -> Result<SystemStatusResponse, AtlasError> {
    // Get system info
    let sys = sysinfo::System::new_all();

    Ok(SystemStatusResponse {
        cpu_usage: sys.global_cpu_usage(),
        memory_total: sys.total_memory(),
        memory_used: sys.used_memory(),
        swap_total: sys.total_swap(),
        swap_used: sys.used_swap(),
        system_name: sys.name(),
        kernel_version: sys.kernel_version(),
        os_version: sys.os_version(),
        host_name: sys.host_name(),
    })
}

#[derive(Serialize)]
pub struct SystemStatusResponse {
    pub cpu_usage: f32,
    pub memory_total: u64,
    pub memory_used: u64,
    pub swap_total: u64,
    pub swap_used: u64,
    pub system_name: Option<String>,
    pub kernel_version: Option<String>,
    pub os_version: Option<String>,
    pub host_name: Option<String>,
}

#[tauri::command]
pub async fn query_database(
    query: String,
    state: State<'_, Mutex<Database>>,
) -> Result<serde_json::Value, AtlasError> {
    let db = state.lock().unwrap();

    // Only allow SELECT queries for safety
    let trimmed = query.trim().to_lowercase();
    if !trimmed.starts_with("select") && !trimmed.starts_with("pragma") {
        return Err(AtlasError::InvalidInput(
            "Only SELECT queries are allowed".to_string(),
        ));
    }

    let conn = db.connection.lock().unwrap();
    let mut stmt = conn.prepare(&query).map_err(|e| AtlasError::Database(e.to_string()))?;

    let column_names: Vec<String> = stmt.column_names().iter().map(|s| s.to_string()).collect();
    let mut results = Vec::new();

    let rows = stmt.query_map([], |row| {
        let mut obj = serde_json::Map::new();
        for (i, name) in column_names.iter().enumerate() {
            let value: serde_json::Value = match row.get_ref(i) {
                Ok(rusqlite::types::ValueRef::Null) => serde_json::Value::Null,
                Ok(rusqlite::types::ValueRef::Integer(i)) => serde_json::Value::Number(i.into()),
                Ok(rusqlite::types::ValueRef::Real(f)) => serde_json::Value::Number(
                    serde_json::Number::from_f64(f).unwrap_or(serde_json::Number::from(0)),
                ),
                Ok(rusqlite::types::ValueRef::Text(s)) => {
                    let text = String::from_utf8_lossy(s).to_string();
                    serde_json::Value::String(text)
                }
                Ok(rusqlite::types::ValueRef::Blob(b)) => {
                    serde_json::Value::String(base64::encode(b))
                }
                Err(e) => serde_json::Value::String(format!("Error: {}", e)),
            };
            obj.insert(name.clone(), value);
        }
        Ok(serde_json::Value::Object(obj))
    }).map_err(|e| AtlasError::Database(e.to_string()))?;

    for row in rows {
        results.push(row.map_err(|e| AtlasError::Database(e.to_string()))?);
    }

    Ok(serde_json::Value::Array(results))
}

#[derive(Deserialize)]
pub struct CreateProjectRequest {
    pub name: String,
    pub description: Option<String>,
    pub research_question: Option<String>,
}

#[tauri::command]
pub async fn create_project(
    request: CreateProjectRequest,
    state: State<'_, Mutex<Database>>,
) -> Result<Project, AtlasError> {
    let db = state.lock().unwrap();

    let now = chrono::Utc::now();
    let project = Project {
        id: uuid::Uuid::new_v4().to_string(),
        name: request.name,
        description: request.description,
        research_question: request.research_question,
        created_at: now,
        updated_at: now,
        status: "active".to_string(),
        tags: "[]".to_string(),
    };

    db.create_project(project.clone())?;
    Ok(project)
}

#[tauri::command]
pub async fn list_documents(
    project_id: Option<String>,
    state: State<'_, Mutex<Database>>,
) -> Result<Vec<Document>, AtlasError> {
    let db = state.lock().unwrap();
    let docs = db.get_documents(project_id.as_deref())?;
    Ok(docs)
}

#[tauri::command]
pub async fn read_file_content(
    path: String,
) -> Result<String, AtlasError> {
    let path = Path::new(&path);

    // Security: ensure path is within allowed directories
    // For now, allow any readable file
    let content = std::fs::read_to_string(path)
        .map_err(|e| AtlasError::FileOperation(e.to_string()))?;

    Ok(content)
}

#[tauri::command]
pub async fn write_file_content(
    path: String,
    content: String,
) -> Result<(), AtlasError> {
    let path = Path::new(&path);

    // Create parent directories if they don't exist
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent)
            .map_err(|e| AtlasError::FileOperation(e.to_string()))?;
    }

    std::fs::write(path, content)
        .map_err(|e| AtlasError::FileOperation(e.to_string()))?;

    Ok(())
}

#[tauri::command]
pub async fn get_document_metadata(
    document_id: String,
    state: State<'_, Mutex<Database>>,
) -> Result<Option<Document>, AtlasError> {
    let db = state.lock().unwrap();
    let docs = db.get_documents(None)?;
    let doc = docs.into_iter().find(|d| d.id == document_id);
    Ok(doc)
}