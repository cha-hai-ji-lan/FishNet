//!
//! 事件发送模块
//!
//! canvas of the sea 事件构成有  服务端启动链接中事件 链接完成运行时事件 结束运行后事件
//!
//! ---
//!
//! 服务端启动链接中事件 : cli-connect
//!
//! 链接完成运行时事件: cli-exe
//!
//! 结束运行后事件 : cli-end
//!
use once_cell::sync::OnceCell;
use std::sync::Arc;
use tauri::AppHandle;
use tauri::Emitter;

static APP_HANDLE: OnceCell<Arc<AppHandle>> = OnceCell::new(); // app handle全局实例

///
/// ### 设置app handle
///
/// 用于后续rust向typeScript发送事件
pub fn set_app_handle(handle: AppHandle) {
    let _ = APP_HANDLE.set(Arc::new(handle));
}

///
/// ### 获取app handle
///
/// 用于事件获取软件运行句柄
pub fn get_app_handle() -> Result<&'static Arc<AppHandle>, &'static str> {
    APP_HANDLE.get().ok_or("AppHandle not initialized")
}

// 定义事件负载数据结构
#[derive(Clone, serde::Serialize)]
pub struct SomePayload {
    pub data: String,
}

///
/// ### 服务端启动事件
///
/// cli-connect
///
/// 用于在前端提示开始连接CAD实例
pub fn send_run_cli_event(app: &AppHandle) {
    app.emit(
        "cli-connect",
        SomePayload {
            data: "开始启动AutoCAD FishNet Core Sever Tool请稍后...".to_string(),
        },
    )
    .unwrap();
}///
/// ### 发送开始链接CAD实例事件
///
/// cli-connect
///
/// 用于在前端提示开始连接CAD实例
pub fn send_start_connect_event(app: &AppHandle) {
    app.emit(
        "start-connect",
        SomePayload {
            data: "开始链接AutoCAD活动实例".to_string(),
        },
    )
    .unwrap();
}
///
/// ### 创建CAD示例事件
///
/// cli-connect
///
pub fn send_create_cad_example_event(app: &AppHandle) {
    app.emit(
        "create-cad-example",
        SomePayload {
            data: "链接AutoCAD失败开始创建AutoCAD实例".to_string(),
        },
    )
    .unwrap();
}
///
/// ### 创建CAD示例失败事件
///
/// cli-connect
///
pub fn send_fail_create_cad_example_event(app: &AppHandle) {
    app.emit(
        "fail-create-cad-example",
        SomePayload {
            data: "AutoCAD实例创建失败...请重启软件".to_string(),
        },
    )
    .unwrap();
}
///
/// ### 链接后端服务失败事件
///
/// cli-connect
///
pub fn send_fail_ready_event(app: &AppHandle) {
    app.emit(
        "fail-ready",
        SomePayload {
            data: "AutoCAD连接无法就绪, 请重启服务端".to_string(),
        },
    )
    .unwrap();
}
///
/// ### CAD已准备就绪事件
///
/// cli-connect
///
pub fn send_cad_ready(app: &AppHandle) {
    app.emit(
        "cad-ready",
        SomePayload {
            data: "AutoCAD 准备就绪".to_string(),
        },
    )
    .unwrap();
}
///
/// ### 横向比例尺为 0 错误事件
///
/// cli-run
///
pub fn send_horizontal_scale_zero_event(app: &AppHandle) {
    app.emit(
        "horizontal-scale-zero",
        SomePayload {
            data: "水平缩放为0,请检查比例尺或重启软件".to_string(),
        },
    )
    .unwrap();
}
