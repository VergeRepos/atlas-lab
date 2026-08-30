use sysinfo::{System, SystemExt, CpuExt, ProcessExt};

#[derive(serde::Serialize, Clone, Debug)]
pub struct SystemInfo {
    pub cpu_usage: f32,
    pub memory_total: u64,
    pub memory_used: u64,
    pub memory_free: u64,
    pub cpu_count: usize,
    pub system_name: String,
    pub kernel_version: String,
    pub os_version: String,
    pub uptime: u64,
}

impl SystemInfo {
    pub fn collect() -> Self {
        let mut sys = System::new_all();
        sys.refresh_all();
        let cpu_usage = sys.global_cpu_info().cpu_usage();
        SystemInfo {
            cpu_usage,
            memory_total: sys.total_memory(),
            memory_used: sys.used_memory(),
            memory_free: sys.free_memory(),
            cpu_count: sys.cpus().len(),
            system_name: sys.name().unwrap_or_default(),
            kernel_version: sys.kernel_version().unwrap_or_default(),
            os_version: sys.os_version().unwrap_or_default(),
            uptime: sys.uptime(),
        }
    }
}
