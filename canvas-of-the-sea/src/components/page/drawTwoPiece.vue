<template>
  <div class="draw-two-piece-main"></div>
  <div class="float-option-version" :class="{'show-option-version': choosePart}">
    <div class="choose-column ban-select" @click="() => { show_part() }">{{ choosePart?"取消选择":"部位选择"}}</div>
    <div class="choose-part">
    <div class="blank-10p"></div>
    <div></div>
    <div></div>
    <div></div>
    <div class="blank-10p"></div>
    </div>
  </div>
</template>
<script setup lang="ts">

import { ref } from 'vue';
const choosePart = ref(false)
const show_part = () => {
  if (choosePart.value ){
  choosePart.value = false;
  } else {
    choosePart.value = true;
  }
}
</script>
<style scoped>
.draw-two-piece-main {
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: column;
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
  width: 3.9vmin;
  z-index: 10;
  transition: width 0.75s ease;
  &.show-option-version {
    width:40vmin
  }
}

.choose-column {
  font-family: "荆南圆体", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
  writing-mode: vertical-rl;
  /* 从上到下，从右到左 */
  text-orientation: upright;
  /* 保持字符直立 */
  background: var(--title);
  border: 2px solid var(--font);
  border-right: 0px solid var(--font);
  border-radius: 2.5vmin 0 0 2.5vmin;
  padding: 1vmin;
  padding-right: 0.5vmin;
}

.choose-part {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background: var(--title);
  border: 2px solid var(--font);
  border-right: 0px solid var(--font);
  border-radius: 2.5vmin 0 0 2.5vmin;
  height: 100%;
}
</style>