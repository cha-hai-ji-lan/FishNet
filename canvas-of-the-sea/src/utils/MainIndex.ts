import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { PathUtils, PATH_CONSTANTS } from './PathUtils';
// 软件相关路径
export const appPath = ref("__APP_PATH__")  // 软件路径
export const binPath = ref("__BIN_PATH__")  // 资源文件夹路径
export const configPathF = ref("__CONFIG_PATH_F__") // 配置文件路径
export const defaultConfigPathF = ref("__DEFAULT_CONFIG_PATH_F__")  // 默认配置文件路径
export const templatePathF = ref("__TEMPLATE_PATH_F__")  // 模板文件路径
export const fishNetEXE = ref("__FISH_NET_PATH_EXE__")  // 绘网工具程序路径

// 相关配置文件
export const mainConfig = ref<any>({ config: "__CONFIGURE__" })  // 主要配置
export const appConfig = ref<any>({ config: "__APP_CONFIGURE__" })  // 软件配置
export const themeConfig = ref<any>({ config: "__THEME_CONFIGURE__" })  // 主题配置
export const interfaceStyle = ref<any>({ config: "__INTERFACE_STYLE_CONFIGURE__" })  // 界面设置
export const coreConfig = ref<any>({ config: "__DEFAULT_CORE_CONFIGURE__" })  // 核心参数
// 模板配置
export const NetT = ref<any>({ config: "__NET_TEMPLATE__" })  // 总模板
export const twoNetT = ref<any>({ config: "__TWO_NET_TEMPLATE__" })  // 两片式模板
export const fourNetT = ref<any>({ config: "__FOUR_NET_TEMPLATE__" })  // 四片式模板
export const sixNetT = ref<any>({ config: "__SIX_NET_TEMPLATE__" })  // 六片式模板


//  内部文件
const defaultConfig = ref<any>({ config: "__DEFAULT_CONFIGURE__" })  // 默认参数 用于恢复默认配置

export const init_app = async () => {
    await init_app_path()
    mainConfig.value = await invoke("read_json_file", { filePath: configPathF.value })
    await init_config()
    await init_template()
    await init_color_palette()

}

export const init_color_palette = async () => {
    console.log(themeConfig.value["currentTheme"])
    // 主题颜色
    document.documentElement.style.setProperty("--ready-note", `${themeConfig.value["readyNote"]}`)
    document.documentElement.style.setProperty("--normal-note", `${themeConfig.value["normalNote"]}`)
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

export const init_template = async () => {
    NetT.value = await invoke("read_json_file", { filePath: templatePathF.value })
    twoNetT.value = NetT.value["twoPieces"]
    fourNetT.value = NetT.value["fourPieces"]
    sixNetT.value = NetT.value["sixPieces"]
}
export const write_config = async () => {
    // 获取主题配置
    mainConfig.value["colorPalette"]["theme"] = themeConfig.value;
    // 获取界面设置
    mainConfig.value["interfaceSetting"] = interfaceStyle.value;
    // core配置将在setting中直接写入config
    await invoke("write_json_file", { filePath: configPathF.value, data: mainConfig.value })
}

const init_config = async () => {
    // 获取软件配置
    appConfig.value = mainConfig.value["app"]
    // 获取主题配置
    themeConfig.value = mainConfig.value["colorPalette"]["theme"]
    // 获取界面设置
    interfaceStyle.value = mainConfig.value["interfaceSetting"]
    // 核心参数
    coreConfig.value = mainConfig.value["core"]

}

export const replace_config = async () => {
    defaultConfig.value = await invoke("read_json_file", { filePath: defaultConfigPathF.value })
    await invoke("write_json_file", { filePath: configPathF.value, data: defaultConfig.value })
}


const init_app_path = async () => {
    appPath.value = await invoke<string>("get_app_path", {})
    // 使用规范的路径拼接方式
    binPath.value = await PathUtils.buildResourcePath(appPath.value, PATH_CONSTANTS.BIN_DIR)
    configPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.CONFIG_FILE);
    defaultConfigPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.DEFAULT_CONFIG_FILE);
    templatePathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.TEMPLATE_FILE);
    fishNetEXE.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.FISH_NET_EXE);
}