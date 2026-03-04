<template>
  <div class="draw-two-piece-main">
    <div class="left-part">
      <div class="canvas-switch" @click="() => { show_canvas() }">{{ showCanvas ? "隐藏画布" : "显示画布" }}</div>
      <canvas class="two-piece-canvas"></canvas>
    </div>
    <div class="mid-part"></div>
    <div class="right-part" :class="{ 'show-canvas': showCanvas }">
      <div class="canvas-switch" @click="() => { show_canvas() }">{{ showCanvas ? "隐藏画布" : "显示画布" }}</div>
      <canvas class="two-piece-canvas"></canvas>
    </div>
  </div>
  <div class="float-option-version" :class="{ 'show-option-version': choosePart }">
    <div class="choose-column ban-select" @click="() => { show_part() }">{{ choosePart ? "取消选择" : "部位选择" }}</div>
    <div class="choose-part">
      <div class="blank-10p"></div>
      <div>
        <span @click="() => { }">
          <NetShowIcons whichIcon="left-sleeve"></NetShowIcons>
        </span>
        <span @click="() => { }">
          <NetShowIcons whichIcon="right-sleeve"></NetShowIcons>
        </span>
      </div>
      <div>
        <span @click="() => { }">
          <NetShowIcons whichIcon="net-body"></NetShowIcons>
        </span>
      </div>
      <div class="blank-10p"></div>
    </div>
  </div>
</template>
<script setup lang="ts">

import { ref } from 'vue';
import NetShowIcons from '../../assets/icons/NetShowIcons.vue';
const choosePart = ref(false)
const showCanvas = ref(false)
const show_part = () => {
  if (choosePart.value) {
    choosePart.value = false;
  } else {
    choosePart.value = true;
  }
}
const show_canvas = () => {
  if (showCanvas.value) {
    showCanvas.value = false;
  } else {
    showCanvas.value = true;
  }
}
</script>
<style scoped>
.draw-two-piece-main {
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: row;
  width: 100%;
  flex: 1%;
  /* height: 95vh; */
  background-color: var(--background);
  /* background-color: rgba(33, 40, 48, 1); */
  /* 淡灰色底色 */
  background-image:
    linear-gradient(to right, var(--border-line) 1px, transparent 1px),
    linear-gradient(to bottom, var(--border-line) 1px, transparent 1px);
  /* 创建虚线网格 */
  background-size: var(--grid-size) var(--grid-size);
}

.float-option-version {
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: row;
  position: absolute;
  bottom: 0;
  right: 0;
  height: 95vh;
  width: 4.5vmin;
  z-index: 10;
  transition: width 0.75s ease;
  pointer-events: none;

  &.show-option-version {
    width: 40vmin
  }

  & .choose-column {
    font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    writing-mode: vertical-rl;
    /* 从上到下，从右到左 */
    text-orientation: upright;
    /* 保持字符直立 */
    background: var(--title);
    border: 2px solid var(--font);
    border-right: 0px solid var(--font);
    border-radius: 1vmin 0 0 2.5vmin;
    padding: 1vmin;
    /* padding-right: 0.5vmin; */
    pointer-events: auto
  }

  & .choose-part {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background: var(--title);
    border-left: 2px solid var(--font);
    border-radius: 2.5vmin 0 0 2.5vmin;
    height: 100%;
    pointer-events: auto
  }
}



.left-part {
  flex: 1;
}

.right-part {
  width: fit-content;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  height: 100%;

  /* 让canvas出现过渡自然 */
  &.show-canvas {
    & .two-piece-canvas {
      transition: width 0.75s ease;
      width: 40vmin;
    }
  }

  & .canvas-switch {
    font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
    width: fit-content;
    writing-mode: vertical-rl;
    text-orientation: upright;
    margin-bottom: 20vmin;
    background: var(--title);
    border: 2px solid var(--font);
    border-right: 0px solid var(--font);
    border-radius: 2.5vmin 0 0 1vmin;
    padding: 1vmin;
  }

  & .two-piece-canvas {
    background: var(--title);
    transition: width 0.75s ease;
    height: 100%;
    width: 0vmin;
    border-left: 2px solid var(--font);
    border-radius: 2.5vmin 0 0 2.5vmin;
    background-image:
      linear-gradient(to right, var(--border-line) 1px, transparent 1px),
      linear-gradient(to bottom, var(--border-line) 1px, transparent 1px);
    /* 创建虚线网格 */
    background-size: var(--grid-size) var(--grid-size);
  }

}
</style>