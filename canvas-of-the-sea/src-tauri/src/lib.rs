use std::{fs, thread};
use std::process::Command;
use serde_json::Value;
use tauri::{Manager};

#[tauri::command]
fn run_exe(path: String) {
    // 使用系统命令启动 EXE 文件，并在新线程中执行
    thread::spawn(move || {
        let output = Command::new("cmd")
            .args(&["/C", "start", "", &path])
            .output()
            .expect("Failed to execute command");

        if !output.status.success() {
            eprintln!("Failed to run EXE: {:?}", output);
        }
    });
}
#[tauri::command]
async fn get_app_path(app_handle: tauri::AppHandle) -> Result<String, String> {
    let resource_dir = app_handle
        .path()
        .resource_dir()
        .map_err(|e| e.to_string())?;
    let resource_path_str = resource_dir.display().to_string();
    // 修复：正确处理Option类型并返回Result
    let resources_path = resource_path_str
        .get(4..resource_path_str.len())
        .ok_or_else(|| "Failed to extract resource path".to_string())?
        .to_string();

    Ok(resources_path)
}

#[tauri::command]
fn read_json_file(file_path: String) -> Result<Value, String> {
    let content = fs::read_to_string(file_path).map_err(|e| e.to_string())?;
    let json: Value = serde_json::from_str(&content).map_err(|e| e.to_string())?;
    Ok(json)
}
#[tauri::command]
fn write_json_file(file_path: String, data: Value) -> Result<(), String> {
    let content = serde_json::to_string_pretty(&data).map_err(|e| e.to_string())?;
    fs::write(file_path, content).map_err(|e| e.to_string())?;
    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            run_exe,              // 运行exe
            get_app_path,         // 获取app路径
            read_json_file,       // 读取json文件
            write_json_file,      // 读取json文件

        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
