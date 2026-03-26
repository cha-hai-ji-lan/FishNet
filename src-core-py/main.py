# main.py
import argparse
import os
from typing import Callable

import win32com.client
from AcadCore import ACAD


class CLIHandler:
    """CLI命令处理器"""

    def __init__(self):
        self.commands = {}
        self.running = True
        self.register_default_commands()
        self.acad = ACAD()

    def register_default_commands(self):
        """注册默认命令"""
        self.register_command('help', self.help_command, "显示帮助信息--测试使用")
        self.register_command('echo', self.echo_command, "回显输入内容--测试使用")
        self.register_command('status', self.status_command, "显示程序状态--测试使用")
        self.register_command('calc', self.calc_command, "简单计算器--测试使用")

    def register_command(self, name: str, func: Callable, description: str = ""):
        """注册新命令"""
        self.commands[name] = {
            'function': func,
            'description': description
        }

    def process_command(self, command_str: str) -> bool:
        """处理命令字符串"""
        if not command_str.strip():
            return True

        parts = command_str.split()
        cmd_name = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # 检查是否为退出命令
        if cmd_name in ['-exit', 'exit', 'quit', '-quit']:
            self.acad.__exit__(None, None, None)
            self.running = False
            return False

        # 查找并执行命令
        if cmd_name in self.commands:
            try:
                result = self.commands[cmd_name]['function'](args)
                return result if result is not None else True
            except Exception as e:
                print(f"执行命令 '{cmd_name}' 时出错: {str(e)}")
                return False
        else:
            print(f"未知命令: {cmd_name}")
            print("输入 'help' 查看可用命令")
            return True

    def help_command(self):
        """帮助命令"""
        print("可用命令:")
        print("-" * 30)
        for cmd_name, cmd_info in self.commands.items():
            desc = cmd_info['description'] or "无描述"
            print(f"  {cmd_name:<10} - {desc}")
        print("\n特殊命令:")
        print("  -exit      - 退出程序")
        print("  exit/quit  - 退出程序")
        print("-" * 30)

    @staticmethod
    def echo_command(args):
        """回显命令"""
        if args:
            print(" ".join(args))
        else:
            print("请输入要回显的内容")

    def status_command(self, args):
        """状态命令"""
        import datetime
        print(f"程序运行状态: 正常运行")
        print(f"当前时间: {datetime.datetime.now()}")
        print(f"已注册命令数: {len(self.commands)}")
        print(f"进程ID: {os.getpid()}")

    @staticmethod
    def calc_command(args):
        """计算器命令"""
        if len(args) != 3:
            print("用法: calc <数字1> <操作符> <数字2>")
            print("支持的操作符: + - * /")
            return

        try:
            num1 = float(args[0])
            operator = args[1]
            num2 = float(args[2])

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    print("错误: 除数不能为零")
                    return
                result = num1 / num2
            else:
                print(f"不支持的操作符: {operator}")
                return

            print(f"{num1} {operator} {num2} = {result}")

        except ValueError:
            print("错误: 请输入有效的数字")


    @staticmethod
    def cleanup():
        """清理资源"""
        print("正在清理资源...")


def main():
    """主函数 - CLI程序入口"""
    # 创建CLI处理器
    cli_handler = CLIHandler()

    # 解析初始命令行参数
    parser = argparse.ArgumentParser(description='持续运行的CLI程序')
    parser.add_argument('command', nargs='*', help='初始命令参数')
    parser.add_argument('-exit', action='store_true', help='退出程序')

    args = parser.parse_args()

    # 如果初始参数包含-exit，则直接退出
    if args.exit:
        print("程序启动时收到退出指令，正在退出...")
        return

    # 处理初始命令
    if args.command:
        initial_command = ' '.join(args.command)
        print(f"处理初始命令: {initial_command}")
        cli_handler.process_command(initial_command)

    # 进入持续运行模式 向rust发送初始化完成目录
    print("-start")

    try:
        while cli_handler.running:
            try:
                # 获取用户输入
                user_input = input(">>>").strip()

                # 处理用户命令
                if user_input:
                    cli_handler.process_command(user_input)

            except KeyboardInterrupt:
                print("\n\n检测到Ctrl+C，程序即将退出...")
                break
            except EOFError:
                print("\n输入流结束，程序退出...")
                break

    finally:
        # 清理资源
        cli_handler.cleanup()
        print("程序已正常退出")


if __name__ == "__main__":
    main()
