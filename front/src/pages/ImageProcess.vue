<template>
  <div id="imageProcessPage-container">
    <div id="sideFunction-container">
      <Side :singleOrMulti="singleOrMulti" :whichProcessType="whichProcessType"></Side>
    </div>
    <div id="mainImageProcess-container">
      <div style="width: 100%;height: 100%; display: flex;justify-content: center;align-items: center" v-show="whichProcessType === 0">
        <p style="font-weight: bolder">/*请选择图片处理方式*/</p>
      </div>
      <router-view v-show="whichProcessType !== 0"></router-view>
    </div>
  </div>
</template>

<script>
import Side from "@/components/ImageProcess_Side"

export default {
  name: "P_ImageProcess",
  components:{
    Side,
  },
  methods:{
    singleOrMulti(w){
      if (w===1){
        this.$router.push({path: "/ImageProcess/SingleImage"});
        this.whichProcessType = 1;
      }
      else if (w===2){
        this.$router.push({path: "/ImageProcess/MultiImage"});
        this.whichProcessType = 2;
      }
    }
  },
  data(){
    return {
      whichProcessType:0,
    }
  }
}
</script>

<style scoped>
#imageProcessPage-container{
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}
#sideFunction-container{
  width: 12%;
  height: 100%;
}
#mainImageProcess-container{
  width: 88%;
  height: 100%;
  overflow: auto;
  background-color: #F8F8FF;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>