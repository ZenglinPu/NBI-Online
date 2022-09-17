<template>
  <div id="imgShowPart">
    <div class="imgPart_inner" style="height: 100%;">
      <div class="additionTitle">附加信息</div>
      <div style="width: 100%;height:100%;display:flex;justify-content: left;">
        <el-scrollbar id="additionInfoForm">
          <!-- 滚动条 -->
          <HistoryImageInfo :GID="this.GID"></HistoryImageInfo>
        </el-scrollbar><!-- /滚动条 -->
      </div>
    </div>
  </div>
</template>

<script>
import HistoryImageInfo from "@/components/history/historyItemDetail/HistoryImageInfo";

export default {
  name: "ImageInfoFormPart",
  components: { HistoryImageInfo },
  props: ['GID'],
}
</script>

<style scoped>
#imgShowPart {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  /* border-bottom: 1px grey solid; */
}

.imgPart_inner {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: column;
}

.additionTitle {
  height: 40px;
  line-height: 40px;
  padding-left: 20px;
  font-weight: bold;
  border-left: 1px solid #e6e6e6;
  border-right: 1px solid #e6e6e6;
  background-image: linear-gradient(180deg, #fbfbff 0%, #fff 100%);
}

#additionInfoForm {
  width: 100%;
  height: 100%;
  /* background-color: rgba(126, 126, 126, 0.25); */
  padding-top: 20px;
  border-left: 1px solid #e6e6e6;
  border-right: 1px solid #e6e6e6;
  /* border-radius: 40px; */
  font-family: STHeiti, serif;
  color: #363636;
  display: flex;
  justify-content: center;
  /*align-items: center;*/
  font-weight: bold;
  transition: 0.3s;
}
</style>