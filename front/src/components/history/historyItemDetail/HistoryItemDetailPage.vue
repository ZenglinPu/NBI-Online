<template>
    <div id="historyItemDetailContainer">
      <div id="detailTitleContainer">
        <div style="margin-left: 5%;height: 100%;width: 30%;font-family: 幼圆,serif;font-size: large;font-weight: bolder;display: flex;justify-content: start;align-items: center;color: #2a2a2a">
          <p>&emsp;&emsp;标本名称:&emsp;{{titleInfo.sampleName}}</p>
        </div>
        <div style="height: 100%;width: 20%;font-family: 幼圆,serif;font-size: small;font-weight: lighter;display: flex;justify-content: start;align-items: end;color: #00002c">
          <p>&emsp;&emsp;上传时间:&emsp;{{titleInfo.uploadTime}}</p>
          <p>&emsp;&emsp;过期时间:&emsp;{{titleInfo.expiresTime}}</p>
        </div>
        <div style="height: 100%;width: 40%;display: flex;justify-content: end;align-items: center;">
          <el-button style="width: 30%;height: 45%;display: flex;justify-content: center;align-items: center" type="danger" icon="el-icon-delete">删 除</el-button>
        </div>
      </div>
      <div id="detailInfoContainer">
        <div id="imageShowPart">
          <HistoryItemImageShow :imageShowInfo="imageShowInfo"></HistoryItemImageShow>
        </div>
        <div id="imageAdjustPart">

        </div>
      </div>
    </div>
</template>

<script>
// import HistoryImageInfo from './HistoryImageInfo.vue';
import HistoryItemImageShow from "@/components/history/historyItemDetail/HistoryItemImageShow";
export default {
  name: "HistoryItemDetailPage",
  props: ['GID'],
  components: {HistoryItemImageShow},
  data(){
    return{
      titleInfo:{
        sampleName: "",
        uploadTime: "",
        expiresTime: "",
      },
      imageShowInfo:{
        NBIImageName: "",
        src_blue: "",
        src_green: "",
        src_white: "",
      }
    }
  },
}
</script>

<style scoped>
#historyItemDetailContainer {
  width: 100%;
  height: 100%;
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#detailTitleContainer{
  width: 100%;
  height: 12%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  border-bottom: 2px solid #0b007e;
}
#detailInfoContainer{
  width: 90%;
  height: 88%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
#imageShowPart{
  width: 55%;
  height: 100%;
}
#imageAdjustPart{
  width: 45%;
  height: 100%;
  border-left: #0b007e solid 1px;
}
</style>