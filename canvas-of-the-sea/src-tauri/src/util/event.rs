use tauri::Emitter;
use once_cell::sync::OnceCell;
use std::sync::Arc;
use tauri::AppHandle;

static APP_HANDLE: OnceCell<Arc<AppHandle>> = OnceCell::new();  // app handle全局实例

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
/// ### 发送开始链接CAD实例事件
///
/// 用于在前端提示开始连接CAD实例
pub fn send_start_connect_event(app: &AppHandle) {
    app.emit("cli-start-connect", SomePayload {
        data: "start connect cad".to_string()
    }).unwrap();
}