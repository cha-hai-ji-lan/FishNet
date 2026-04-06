<template>
    <div class="draw-two-piece-main">
        <div class="router">
            <div @click="() => { router.push(cacheRouterPath) }" class="router-item ban-select">
                <span>返回上一界面</span>
            </div>
            <div class="router-item ban-select" @click="() => { rollTo('app-base-setting') }">
                <span>软件基础设置</span>
            </div>
            <div class="router-item ban-select" @click="() => { rollTo('app-core-setting') }">
                <span>服务设置</span>
            </div>
            <div class="router-item ban-select" @click="() => { rollTo('app-default-setting') }">
                <span>缺省参数设置</span>
            </div>
        </div>
        <div class="detail">
            <div class="setting-item">
                <span id="app-base-setting" class="position-title ban-select">软件基础设置</span>
            </div>
            <div class="setting-item">
                <div class="setting-title ban-select">软件透明度</div>
                <input v-model.number="transparencyValue" type="range" min="0" max="100">
                <div class="update-item">{{ transparencyValue }}</div>
            </div>
            <div class="setting-item">
                <div class="setting-title ban-select">主题切换</div>
                <div class="update-item">
                    <SelectBar v-model="currentTheme" :options="themeTypes" placeholder="主题样式"></SelectBar>

                </div>
            </div>
            <div class="setting-item part-flex-colum">
                <div class="setting-item ban-bor-bgc">
                    <div class="setting-title ban-select">主题颜色</div>
                    <div @click="() => { init_color_palette() }" class="set-but ban-select">设置</div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">标题栏颜色</div>
                    <div class="update-item nor-input">
                        <input v-model="ThemeColor['title']" type="text" :placeholder="ThemeColor['title']">
                    </div>
                    <div class="color-block" :style="{ 'background-color': `rgb(${ThemeColor['title']})` }"></div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">背景颜色</div>
                    <div class="update-item nor-input">
                        <input v-model="ThemeColor['background']" type="text" :placeholder="ThemeColor['background']">

                    </div>
                    <div class="color-block" :style="{ 'background-color': `rgb(${ThemeColor['background']})` }"></div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">边框线颜色</div>
                    <div class="update-item nor-input">
                        <input v-model="ThemeColor['borderLine']" type="text" :placeholder="ThemeColor['borderLine']">

                    </div>
                    <div class="color-block" :style="{ 'background-color': `rgb(${ThemeColor['borderLine']})` }"></div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">一般按钮颜色</div>
                    <div class="update-item nor-input">
                        <input v-model="ThemeColor['button']" type="text" :placeholder="ThemeColor['button']">
                    </div>
                    <div class="color-block" :style="{ 'background-color': `rgb(${ThemeColor['button']})` }"></div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">文字颜色</div>
                    <div class="update-item nor-input">
                        <input v-model="ThemeColor['font']" type="text" :placeholder="ThemeColor['font']">
                    </div>
                    <div class="color-block" :style="{ 'background-color': `rgb(${ThemeColor['font']})` }"></div>
                </div>
            </div>
            <div class="setting-item">
                <span id="app-core-setting" class="position-title ban-select">服务设置</span>
            </div>
            <div class="setting-item">
                <div class="setting-title ban-select">重启服务</div>
                <div @click="()=>{reset_cli()}" class="update-item">
                    <div class="set-but ban-select">重启服务端</div>
                </div>
            </div>
            <div class="setting-item">
                <div class="setting-title ban-select">聚焦绘图</div>
                <div class="update-item" @click="() => { switch_but('focusDraw') }">
                    <div class="set-but ban-select" :class="{ 'lost-color': focusDraw === '禁用中' }">{{ focusDraw }}</div>
                </div>
            </div>
            <div class="setting-item">
                <div class="setting-title ban-select">撤销模式</div>
                <div class="update-item" @click="() => { switch_but('undoMode') }">
                    <div class="set-but ban-select">{{ undoMode }}</div>
                </div>
            </div>
            <div class="setting-item">
                <span id="app-default-setting" class="position-title ban-select">缺省参数设置</span>
            </div>
            <div class="setting-item part-flex-colum">
                <div class="setting-item ban-bor-bgc">
                    <div class="setting-title ban-select">缺省参数</div>
                    <!-- <div @click="() => { init_color_palette() }" class="set-but ban-select">设置</div> -->
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">全局缩放</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['zoom']" type="number" :placeholder="CoreConfig['zoom']">
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">表格偏移量</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['tableOffset']" type="number"
                            :placeholder="CoreConfig['tableOffset']">
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">水平比例尺</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['scaleX']" type="number" :placeholder="CoreConfig['scaleX']">
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">垂直比例尺</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['scaleY']" type="number" :placeholder="CoreConfig['scaleY']">
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">字 高</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['textHeight']" type="number" :placeholder="CoreConfig['textHeight']">
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">表 格 字 高</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['commentOffset']" type="number"
                            :placeholder="CoreConfig['commentOffset']">
                    </div>
                </div>
                <div class="setting-item">
                    <div class="setting-title ban-select">制 网 材 料</div>
                    <div class="update-item nor-input">
                        <input v-model="CoreConfig['materal']" type="text" :placeholder="CoreConfig['materal']">
                    </div>
                </div>
            </div>
            <div class="setting-item ban-bor-bgc">
                <div class="blank-10vh"></div>
            </div>
        </div>
    </div>
    <div class="float-save">
        <div @click="() => { save_config() }" class="save-setting-button ban-select">保存</div>
        <div @click="() => { replace_default_config() }" class="replace-setting-button ban-select">恢复默认</div>
    </div>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue';
import { invoke } from "@tauri-apps/api/core";
import { useRouter } from "vue-router"; // 引入 useRoute
import SelectBar from '../utils/SelectorBar.vue';
import { themeTypes, cacheRouterPath } from '../../utils/Memory.ts'
import { init_cad_listen_group} from "../../utils/event.ts";
import { themeConfig, interfaceStyle, coreConfig, fishNetEXE, init_color_palette, write_config, replace_config, init_app } from "../../utils/MainIndex.ts";

const focusDraw = ref<string>("启用中")
const undoMode = ref<string>("段撤销")

const router = useRouter()

// 创建可写的计算属性
const transparencyValue = computed({
    get: () => Math.round(interfaceStyle.value['interfaceTransparency'] * 100),
    set: (newValue: number) => {
        interfaceStyle.value['interfaceTransparency'] = newValue / 100;
        // 更新 CSS 变量
        document.documentElement.style.setProperty("--transparency", `${newValue / 100}`);
    }
});
const currentTheme = computed({
    get: () => themeConfig.value["currentTheme"],
    set: (newValue: string) => {
        themeConfig.value["currentTheme"] = newValue;
        console.log(newValue)

        // 更新 CSS 变量
        init_color_palette()
    }
});
const ThemeColor = computed({
    get: () => themeConfig.value[themeConfig.value["currentTheme"]],
    set: (newValue: number[]) => {
        console.log(newValue)
        // 更新 CSS 变量
        init_color_palette()
    }
});
const CoreConfig = computed({
    get: () => coreConfig.value["defaultParam"],
    set: (newValue: any) => {
        console.log(newValue)
    }
});

const rollTo = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({
            block: 'start',
            behavior: 'smooth'
        });
    }
}

const switch_but = (who: string) => {  // 切换按钮样式
    switch (who) {
        case "focusDraw":
            if (focusDraw.value === "启用中") {
                coreConfig.value["focusDraw"] = false;
                focusDraw.value = "禁用中";
            } else if ((focusDraw.value === "禁用中")) {
                coreConfig.value["focusDraw"] = true;
                focusDraw.value = "启用中";

            }
            break;
        case "undoMode":
            if (undoMode.value === "段撤销") {
                coreConfig.value["backUpMode"] = "single-step";
                undoMode.value = "步撤销"
            } else if ((undoMode.value === "步撤销")) {
                coreConfig.value["backUpMode"] = "segment-step";
                undoMode.value = "段撤销"
            }
            break;
        default:
            break;
    }

}
const reset_cli = () =>{
    init_cad_listen_group()
    invoke("reset_cli", { acadToolPath:fishNetEXE.value, command1: ["-config-set",  JSON.stringify(coreConfig.value["defaultParam"])]})
}
const save_config = () => {
    console.log(JSON.stringify(coreConfig.value["defaultParam"]))
    invoke("send_param_to_cli", {command: ["-config-set", JSON.stringify(coreConfig.value["defaultParam"])]})
    write_config()
}
const replace_default_config = async () => {
    await replace_config()
    await init_app()
}
</script>
<style scoped>
.draw-two-piece-main {
    font-family: "思印宋", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    font-size: 3vmin;
    color: rgba(var(--font), 1);
    display: flex;
    align-items: center;
    justify-content: start;
    flex-direction: row;
    width: 100%;
    height: 95%;
    overflow: hidden;
    /* height: 95vh; */
    background-color: rgba(var(--background), var(--transparency));
    /* background-color: rgba(33, 40, 48, 1); */
    /* 淡灰色底色 */
    background-image:
        linear-gradient(to right, rgba(var(--border-line), var(--transparency)) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(var(--border-line), var(--transparency)) 1px, transparent 1px);
    /* 创建虚线网格 */
    background-size: var(--grid-size) var(--grid-size);
    transition: all 1.25s ease-in-out;


    & .router {
        display: flex;
        align-items: center;
        justify-content: start;
        flex-direction: column;
        height: 100%;
        width: 22.5%;
        max-width: 250px;
        background-color: rgba(var(--title), var(--transparency));
        border-right: 2px solid rgba(var(--font), var(--transparency));

        & .router-item {
            width: 100%;
            height: fit-content;
            text-align: center;
            background-color: rgba(var(--button), var(--pTransparency));
            margin-top: 2vmin;
            border-radius: 0.75vmin;
            padding: 2vmin 0;

            &:hover {
                border: 2px solid rgba(var(--font), var(--pTransparency));
                padding: calc(2vmin - 2px) 0;
                filter: brightness(1.2)
            }

            &:active {
                border: 2px solid rgba(var(--font), var(--transparency));
                padding: calc(2vmin - 2px) 0;

                filter: brightness(1.2)
            }
        }

    }

    & .detail {
        flex: 1;
        display: flex;
        align-items: start;
        justify-content: start;
        flex-direction: column;
        height: 100%;
        margin: 2vmin;
        overflow-y: auto;
        overflow-x: hidden;


        & .setting-item {
            display: flex;
            align-items: center;
            justify-content: start;
            flex-direction: row;
            width: 100%;
            margin-top: 2vmin;
            border: 2px solid rgba(var(--border-line), var(--transparency));
            border-radius: 2vmin;
            background-color: rgba(var(--button), var(--pTransparency));

            & .position-title {
                font-size: 3.5vmin;
                font-weight: bold;
                margin: 0.5vmin 2vmin;
            }

            &.ban-bor-bgc {
                border: 0 solid rgba(var(--border-line), var(--transparency));
                border-radius: 0;
                background-color: rgba(0, 0, 0, 0);
            }

            &.part-flex-colum {
                align-items: start;
                flex-direction: column;
            }

            & .set-but {
                width: fit-content;
                height: fit-content;
                display: flex;
                align-items: start;
                justify-content: start;
                flex-direction: row;
                margin-left: auto;
                margin-right: 4vmin;
                padding: 0.25vmin 3.5vmin;
                border-radius: 1.5vmin;
                border: 2px solid rgba(var(--normal-note), 1);
                background-color: rgba(var(--normal-note), var(--pTransparency));

                &:hover {
                    filter: brightness(1.1);
                }

                &:active {
                    filter: brightness(1.35);

                }

                &.lost-color {
                    border: 2px solid rgba(var(--background), 1);
                    background-color: rgba(var(--background), var(--pTransparency));
                }
            }

            & .setting-title {
                width: 30%;
                margin: 2vmin;
            }

            & .update-item {
                text-align: center;
                flex: 1;
                max-width: 300px;
                /* height: 1.5vmin; */
            }

            & input[type="range"] {
                -webkit-appearance: none;
                appearance: none;

                background: rgba(var(--button), var(--transparency));
                border-radius: 0.75vmin;
                outline: none;
                cursor: pointer;

                &::-webkit-slider-thumb {
                    -webkit-appearance: none;
                    appearance: none;
                    width: 2vmin;
                    height: 2vmin;
                    background: rgba(var(--button), var(--transparency));
                    border-radius: 50%;
                    cursor: pointer;
                    transition: all 0.2s ease;

                    &:hover {
                        background: rgba(var(--font), var(--transparency));
                        transform: scale(1.2);
                    }

                    &:active {
                        transform: scale(0.9);
                    }
                }

                &::-moz-range-thumb {
                    width: 2vmin;
                    height: 2vmin;
                    background: rgba(var(--button), var(--transparency));
                    border-radius: 50%;
                    border: none;
                    cursor: pointer;
                    transition: all 0.2s ease;

                    &:hover {
                        background: rgba(var(--font), var(--transparency));
                        transform: scale(1.2);
                    }

                    &:active {
                        transform: scale(0.9);
                    }
                }

                &::-ms-thumb {
                    width: 2vmin;
                    height: 2vmin;
                    background: rgba(var(--button), var(--transparency));
                    border-radius: 50%;
                    cursor: pointer;
                }
            }
        }

        &::-webkit-scrollbar {
            width: 1vmin;
            /* 垂直滚动条宽度 */
            height: 1vmin;
            /* 水平滚动条高度 */

        }

        &::-webkit-scrollbar-track {
            background: rgba(var(--title), var(--pTransparency));
            /* 滚动条轨道背景色 */
            border-radius: 4px;
        }

        &::-webkit-scrollbar-thumb {
            background: rgba(var(--button), var(--pTransparency));
            /* 滚动条滑块颜色 */
            border-radius: 4px;
        }

        &::-webkit-scrollbar-thumb:hover {
            filter: brightness(1.2);
            /* 滑块悬停时的颜色 */
        }
    }
}

.nor-input {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    width: 100%;
    border-bottom: 2px solid rgba(var(--button), var(--transparency));
    padding-top: 1vmin;
    padding-bottom: 1vmin;
    margin-right: 2vmin;


    /* 数字输入框移除上下箭头 */
    & input[type="number"]::-webkit-inner-spin-button,
    & input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    & input {
        /* 移除所有默认样式 */
        appearance: none;
        -webkit-appearance: none;
        -moz-appearance: none;

        /* 重置边框和背景 */
        border: 2px solid rgba(var(--title), var(--transparency));
        outline: none;
        background: transparent;

        /* 重置其他样式 */
        padding: 0;
        margin: 0;
        font-family: inherit;
        font-size: inherit;
        color: inherit;
        border-radius: 0;
        background-color: rgba(var(--border-line), var(--transparency));
        border-radius: 1vmin;
        text-align: center;
        height: 3vmin;

        &:hover {
            filter: drop-shadow(0 0 0.25em rgba(var(--normal-note), 0.75));
        }

        &:active {
            border: 2px solid rgba(var(--normal-note), 1);
        }

        &:focus {
            border: 2px dashed rgba(var(--normal-note), 0.75);
        }
    }
}

.color-block {
    width: 3vmin;
    height: 3vmin;
    border-radius: 0.75vmin;
    border: 2px solid rgba(var(--title), var(--pTransparency));
}

.float-save {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    bottom: 2vmin;
    right: 2vmin;
    width: fit-content;
    height: 8vmin;
    border-radius: 2vmin;
    background-color: rgba(var(--button), var(--pTransparency));
    z-index: 100;

    & .save-setting-button {
        margin: 1.5vmin;
        font-size: 3.25vmin;
        font-family: "思印宋", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 18vmin;
        height: 4vmin;
        border-radius: 1vmin;
        border: 2px solid rgba(var(--normal-note), 1);
        background-color: rgba(var(--normal-note), var(--pTransparency));

        &:hover {
            filter: brightness(1.1);
        }

        &:active {
            filter: brightness(1.35);

        }
    }

    & .replace-setting-button {
        margin: 1.5vmin;
        font-size: 3.25vmin;
        font-family: "思印宋", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 18vmin;
        height: 4vmin;
        border-radius: 1vmin;
        border: 2px solid rgba(var(--warn-note), 1);
        background-color: rgba(var(--warn-note), var(--pTransparency));

        &:hover {
            filter: brightness(1.1);
        }

        &:active {
            filter: brightness(1.35);

        }
    }
}
</style>