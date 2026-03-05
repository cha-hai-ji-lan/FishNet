import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { PathUtils, PATH_CONSTANTS } from './PathUtils';
// 软件相关路径
export const appPath = ref("__APP_PATH__")
export const binPath = ref("__BIN_PATH__")
export const configPathF = ref("__CONFIG_PATH_F__")

// 相关配置文件
export const mainConfig = ref<any>({config : "__CONFIGURE__"})  // 主要配置
export const themeConfig = ref<any>({config : "__THEME_CONFIGURE__"})  // 主题配置
export const interfaceStyle = ref<any>({config : "__INTERFACE_STYLE_CONFIGURE__"})  // 界面设置


// 内部配置
const currentThemeConfig = ref<string>("__CURRENT_THEME__")

export const init_app = async () => {
    await init_app_path()
    mainConfig.value = await invoke("read_json_file", { filePath: configPathF.value })
    await init_config()
    await init_color_palette()

}
const init_config = async () => {
    // 获取主题配置
    themeConfig.value = mainConfig.value["colorPalette"]["theme"]
    currentThemeConfig.value = themeConfig.value["currentTheme"]
    // 获取界面设置
    interfaceStyle.value = mainConfig.value["interfaceSetting"]
    console.log(interfaceStyle.value)
}
const init_color_palette = async () => {
    // 主题颜色
    document.documentElement.style.setProperty("--title",`rgba(${themeConfig.value[currentThemeConfig.value]["title"]})`)
    document.documentElement.style.setProperty("--background",`rgba(${themeConfig.value[currentThemeConfig.value]["background"]})`)
    document.documentElement.style.setProperty("--border-line",`rgba(${themeConfig.value[currentThemeConfig.value]["borderLine"]})`)
    document.documentElement.style.setProperty("--button",`rgba(${themeConfig.value[currentThemeConfig.value]["button"]})`)
    document.documentElement.style.setProperty("--font",`rgba(${themeConfig.value[currentThemeConfig.value]["font"]})`)
    // 界面样式
    document.documentElement.style.setProperty("--grid-size",`${interfaceStyle.value["gridSize"]}`)
    document.documentElement.style.setProperty("--transparency",`${interfaceStyle.value["InterfaceTransparency"]}`)

}

const init_app_path = async () => {
    appPath.value = await invoke<string>("get_app_path", {})
    // 使用规范的路径拼接方式
    binPath.value = await PathUtils.buildResourcePath(appPath.value, PATH_CONSTANTS.BIN_DIR)
    configPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.CONFIG_FILE);
}