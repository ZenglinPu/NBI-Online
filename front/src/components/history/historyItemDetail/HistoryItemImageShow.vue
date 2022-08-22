<template>
  <div style="height: 100%;width: 100%;display: flex;flex-direction: column;justify-content: center;align-items: center">
    <div style="height: 70%;margin-bottom: 5%;width: 90%">
      <img class="bigNBIImage" :src="bigNBIImageSrc">
    </div>
    <div style="height: 25%;width: 90%;display: flex;flex-direction: row;justify-content: space-between;align-items: center">
      <img class="srcImage" :src="blueImageSrc">
      <img class="srcImage" :src="greenImageSrc">
      <img class="srcImage" :src="whiteImageSrc">
    </div>
  </div>
</template>

<script>
export default {
  name: "HistoryItemImageShow",
  props: ["imageShowInfo"],
  data(){
    return {
      bigNBIImageSrc: "/static/Data/NBI/"+this.imageShowInfo.NBIImageName,
      greenImageSrc: "/static/Data/Green"+this.imageShowInfo.greenImageSrc,
      blueImageSrc: "/static/Data/Blue"+this.imageShowInfo.blueImageSrc,
      whiteImageSrc: "/static/Data/White"+this.imageShowInfo.whiteImageSrc,
    }
  }
}
</script>

<style scoped>

</style>