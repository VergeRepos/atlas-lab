use std::process::{Command, Stdio};
use std::path::Path;

pub fn get_system_status() -> std::collections::HashMap<String, String> {
    let mut result = std::collections::HashMap::new();
    result.insert("service".to_string(), "atlas-lab-rust-file-manager".to_string());
    result.insert("status".to_string(), "healthy".to_string());
    result
}

pub fn read_file_content(path: &str) -> Result<String, String> {
    use std::fs;
    let p = Path::new(path);
    if !p.exists() {
        return Err(format!("File not found: {}", path));
    }
    fs::read_to_string(p).map_err(|e| format!("Read error: {}", e))
}
