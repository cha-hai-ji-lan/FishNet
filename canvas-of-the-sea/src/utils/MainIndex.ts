import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { PathUtils, PATH_CONSTANTS } from './PathUtils';
// 软件相关路径
export const appPath = ref("__APP_PATH__")
export const binPath = ref("__BIN_PATH__")
export const configPathF = ref("__CONFIG_PATH_F__")

// 相关配置文件
export const mainConfig = ref<any>({config : "__CONFIGURE__"})
export const ThemeConfig = ref<any>({config : "__THEME_CONFIGURE__"})


// 内部配置
const currentThemeConfig = ref<string>("__CURRENT_THEME__")

export const init_app = async () => {
    await init_app_path()
    mainConfig.value = await invoke("read_json_file", { filePath: configPathF.value })
    await init_config()
    await init_color_palette()

}
const init_config = async () => {
    ThemeConfig.value = mainConfig.value["ColorPalette"]["Theme"]
    currentThemeConfig.value = ThemeConfig.value["currentTheme"]
}
const init_color_palette = async () => {
    // 主题颜色
    document.documentElement.style.setProperty("--title",`rgba(${ThemeConfig.value[currentThemeConfig.value]["Title"]})`)
    document.documentElement.style.setProperty("--background",`rgba(${ThemeConfig.value[currentThemeConfig.value]["Background"]})`)
    document.documentElement.style.setProperty("--border-line",`rgba(${ThemeConfig.value[currentThemeConfig.value]["BorderLine"]})`)
    document.documentElement.style.setProperty("--button",`rgba(${ThemeConfig.value[currentThemeConfig.value]["Button"]})`)
    document.documentElement.style.setProperty("--font",`rgba(${ThemeConfig.value[currentThemeConfig.value]["Font"]})`)
}

const init_app_path = async () => {
    appPath.value = await invoke<string>("get_app_path", {})
    // 使用规范的路径拼接方式
    binPath.value = await PathUtils.buildResourcePath(appPath.value, PATH_CONSTANTS.BIN_DIR)
    configPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.CONFIG_FILE);
}