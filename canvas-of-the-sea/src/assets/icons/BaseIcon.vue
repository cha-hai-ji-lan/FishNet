<template>
    <svg v-if="whichIcon === 'pin-ing'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <g>
            <line x2="515" y2="641" x1="513" y1="886" stroke-width="64" stroke-linecap="round" />
            <path d="M384 256H640L576 384 640 640H384L448 384z" stroke-linejoin="round" stroke-linecap="round"
                stroke-width="64" />
        </g>
    </svg>
    <svg v-if="whichIcon === 'pin'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <g transform="rotate(45 512 512)">
            <line x2="515" y2="641" x1="513" y1="886" stroke-width="64" stroke-linecap="round" />
            <path d="M384 256H640L576 384 640 640H384L448 384z" stroke-linejoin="round" stroke-linecap="round"
                stroke-width="64" />
        </g>
    </svg>
    <svg v-if="whichIcon === 'minimize'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <line x2="768" y2="512" x1="256" y1="512" stroke-width="64" stroke-linecap="round" />
    </svg>
    <svg v-if="whichIcon === 'maximize-max'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024"
        height="1024" viewBox="0 0 1024 1024">
        <g>
            <polyline points="576 256 768 256 768 442" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <polyline points="442 768 256 768 256 576" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <polyline points="768 576 768 768 576 768" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <polyline points="448 256 256 256 256 448" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <line x2="768" y2="768" x1="256" y1="256" stroke-width="64" stroke-linecap="round" />
            <line x2="256" y2="768" x1="768" y1="256" stroke-width="64" stroke-linecap="round" />
        </g>
        <circle r="96" cx="512" cy="512" />
    </svg>
    <svg v-else-if="whichIcon === 'maximize-min'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024"
        height="1024" viewBox="0 0 1024 1024">
        <g>
            <polyline points="576 256 768 256 768 442" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <polyline points="442 768 256 768 256 576" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <polyline points="768 576 512 512 576 768" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <polyline points="448 256 512 512 256 448" fill-opacity="1" stroke-width="64" stroke-linecap="round"
                stroke-linejoin="round" />
            <line x2="768" y2="768" x1="256" y1="256" stroke-width="64" stroke-linecap="round" />
        </g>
    </svg>
    <svg v-if="whichIcon === 'close'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <g>
            <line x2="768" y2="768" x1="256" y1="256" stroke-width="64" stroke-linecap="round" />
            <line x2="768" y2="256" x1="256" y1="768" stroke-width="64" stroke-linecap="round" />
            <circle r="96" cx="512" cy="512" />
        </g>
    </svg>
    <svg v-if="whichIcon === 'report-bug'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024"
        height="1024" viewBox="0 0 1024 1024">
        <g>
            <path
                d="M192 512v256c0 128 0 128 128 128h384c128 0 128 0 128-128v-256c0-32 0-96-64-128l-128.4-65c-128-63.2-148.2-52.8-254.6 0l-127.293277 63.168093c-64.406723 35.231907-65.706723 97.831907-65.706723 129.831907zM192 512l512 192c84.493151 31.684932 84.493 192 0 192m-181.7-261.6L832 512"
                stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M384 640h-128v96 96h128M256 736h100M420 736h64" fill="none" stroke-width="64"
                stroke-linecap="round" stroke-linejoin="round" />
        </g>
    </svg>
    <svg v-if="whichIcon === 'setting'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <g>
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(37 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(74 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(111 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(144 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(181 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(-37 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(-74 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(-111 512 512)" />
            <path d="M464 256h96s32 0 32-32l-32-128s0-16-16-16h-64s-16 0-16 16l-32 128s0 32 32 32z" stroke-width="64"
                fill="none" transform="rotate(-144 512 512)" />
            <path d="M416 512l32-64 64-32 64 32 32 64-32 64-64 32-64-32z" fill="none" stroke-width="64"
                stroke-linejoin="round" stroke-linecap="round" />
        </g>
    </svg>
    <svg v-if="whichIcon === 'github'" t="1775887870552" class="base-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
        p-id="5905" width="200" height="200">
        <path
            d="M511.6 76.3C264.3 76.2 64 276.4 64 523.5 64 718.9 189.3 885 363.8 946c23.5 5.9 19.9-10.8 19.9-22.2v-77.5c-135.7 15.9-141.2-73.9-150.3-88.9C215 726 171.5 718 184.5 703c30.9-15.9 62.4 4 98.9 57.9 26.4 39.1 77.9 32.5 104 26 5.7-23.5 17.9-44.5 34.7-60.8-140.6-25.2-199.2-111-199.2-213 0-49.5 16.3-95 48.3-131.7-20.4-60.5 1.9-112.3 4.9-120 58.1-5.2 118.5 41.6 123.2 45.3 33-8.9 70.7-13.6 112.9-13.6 42.4 0 80.2 4.9 113.5 13.9 11.3-8.6 67.3-48.8 121.3-43.9 2.9 7.7 24.7 58.3 5.5 118 32.4 36.8 48.9 82.7 48.9 132.3 0 102.2-59 188.1-200 212.9 23.5 23.2 38.1 55.4 38.1 91v112.5c0.8 9 0 17.9 15 17.9 177.1-59.7 304.6-227 304.6-424.1 0-247.2-200.4-447.3-447.5-447.3z"
            p-id="5906"></path>
    </svg>
</template>
<script setup lang="ts">
defineProps<{
    whichIcon: string
}>()
</script>
<style scoped>
.base-icon {
    height: 4vmin;
    max-height: 30px;
    width: 4vmin;
    max-width: 30px;
    margin-right: 2.5vmin;
    stroke: rgba(var(--button), 1);
    fill: rgba(var(--button), 1);

    &:hover {
        height: 3.5vmin;
        width: 3.5vmin;
        border: 0.25vmin dashed rgba(var(--button), 1);
    }

    &:active {
        stroke: rgba(var(--font), 1);

    }
}
</style>