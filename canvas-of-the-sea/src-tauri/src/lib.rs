mod util;

use crate::util::event::set_app_handle;
use serde_json::Value;
use std::process::Command;
use std::{fs, thread};
use tauri::Manager;
use util::process_client::{init_connect_cli, kill_cad_process, send_params};

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

#[tauri::command]
async fn connect_cad_cli(
    acad_tool_path: String,
    command1: Option<Vec<String>>,
    command2: Option<Vec<String>>,
) -> Result<String, String> {
    let result = init_connect_cli(acad_tool_path, command1, command2);
    match result {
        Ok(_) => Ok("-success".to_string()),
        Err(error) => Err(error.to_string()),
    }
}
#[tauri::command]
async fn send_param_to_cli(command: Vec<String>) -> Result<String, String> {
    let result = send_params(command);
    match result {
        Ok(_) => Ok("-success".to_string()),
        Err(error) => Err(error.to_string()),
    }
}
#[tauri::command]
async fn reset_cli(
    acad_tool_path: String,
    command1: Option<Vec<String>>,
    command2: Option<Vec<String>>,
) -> Result<String, String> {
    let _ = kill_cad_process();
    let result = init_connect_cli(acad_tool_path, command1, command2);
    match result {
        Ok(_) => Ok("-success".to_string()),
        Err(error) => Err(error.to_string()),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            set_app_handle(app.handle().clone());
            Ok(())
        })
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            run_exe,           // 运行exe
            get_app_path,      // 获取app路径
            read_json_file,    // 读取json文件
            write_json_file,   // 写入json文件
            connect_cad_cli,   // 连接CAD_Tool_CLI
            send_param_to_cli, // 发送参数给CAD_Tool_CLI
            reset_cli,         // 杀死CLI链接CAD进程
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
