// Atlas Lab Tauri Backend (Rust)
// Handles database, file management, system monitoring, and Tauri commands

#![cfg_attr(
  feature = "custom-protocol",
  allow(leaked_lifetimes) // Remove when Tauri 2.0 stable supports it
)]

use std::sync::Mutex;
use tauri::{Manager, Runtime};

mod commands;
mod database;
mod error;
mod file_manager;
mod system_monitor;

pub use error::AtlasError;
pub use database::Database;

#[derive(Default)]
struct AtlasState {
  database: Mutex<Database>,
}

fn main() {
  // Setup logging
  env_logger::init();

  // Initialize database
  let database = Database::new().expect("Failed to initialize database");
  let state = AtlasState {
    database: Mutex::new(database),
  };

  tauri::Builder::<tauri::Wry>::default()
    .manage(state)
    .invoke_handler(tauri::generate_handler![
      commands::health_check,
      commands::get_system_status,
      commands::query_database,
      commands::create_project,
      commands::read_file_content,
      commands::write_file_content,
      commands::list_documents,
      commands::get_document_metadata,
    ])
    .run(tauri::generate_context!())
    .expect("error running tauri application");
}

#[cfg(test)]
mod tests {
  use super::*;
  use database::Database;

  #[test]
  fn test_database_initialization() {
    let db = Database::new();
    assert!(db.is_ok(), "Database should initialize successfully");
  }

  #[test]
  fn test_health_check() {
    let result = commands::health_check();
    assert_eq!(result.status, "healthy");
    assert_eq!(result.service, "atlas-lab-rust-backend");
  }
}