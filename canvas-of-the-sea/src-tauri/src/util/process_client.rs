use once_cell::sync::OnceCell;
use std::io;
use std::io::{BufRead, BufReader, Error, Write};
use std::process::{ChildStderr, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::{Arc, Mutex};

use crate::util::event::{send_start_connect_event, get_app_handle};

///
/// ### CLI 连接器结构体
///
/// 用于管理主进程与子进程的通信
pub struct CadCliConnector {
    pub stdin: ChildStdin,
    pub reader: BufReader<ChildStdout>,
    pub stderr: BufReader<ChildStderr>,
}

///
/// ### 全局 CAD CLI 连接器实例
///
/// 使用 OnceCell 实现延迟初始化的全局变量
static CAD_CONNECTOR: OnceCell<Arc<Mutex<CadCliConnector>>> = OnceCell::new();
static mut START_MONITOR: bool = false;

///
/// ### 获取全局连接器实例
///
/// 返回全局连接器的引用，如果未初始化则返回错误
fn get_connector() -> Result<Arc<Mutex<CadCliConnector>>, Error> {
    CAD_CONNECTOR.get().cloned().ok_or_else(|| {
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
        let bytes_read = connector.reader.read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // 尝试转换为字符串，忽略无效 UTF-8
        if let Ok(line) = String::from_utf8(buffer.clone()) {
            println!("{}", line);
            match line.trim() {
                "-start-cad" =>{
                    let app_handle = get_app_handle().unwrap();
                    send_start_connect_event(&app_handle)
                }
                "-start" => {
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
    writeln!(connector.stdin, "{}{}", command1, command2)?;

    loop {
        buffer.clear();
        let bytes_read = connector.reader.read_until(b'\n', &mut buffer)?;
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
    let mut child = Command::new(&acad_tool_path)
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
        stdin,
        reader,
        stderr: stderr_reader,
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

    // 存储到全局变量
    CAD_CONNECTOR
        .set(Arc::new(Mutex::new(connector)))
        .map_err(|_| {
            Error::new(
                io::ErrorKind::AlreadyExists,
                "CAD CLI 连接器已初始化，无法重复初始化",
            )
        })?;
    println!("CAD CLI 连接器初始化成功");
    Ok(())
}
///
/// ### 监控stdout
///
/// 监控CAD CLI的输出
pub fn monitor_stdout() -> Result<(), Error> {
    let connector = get_connector()?;
    unsafe {
        if  !START_MONITOR {
            return Ok(());
        }
    }
    loop {
        let mut buffer = Vec::new();
        let bytes_read = connector
            .lock()
            .unwrap()
            .reader
            .read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // 尝试转换为字符串，忽略无效 UTF-8
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
    let mut connector_guard = connector
        .lock()
        .map_err(|e| Error::new(io::ErrorKind::Other, format!("获取连接器锁失败：{}", e)))?;

    let mut buffer = Vec::new();
    let mut command = String::new();

    // 构建命令字符串
    for param in params {
        command += &format!("{} ", param);
    }

    // 发送命令
    writeln!(connector_guard.stdin, "{}", command)?;

    // 读取响应（可以根据需要调整响应处理逻辑）
    loop {
        buffer.clear();
        let bytes_read = connector_guard.reader.read_until(b'\n', &mut buffer)?;
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
pub fn close_cli_connection() -> Result<(), Error> {
    println!("所有文档处理完毕，正在退出程序...");

    // 从全局变量获取连接器
    let connector = get_connector()?;
    let mut connector_guard = connector
        .lock()
        .map_err(|e| Error::new(io::ErrorKind::Other, format!("获取连接器锁失败：{}", e)))?;

    writeln!(connector_guard.stdin, "-exit")?;

    // 注意：这里不等待进程结束，让调用者决定如何处理
    // 如果需要等待，可以调用 child.wait()

    Ok(())
}


///
/// ### 检查连接器是否已初始化
pub fn is_connected() -> bool {
    CAD_CONNECTOR.get().is_some()
}


