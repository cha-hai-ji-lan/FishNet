<template>
  <main class="container">
    <div data-tauri-drag-region class="main-head">
      这是头
    </div>
    <!-- <RouterView></RouterView> -->
  </main>
</template>
<script setup lang="ts">
// import { RouterView } from 'vue-router';

import { ref, onMounted } from "vue";
import { invoke } from "@tauri-apps/api/core";

import { init_app } from "./utils/MainIndex";

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
}

.main-head {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 5vh;
  width: 100%;
}
</style>
<style></style>