import { ref } from "vue";
import { invoke } from "@tauri-apps/api/core";
import { PathUtils, PATH_CONSTANTS } from './PathUtils';
// 软件相关路径
export const appPath = ref("__APP_PATH__")
export const binPath = ref("__BIN_PATH__")
export const configPathF = ref("__CONFIG_PATH_F__")

// 相关配置文件
export const mainConfig = ref<any>({config : "__CONFIGURE__"})



export const init_app = async () => {
    await init_app_path()
    mainConfig.value = await invoke("read_json_file", { filePath: configPathF.value })
    console.log(mainConfig.value)
    console.log(mainConfig.value["ColorPalette"]["Theme"]["dark"])

}

const init_app_path = async () => {
    appPath.value = await invoke<string>("get_app_path", {})
    // 使用规范的路径拼接方式
    binPath.value = await PathUtils.buildResourcePath(appPath.value, PATH_CONSTANTS.BIN_DIR)
    configPathF.value = await PathUtils.buildResourcePath(binPath.value, PATH_CONSTANTS.CONFIG_FILE);
}