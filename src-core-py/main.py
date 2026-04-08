# --base-- format edition --base--
import argparse
import json
import re
from typing import Callable
from AcadCore import ACAD


class CLIHandler:
    """CLI命令处理器"""

    def __init__(self):
        self.commands = {}
        self.running = True
        self.acad = ACAD()
        self.register_default_commands()

    def register_default_commands(self):
        """注册默认命令"""
        self.register_command('-help', self.help_command, "show help information")
        self.register_command('-config-set', self.set_config_command, "Set the configuration parameters")
        self.register_command('-i', self.echo_command, "echo input command")
        self.register_command('-i-tb', self.acad.draw_two_piece_body, "draw Two-piece mesh body")

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
            self.running = False
            self.acad.__exit__(None, None, None)  # 关闭acad
            return False

        # 查找并执行命令
        if cmd_name in self.commands:
            try:
                print(f"--exe-command--{cmd_name}")
                result = self.commands[cmd_name]['function'](args)
                return result if result is not None else True
            except Exception as e:
                print(f"--exe-err--{e}")
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
            print("echo:")
            print("-fin-", "-".join(args))
        else:
            print("enter_what_you_want_to_echo")

    def set_config_command(self, args):
        """设置配置命令"""
        if args:
            self.acad.cfg = json.loads(" ".join(args))
            self.acad.cfg["originPosition"] = [
                float(x) for x in re.findall(r'\d+\.\d+|\d+', self.acad.cfg["originPosition"])
            ]
            self.acad.cfg["originPosition"].extend(
                [self.acad.cfg["originPosition"][0] + 10000000.0, self.acad.cfg["originPosition"][1]])
            self.acad.set_core_config_encapsulation()  # 设置核心封装
            print("-fin-set-", self.acad.cfg, type(self.acad.cfg))
        else:
            print("请输入要设置的配置参数")

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
                print("-end")

            except KeyboardInterrupt:
                print("-ctrl-c-is-detected")
                break
            except EOFError:
                print("-end-of-input-stream")
                break

    finally:
        print("-exit-app-normal")


if __name__ == "__main__":
    main()
