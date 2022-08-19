<template>
    <div id="historyItem-container">
        <div id="historyImageInfoContainer">
            <HistoryImageInfo />
        </div>
        <div id="imageShowPartContainer">
            <div style="width: 100%;height: 70%">
                <HistoryImageGetPart />
            </div>
            <div style="width: 100%;height: 30%">
                <HistoryImageAdjust />
            </div>
        </div>
    </div>
</template>

<script>
import HistoryImageAdjust from './HistoryImageAdjust.vue';
import HistoryImageGetPart from './HistoryImageGetPart.vue';
import HistoryImageInfo from './HistoryImageInfo.vue';
export default {
    name: "HistoryItemPage",
    components: { HistoryImageAdjust, HistoryImageGetPart, HistoryImageInfo }
}
</script>

<style scoped>
#historyItem-container {
    width: 100%;
    height: 100%;
    overflow: auto;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

#historyImageInfoContainer {
    width: 40%;
    height: 100%;
    border: 1px rgb(0, 149, 255) solid;
    border-right: none;
}

#imageShowPartContainer {
    width: 60%;
    height: 100%;
    border: 1px rgb(0, 149, 255) solid;
}
</style>