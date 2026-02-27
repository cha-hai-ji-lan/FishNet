<template>
  <main class="container">
    <div data-tauri-drag-region class="main-head">
      <div class="title-head left-head"></div>
      <div class="title-head mid-head"></div>
      <div class="title-head right-head">
        <BaseIcon whichIcon="pin"></BaseIcon>
        <BaseIcon whichIcon="minimize"></BaseIcon>
        <BaseIcon whichIcon="maximize"></BaseIcon>
        <BaseIcon whichIcon="close"></BaseIcon>
      </div>

    </div>
    <RouterView></RouterView>
  </main>
</template>
<script setup lang="ts">

import { ref, onMounted } from "vue";
import { RouterView } from 'vue-router';
import { invoke } from "@tauri-apps/api/core";

import { init_app } from "./utils/MainIndex";
import BaseIcon from "./assets/icons/BaseIcon.vue";

onMounted(async () => {
  await init_app();
})

</script>



<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* border: 0.25vmin solid #fff */
}

.main-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 5vh;
  width: 100%;
  background: var(--title);
}

.title-head {
  width: calc(100% / 3);
}

.right-head {
  display: flex;
  align-items: center;
  justify-content: end;
  margin-right: 1vmin;
}
</style>
<style>
html {
  padding: 0;
  margin: 0;
  font: 1.75vmin "宋体", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-weight: 500;
  color: var(--font);
  width: 100vw;
  height: 100vh;
}

body {
  padding: 0;
  margin: 0;
}

.base-icon {
  height: 4vmin;
  width: 4vmin;
  margin-right: 2vmin;
  stroke: var(--button);
  fill: var(--button);

  &:hover {
    border: 0.25vmin dashed var(--button);
  }
}
</style>