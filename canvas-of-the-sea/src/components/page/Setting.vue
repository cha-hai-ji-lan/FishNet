<template>
    <div class="draw-two-piece-main">
        <div class="router"></div>
        <div class="detail">
            <div class="setting-item">
                <div class="setting-title">软件透明度</div>
                <input v-model.number="transparencyValue" type="range" min="0" max="100">
                <div>{{ transparencyValue }}</div>
            </div>
        </div>
    </div>
    <div class="float-save">
        <div class="save-setting-button ban-select">保存</div>
    </div>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { interfaceStyle } from "../../utils/MainIndex.ts";
// 创建可写的计算属性
const transparencyValue = computed({
    get: () => Math.round(interfaceStyle.value['interfaceTransparency'] * 100),
    set: (newValue: number) => {
        interfaceStyle.value['interfaceTransparency'] = newValue / 100;
        // 更新 CSS 变量
        document.documentElement.style.setProperty("--transparency", `${newValue / 100}`);
    }
});
</script>
<style scoped>
.draw-two-piece-main {
    font-family: "思印宋", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    font-size: 3vmin;
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
        height: 100%;
        width: 22.5%;
        max-width: 250px;
        background-color: rgba(var(--title), var(--transparency));
        border-right: 2px solid rgba(var(--font), var(--transparency));
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

            & input[type="range"] {
                -webkit-appearance: none;
                appearance: none;
                flex: 1;
                max-width: 300px;
                height: 1.5vmin;
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
    width: 25vmin;
    height: 8vmin;
    border-radius: 2vmin;
    background-color: rgba(var(--button), var(--pTransparency));
    z-index: 100;

    & .save-setting-button {
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
        &:hover{
            filter: brightness(1.1);
        }
        &:active{
            filter: brightness(1.35);

        }
    }
}
</style>