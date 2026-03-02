<template>
<div class="draw-two-piece-main">绘制四片式</div>
</template>
<script setup lang="ts"></script>
<style scoped>
.draw-two-piece-main{
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
</style>