<template>
    <svg v-if="whichIcon === 'pin-ing'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <g>
            <line x2="515" y2="641" x1="513" y1="886" stroke-width="64" stroke-linecap="round" />
            <path d="M384 256H640L576 384 640 640H384L448 384z" stroke-linejoin="round" stroke-linecap="round"
                stroke-width="64" />
        </g>
    </svg>
    <svg  v-if="whichIcon === 'pin'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024" viewBox="0 0 1024 1024">
        <g transform="rotate(45 512 512)">
            <line x2="515"  y2="641" x1="513" y1="886" stroke-width="64" stroke-linecap="round" />
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
    <svg v-if="whichIcon === 'report-bug'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024" viewBox="0 0 1024 1024">
	<g>
		<path d="M192 512v256c0 128 0 128 128 128h384c128 0 128 0 128-128v-256c0-32 0-96-64-128l-128.4-65c-128-63.2-148.2-52.8-254.6 0l-127.293277 63.168093c-64.406723 35.231907-65.706723 97.831907-65.706723 129.831907zM192 512l512 192c84.493151 31.684932 84.493 192 0 192m-181.7-261.6L832 512" stroke-width="32" fill="none"  stroke-linecap="round" stroke-linejoin="round" />
		<path d="M384 640h-128v96 96h128M256 736h100M420 736h64" fill="none" stroke-width="36"  stroke-linecap="round" stroke-linejoin="round" />
	</g>
</svg>
</template>
<script setup lang="ts">
defineProps<{
    whichIcon: string
}>()
</script>