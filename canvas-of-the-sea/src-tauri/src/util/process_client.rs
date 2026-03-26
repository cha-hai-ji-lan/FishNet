use std::io;
use std::io::{BufRead, BufReader, Error, Write};
use std::path::{PathBuf};
use std::process::{ChildStderr, ChildStdin, ChildStdout, Command, Stdio};

///
/// ### 主进程与子进程通讯器
///
/// `acad_tool_path`: 启动的文档处理工具路径
///
/// `args_g1`: 命令行参数组1
///
/// `args_g2`: 命令行参数组2
pub fn cad_cli_exchanges(
    acad_tool_path: String,
    args_g1: Option<Vec<String>>,
    args_g2: Option<Vec<String>>,
) -> Result<(), Error> {
    // 启动 acad_tool.exe
    let mut child = Command::new("cmd")
        .args(&["/C", &acad_tool_path])
        .stdin(Stdio::piped())  // 创建管道捕获 标准输入 [主进程 -> 子进程]
        .stdout(Stdio::piped()) // 创建管道捕获 标准输出 [子进程 -> 主进程]
        .stderr(Stdio::piped()) // 创建管道捕获 错误输出 [子进程 -> 主进程]
        .spawn()?;
    let mut stdin:ChildStdin = child.stdin.take().unwrap(); // 获取 stdin
    let stdout: ChildStdout = child.stdout.take().unwrap(); // 获取 stdout
    let stderr: ChildStderr = child.stderr.take().unwrap(); // 获取 stderr
    let mut command1 = String::new(); // 创建命令行参数字符串 组1
    let mut command2 = String::new(); // 创建命令行参数字符串 组2
    // 使用字节流而不是 UTF-8 字符串
    // BufReader::new(stdout)：包装 stdout 管道，提供带缓冲的读取能力，避免频繁的系统调用
    let mut reader = BufReader::new(stdout);  // 读取缓冲区，用于读取字节流
    // buffer：可增长的字节向量，作为临时存储空间，配合 read_until() 逐行读取子进程输出
    let mut buffer = Vec::new();  // 创建缓冲区，用于存储字节流
    // 用于等待 "-start" 输出 标志位
    let mut found_start = false;
    // 用于等待 "-end" 输出 标志位
    let mut found_end = false;
    loop {
        buffer.clear();
        let bytes_read = reader.read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }
        // 尝试转换为字符串，忽略无效UTF-8
        if let Ok(line) = String::from_utf8(buffer.clone()) {
            println!("{}", line);
            if line.trim() == "-start" {
                found_start = true;
                break;
            }
        }
    }
    if !found_start {
        return Err(Error::new(
            io::ErrorKind::NotFound,
            "无法找到 -start 起始标志".to_string(),
        ));
    }
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
    loop {
        writeln!(stdin, "{}{}", command1, command2)?;  // 发送命令行参数
        buffer.clear();
        let bytes_read = reader.read_until(b'\n', &mut buffer)?;
        if bytes_read == 0 {
            break; // EOF
        }

        // 尝试转换为字符串，忽略无效UTF-8
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

    // 发送退出命令
    println!("所有文档处理完毕，正在退出程序...");
    writeln!(stdin, "-exit")?;

    // 等待进程结束
    let _ = child.wait();

    Ok(())
}
// fn main() {
//     let args: Vec<String> = Vec::from([r"D:\Object_\靶场\新建文件夹\office\内燃机轴系扭转振动分析系统使用手册.docx".to_string(),
//         r"D:\Object_\靶场\新建文件夹\office\信息表.docx".to_string(),]);
//     office_fm_cov(
//         r"D:\Object_\APP\Tauri\work\Click\click_v1\src-py\officeCC.exe".to_string(),
//         Some(vec!["-docx2xlsx".to_string()]),
//         args,
//         Some(vec![]),
//         "docx".to_string(),
//         "xlsx".to_string(),
//     )
//         .expect("Error");
// }
