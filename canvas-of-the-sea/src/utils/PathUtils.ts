import { join, resolve, dirname, basename, extname } from '@tauri-apps/api/path';
import { sep } from '@tauri-apps/api/path';

/**
 * 路径处理工具类
 * 提供跨平台的路径操作方法
 */
export class PathUtils {
  /**
   * 安全地拼接路径
   * @param paths 要拼接的路径片段
   * @returns 拼接后的完整路径
   */
  static async joinPaths(...paths: string[]): Promise<string> {
    if (paths.length === 0) return '';
    if (paths.length === 1) return paths[0];
    
    return await join(...paths);
  }

  /**
   * 解析绝对路径
   * @param path 相对路径或绝对路径
   * @returns 绝对路径
   */
  static async resolvePath(path: string): Promise<string> {
    return await resolve(path);
  }

  /**
   * 获取文件所在目录
   * @param filePath 文件路径
   * @returns 目录路径
   */
  static async getDirectory(filePath: string): Promise<string> {
    return await dirname(filePath);
  }

  /**
   * 获取文件名
   * @param filePath 文件路径
   * @param ext 是否包含扩展名
   * @returns 文件名
   */
  static async getFileName(filePath: string, ext: boolean = true): Promise<string> {
    const fileName = await basename(filePath);
    return ext ? fileName : fileName.replace(new RegExp(`${await extname(filePath)}$`), '');
  }

  /**
   * 构建资源路径
   * @param basePath 基础路径
   * @param resourcePath 资源相对路径
   * @returns 完整的资源路径
   */
  static async buildResourcePath(basePath: string, resourcePath: string): Promise<string> {
    return await this.joinPaths(basePath, resourcePath);
  }

  /**
   * 验证路径是否存在（简化版）
   * @param path 要验证的路径
   * @returns 路径是否存在
   */
  static async pathExists(_path: string): Promise<boolean> {
    try {
      // 这里可以调用 Tauri 的文件系统 API 来检查路径
      // 暂时返回 true，实际使用时需要实现具体逻辑
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 标准化路径分隔符
   * @param path 原始路径
   * @returns 标准化后的路径
   */
  static normalizePath(path: string): string {
    return path.replace(/\\/g, sep).replace(/\//g, sep);
  }
}

// 导出常用的路径常量
export const PATH_CONSTANTS = {
  BIN_DIR: 'bin',
  CONFIG_FILE: 'config.json',
  DEFAULT_CONFIG_FILE: 'defaultConfig.json',
  TEMPLATE_FILE: 'template.json',
  FISH_NET_EXE: 'fishNet.exe',
} as const;