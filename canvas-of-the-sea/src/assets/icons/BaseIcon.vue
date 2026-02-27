<template>
    <svg v-if="whichIcon === 'pin'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024" viewBox="0 0 1024 1024">
	<g>
		<line x2="515"  y2="641" x1="513" y1="886" stroke-width="64" stroke-linecap="round" />
		<path d="M384 256H640L576 384 640 640H384L448 384" stroke-linejoin="round" stroke-linecap="round" stroke-width="64" />
	</g>
</svg>
    <svg v-if="whichIcon === 'minimize'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <line x2="768" y2="512" x1="256" y1="512" stroke-width="64" stroke-linecap="round" />
    </svg>
    <svg v-if="whichIcon === 'maximize'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
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
    <svg v-if="whichIcon === 'close'" xmlns="http://www.w3.org/2000/svg" class="base-icon" width="1024" height="1024"
        viewBox="0 0 1024 1024">
        <g>
            <line x2="768" y2="768" x1="256" y1="256" stroke-width="64" stroke-linecap="round" />
            <line x2="768" y2="256" x1="256" y1="768" stroke-width="64" stroke-linecap="round" />
            <circle r="96" cx="512" cy="512" />
        </g>
    </svg>
</template>
<script setup lang="ts">
defineProps<{
    whichIcon: string
}>()
</script>