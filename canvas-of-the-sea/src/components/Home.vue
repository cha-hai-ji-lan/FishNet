<template>
  <div class="home-main">
    <div class="blank"></div>
    <div class="flex-r-div"><img class="main-icon" src="../assets/icon.png" alt="">
      <h1>Canvas of the sea</h1>
      <div class="app-version">0.1.5</div>
    </div>
    <div class="flex-r-div home-subtitle">{{welcomeTitle}} 欢迎回来.{{ careTitle }}</div>
    <div class="flex-r-div"><NormalIcons whichIcon="newFile"></NormalIcons></div>


  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import NormalIcons from '../assets/icons/NormalIcons.vue';
// 响应式变量存储当前时间
const currentTime = ref('');
const welcomeTitle = ref("__WELCOME_SENTENCES__")
const careTitle = ref("") // __CARE_SENTENCES__

onMounted(() => {
  updateTime(); // 立即更新一次时间
});
const updateTime = () => {
  const now = new Date().getHours();
  currentTime.value = now.toLocaleString(); // 格式化时间为本地字符串
  if (Number(currentTime.value) >= 4 && Number(currentTime.value) <= 9) {
    welcomeTitle.value = "🌅早上好";
    careTitle.value = "又是元气满满的一天";
  } else if (Number(currentTime.value) > 9 && Number(currentTime.value) < 12) {
    welcomeTitle.value = "☀️上午好";
    careTitle.value = "清醒头脑,才思泉涌";
  } else if (Number(currentTime.value) >= 12 && Number(currentTime.value) < 15) {
    welcomeTitle.value = "🌞午间好";
    careTitle.value = "加油!";
  } else if (Number(currentTime.value) >= 15 && Number(currentTime.value) < 18) {
    welcomeTitle.value = "🌇下午好";
    careTitle.value = "祝你工作顺利完成,早点结束";
  } else if (Number(currentTime.value) >= 18 && Number(currentTime.value) < 24) {
    welcomeTitle.value = "⭐️晚上好";
    careTitle.value = "熬夜会损害我们的健康,注意早点休息";
  } else if (Number(currentTime.value) >= 0 && Number(currentTime.value) < 4) {
    welcomeTitle.value = "🌙午夜好";
    careTitle.value = "已经到凌晨了,这么晚工作对身体不好早点休息吧";
  }
  console.log(currentTime.value)
};

</script>
<style scoped>
h1 {
  font-size: 6vmin;
  margin-left: 2vmin;
  font-family: "Judou-Heavy", "宋体", "Microsoft YaHei", "微软雅黑", "SimSun", sans-serif;
}

.home-main {
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

.blank {
  width: 100%;
  height: 17.5%;
}

.main-icon {
  width: 20vmin;
  height: 20vmin;
}

.flex-r-div {
  display: flex;
  align-items: center;
  justify-content: start;
  flex-direction: row;
}

.app-version {
  margin-left: 2vmin;
  width: fit-content;
  height: fit-content;
  border: 2px solid #1177bb;
  border-radius: 2vmin;
  padding: 0.5vmin 1vmin;
  font-size: 3.5vmin;
}

.home-subtitle {
  font-size: 2.75vmin;
}
</style>