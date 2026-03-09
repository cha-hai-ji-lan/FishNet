import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { PathUtils, PATH_CONSTANTS } from './PathUtils';
// 软件相关路径
export const appPath = ref("__APP_PATH__")
export const binPath = ref("__BIN_PATH__")
export const configPathF = ref("__CONFIG_PATH_F__")
export const defaultConfigPathF = ref("__DEFAULT_CONFIG_PATH_F__")

// 相关配置文件
export const mainConfig = ref<any>({ config: "__CONFIGURE__" })  // 主要配置
export const appConfig = ref<any>({ config: "__APP_CONFIGURE__" })  // 主要配置
export const themeConfig = ref<any>({ config: "__THEME_CONFIGURE__" })  // 主题配置
export const interfaceStyle = ref<any>({ config: "__INTERFACE_STYLE_CONFIGURE__" })  // 界面设置


//  内部文件
const defaultConfig = ref<any>({ config: "__DEFAULT_CONFIGURE__" })  // 主要配置

export const init_app = async () => {
    await init_app_path()
    mainConfig.value = await invoke("read_json_file", { filePath: configPathF.value })
    await init_config()
    await init_color_palette()

}

export const init_color_palette = async () => {
    console.log(themeConfig.value["currentTheme"])
    // 主题颜色
    document.documentElement.style.setProperty("--noramal-note", `${themeConfig.value["normalNote"]}`)
    document.documentElement.style.setProperty("--warn-note", `${themeConfig.value["warnNote"]}`)
    document.documentElement.style.setProperty("--error-note", `${themeConfig.value["errorNote"]}`)
    document.documentElement.style.setProperty("--title", `${themeConfig.value[themeConfig.value["currentTheme"]]["title"]}`)
    document.documentElement.style.setProperty("--background", `${themeConfig.value[themeConfig.value["currentTheme"]]["background"]}`)
    document.documentElement.style.setProperty("--border-line", `${themeConfig.value[themeConfig.value["currentTheme"]]["borderLine"]}`)
    document.documentElement.style.setProperty("--button", `${themeConfig.value[themeConfig.value["currentTheme"]]["button"]}`)
    document.documentElement.style.setProperty("--font", `${themeConfig.value[themeConfig.value["currentTheme"]]["font"]}`)
    // 界面样式
    document.documentElement.style.setProperty("--grid-size", `${interfaceStyle.value["gridSize"]}`)
    document.documentElement.style.setProperty("--transparency", `${interfaceStyle.value["interfaceTransparency"]}`)
    document.documentElement.style.setProperty("--pTransparency", `${interfaceStyle.value["partialTransparency"]}`)

}

export const write_config = async () => {
    // 获取主题配置
    mainConfig.value["colorPalette"]["theme"] = themeConfig.value; 
    // 获取界面设置
    mainConfig.value["interfaceSetting"] = interfaceStyle.value;
    await invoke("write_json_file", { filePath: configPathF.value , data: mainConfig.value})
}

const init_config = async () => {
    // 获取软件配置
    appConfig.value = mainConfig.value["app"]
    // 获取主题配置
    themeConfig.value = mainConfig.value["colorPalette"]["theme"]
    // 获取界面设置
    interfaceStyle.value = mainConfig.value["interfaceSetting"]
}

export const replace_config = async () => {
    defaultConfig.value = await invoke("read_json_file", { filePath: defaultConfigPathF.value })
    await invoke("write_json_file", { filePath: configPathF.value , data: defaultConfig.value})
}


const init_app_path = async () => {
    appPath.value = await invoke<string>("get_app_path", {})
    // 使用规范的路径拼接方式
    binPath.value = await PathUtils.buildResourcePath(appPath.value, PATH_CONSTANTS.BIN_DIR)
    configPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.CONFIG_FILE);
    defaultConfigPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.DEFAULT_CONFIG_FILE);
}