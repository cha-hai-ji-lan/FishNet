<template>
    <div class="draw-two-piece-main">
        <div class="router">
            <div @click="() => {router.push(cacheRouterPath)}" class="router-item ban-select">
                <span>返回上一界面</span>
            </div>
            <div class="router-item ban-select">
                <span>基础设置</span>
            </div>
        </div>
        <div class="detail">
            <div class="setting-item">
                <div class="setting-title">软件透明度</div>
                <input v-model.number="transparencyValue" type="range" min="0" max="100">
                <div class="update-item">{{ transparencyValue }}</div>
            </div>
            <div class="setting-item">
                <div class="setting-title">主题切换</div>
                <div class="update-item">
                    <SelectBar v-model="currentTheme" :options="themeTypes" placeholder="主题样式"></SelectBar>

                </div>
            </div>
        </div>
    </div>
    <div class="float-save">
        <div @click="()=>{save_config()}" class="save-setting-button ban-select">保存</div>
        <div @click="()=>{replace_default_config()}" class="replace-setting-button ban-select">恢复默认</div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from "vue-router"; // 引入 useRoute
import SelectBar from '../utils/SelectorBar.vue';
import { themeTypes, cacheRouterPath } from '../../utils/Memory.ts'
import { themeConfig, interfaceStyle, init_color_palette, write_config , replace_config, init_app} from "../../utils/MainIndex.ts";

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
        // 更新 CSS 变量
        init_color_palette()
    }
});

const save_config = () =>{
    write_config()
}
const replace_default_config = async () =>{
    await replace_config()
    await  init_app()
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
    flex: 1%;
    /* height: 95vh; */
    background-color: rgba(var(--background), var(--transparency));
    /* background-color: rgba(33, 40, 48, 1); */
    /* 淡灰色底色 */
    background-image:
        linear-gradient(to right, rgba(var(--border-line), var(--transparency)) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(var(--border-line), var(--transparency)) 1px, transparent 1px);
    /* 创建虚线网格 */
    background-size: var(--grid-size) var(--grid-size);

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

            & .setting-title {
                width: 30%;
                margin: 2vmin;
            }

            & .update-item {
                text-align: center;
                flex: 1;
                max-width: 300px;
                height: 1.5vmin;
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
    }
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
        border: 2px solid rgba(6, 150, 215, 1);
        background-color: rgba(6, 150, 215, var(--pTransparency));

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
        border: 2px solid rgba(255, 206, 72, 1);
        background-color: rgba(255, 206, 72, var(--pTransparency));

        &:hover {
            filter: brightness(1.1);
        }

        &:active {
            filter: brightness(1.35);

        }
    }
}
</style>