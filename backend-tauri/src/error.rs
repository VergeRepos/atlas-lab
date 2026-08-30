use thiserror::Error;
use tauri::plugin::Builder as TauriPluginBuilder;

#[derive(Debug, Error)]
pub enum AtlasError {
    #[error("Database error: {0}")]
    Database(String),

    #[error("File operation error: {0}")]
    FileOperation(String),

    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Unauthorized: {0}")]
    Unauthorized(String),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),

    #[error("UUID error: {0}")]
    Uuid(#[from] uuid::Error),
}

impl From<AtlasError> for tauri::Error {
    fn from(err: AtlasError) -> Self {
        tauri::Error::Api {
            api: "AtlasLab".into(),
            error: format!("{}", err),
        }
    }
}

// Helper function to create error result
pub fn error_result<T>(err: AtlasError) -> Result<T, AtlasError> {
    Err(err)
}