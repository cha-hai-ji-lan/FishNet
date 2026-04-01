use std::io;
use std::io::{BufRead, BufReader, Error, Write};
use std::process::{Child, ChildStderr, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::{Arc, Mutex};
// 事件监听发送器
use crate::util::event::{
    get_app_handle, send_cad_ready, send_create_cad_example_event,
    send_fail_create_cad_example_event, send_fail_ready_event, send_run_cli_event,
    send_start_connect_event,
};

///
/// ### CLI 连接器结构体
///
/// 用于管理主进程与子进程的通信
pub struct CadCliConnector {
    pub child_process: Arc<Mutex<Child>>,
    pub stdin: Arc<Mutex<ChildStdin>>,
    pub reader: Arc<Mutex<BufReader<ChildStdout>>>,
    #[allow(dead_code)]
    pub stderr: Arc<Mutex<BufReader<ChildStderr>>>,
}

///
/// ### 全局 CAD CLI 连接器实例
///
/// 使用 Mutex<Option> 允许后续清除和重新初始化
static CAD_CONNECTOR: Mutex<Option<Arc<CadCliConnector>>> = Mutex::new(None);
static mut START_MONITOR: bool = false;

///
/// ### 获取全局连接器实例
///
/// 返回全局连接器的引用，如果未初始化则返回错误
fn get_connector() -> Result<Arc<CadCliConnector>, Error> {
    let connector = CAD_CONNECTOR.lock().unwrap();
    connector.clone().ok_or_else(|| {
        Error::new(
            io::ErrorKind::NotConnected,
            "CAD CLI 连接器未初始化，请先调用 init_connect_cli()",
        )
    })
}

///
/// ### 等待启动标志
fn wait_for_start(connector: &mut CadCliConnector) -> Result<(), Error> {
    let mut buffer = Vec::new();
    let mut found_start = false;

    loop {
        buffer.clear();
        let bytes_read = connector
            .reader
            .lock()
            .unwrap()
            .read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // 尝试转换为字符串，忽略无效 UTF-8
        if let Ok(line) = String::from_utf8(buffer.clone()) {
            let app_handle = get_app_handle().unwrap();
            println!("{}", line);
            match line.trim() {
                "-start-cad" => send_start_connect_event(&app_handle),
                "-try-crate-cad" => send_create_cad_example_event(&app_handle),
                "-fail-crate-cad" => send_fail_create_cad_example_event(&app_handle),
                "-start" => {
                    println!("获取到 ---start--- 已启动");
                    send_cad_ready(&app_handle);
                    found_start = true;
                    break;
                }
                "-end" => {
                    return Err(Error::new(
                        io::ErrorKind::UnexpectedEof,
                        "-start 丢失".to_string(),
                    ));
                }
                _ => {}
            }
        }
    }

    if !found_start {
        let app_handle = get_app_handle().unwrap();
        send_fail_ready_event(&app_handle);
        return Err(Error::new(
            io::ErrorKind::NotFound,
            "无法找到 -start 起始标志".to_string(),
        ));
    }

    Ok(())
}

///
/// ### 发送初始参数
fn send_initial_params(
    connector: &mut CadCliConnector,
    command1: &str,
    command2: &str,
) -> Result<(), Error> {
    unsafe {
        START_MONITOR = false;
    }
    let mut buffer = Vec::new();
    let mut found_end = false;
    println!("{}{}", command1, command2);
    // 发送命令行参数
    writeln!(connector.stdin.lock().unwrap(), "{}{}", command1, command2)?;

    loop {
        buffer.clear();
        let bytes_read = connector
            .reader
            .lock()
            .unwrap()
            .read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // 尝试转换为字符串，忽略无效 UTF-8
        if let Ok(line) = String::from_utf8(buffer.clone()) {
            println!("{}", line);
            if line.trim() == "-end" {
                found_end = true;
                break;
            }
        }
    }

    if !found_end {
        return Err(Error::new(
            io::ErrorKind::NotFound,
            "未收到 -end 信号".to_string(),
        ));
    }
    unsafe {
        START_MONITOR = true;
    }
    Ok(())
}

///
/// ### 初始化 CAD CLI 连接 (全局单例版本)
///
/// 启动 CAD 工具并建立通信管道，存储到全局变量中
///
/// `acad_tool_path`: 启动的文档处理工具路径
///
/// `args_g1`: 命令行参数组 1 (可选)
///
/// `args_g2`: 命令行参数组 2 (可选)
pub fn init_connect_cli(
    acad_tool_path: String,
    args_g1: Option<Vec<String>>,
    args_g2: Option<Vec<String>>,
) -> Result<(), Error> {
    // 检查是否已经初始化
    let global_connector = CAD_CONNECTOR.lock().unwrap();
    if global_connector.is_some() {
        return Err(Error::new(
            io::ErrorKind::AlreadyExists,
            "CAD CLI 连接器已初始化，无法重复初始化。请先调用 kill_cad_process() 或 close_cli_connection() 清除后再初始化",
        ));
    }
    drop(global_connector); // 释放锁
    let app_handle = get_app_handle().unwrap();
    send_run_cli_event(&app_handle); // 发送运行 CLI 启动事件
    let mut child: Child = Command::new(&acad_tool_path)
        .stdin(Stdio::piped()) // 创建管道捕获 标准输入 [主进程 -> 子进程]
        .stdout(Stdio::piped()) // 创建管道捕获 标准输出 [子进程 -> 主进程]
        .stderr(Stdio::piped()) // 创建管道捕获 错误输出 [子进程 -> 主进程]
        .spawn()?;

    let stdin: ChildStdin = child.stdin.take().unwrap(); // 获取 stdin
    let stdout: ChildStdout = child.stdout.take().unwrap(); // 获取 stdout
    let stderr: ChildStderr = child.stderr.take().unwrap(); // 获取 stderr

    let reader = BufReader::new(stdout); // 读取缓冲区，用于读取字节流
    let stderr_reader = BufReader::new(stderr);
    let mut connector = CadCliConnector {
        child_process: Arc::new(Mutex::new(child)),
        stdin: Arc::new(Mutex::new(stdin)),
        reader: Arc::new(Mutex::new(reader)),
        stderr: Arc::new(Mutex::new(stderr_reader)),
    };

    // 等待 "-start" 标志
    wait_for_start(&mut connector)?;

    // 构建并发送命令行参数
    let mut command1 = String::new();
    let mut command2 = String::new();

    if let Some(ref args) = args_g1 {
        for i in args {
            command1 += &format!("{} ", i);
        }
    }

    if let Some(ref args) = args_g2 {
        for i in args {
            command2 += &format!("{} ", i);
        }
    }

    // 发送初始化参数并等待 "-end" 标志
    send_initial_params(&mut connector, &command1, &command2)?;

    // 存储到全局变量 - Mutex<Option>
    let mut global_connector = CAD_CONNECTOR.lock().unwrap();
    *global_connector = Some(Arc::new(connector));

    println!("CAD CLI 连接器初始化成功");
    Ok(())
}
///
/// ### 监控stdout
///
/// 监控CAD CLI的输出
///
/// [暂时停用]
#[allow(dead_code)]
pub fn monitor_stdout() -> Result<(), Error> {
    let connector = get_connector()?;
    unsafe {
        if !START_MONITOR {
            return Ok(());
        }
    }
    loop {
        let mut buffer = Vec::new();
        let bytes_read = connector
            .reader
            .lock()
            .unwrap()
            .read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break;
        }

        if let Ok(line) = String::from_utf8(buffer.clone()) {
            println!("{}", line);
        }
    }
    Ok(())
}

///
/// ### 发送参数到 CAD CLI (使用全局连接器)
///
/// 通过已建立的全局连接向 CAD 工具发送参数
///
/// `params`: 要发送的参数向量
pub fn send_params(params: Vec<String>) -> Result<(), Error> {
    // 从全局变量获取连接器
    unsafe {
        START_MONITOR = false;
    }
    let connector = get_connector()?;
    let connector_guard = connector;

    let mut buffer = Vec::new();
    let mut command = String::new();

    // 构建命令字符串
    for param in params {
        command += &format!("{} ", param);
    }

    // 发送命令
    writeln!(connector_guard.stdin.lock().unwrap(), "{}", command)?;

    // 读取响应（可以根据需要调整响应处理逻辑）
    loop {
        buffer.clear();
        let bytes_read = connector_guard
            .reader
            .lock()
            .unwrap()
            .read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // 尝试转换为字符串，忽略无效 UTF-8
        if let Ok(line) = String::from_utf8(buffer.clone()) {
            println!("---read-line---");
            println!("{}", line);
            if line.trim() == "-end" {
                break;
            }
            // 这里可以根据需要添加特定的响应处理逻辑
            // 例如等待特定的结束标志
        }
    }

    unsafe {
        START_MONITOR = true;
    }
    Ok(())
}

///
/// ### 关闭 CAD CLI 连接 (使用全局连接器)
///
/// 发送退出命令并清理资源
///
/// [暂时停用]
#[allow(dead_code)]
pub fn close_cli_connection() -> Result<(), Error> {
    println!("所有文档处理完毕，正在退出程序...");

    // 从全局变量获取连接器
    let connector = get_connector()?;
    let connector_guard = connector;

    writeln!(connector_guard.stdin.lock().unwrap(), "-exit")?;

    // 注意：这里不等待进程结束，让调用者决定如何处理
    // 如果需要等待，可以调用 child.wait()

    Ok(())
}

///
/// ### 强制终止子进程并清除连接器
///
/// 立即终止 CAD 子进程，并清除连接器实例允许重新初始化
pub fn kill_cad_process() -> Result<(), Error> {
    println!("正在强制终止 CAD 进程...");

    let connector = get_connector()?;

    // 通过锁获取 child_process 的可变引用
    let mut child_guard = connector.child_process.lock().unwrap();
    child_guard.kill()?;
    drop(child_guard);

    println!("CAD 进程已终止");

    drop(connector);

    let mut global_connector = CAD_CONNECTOR.lock().unwrap();
    *global_connector = None;

    println!("连接器已清除，可以重新初始化");
    Ok(())
}

///
/// ### 检查连接器是否已初始化
///
/// [暂时停用]
#[allow(dead_code)]
pub fn is_connected() -> bool {
    CAD_CONNECTOR.lock().unwrap().is_some()
}

///
/// ### 清除连接器实例
///
/// 手动清除连接器，允许重新初始化
///
/// [暂时停用]
#[allow(dead_code)]
pub fn clear_connector() -> Result<(), Error> {
    let mut global_connector = CAD_CONNECTOR.lock().unwrap();
    *global_connector = None;
    println!("连接器已清除");
    Ok(())
}

// ... existing code ...
