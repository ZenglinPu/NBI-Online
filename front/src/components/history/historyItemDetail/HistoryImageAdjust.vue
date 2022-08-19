<template>
  <div id="singleImage_adjust-container">
    <div id="controlPanelPart">
      <div style="height: 100%;width: 18%;font-size: small;font-family: 幼圆,serif;">
        <div id="openFunctionContainer">
          <p style="padding-left: 3%;padding-right: 5px;">开启图片调整功能</p>
          <input type="checkbox" ref="isAdjustImage">
        </div>
      </div>
      <div id="moreFunctionControlRange">
        <div class="adjustContainer">
          <div style="width: 20%;display: flex;justify-content: center;align-items: center;">
            <p style="font-family: 幼圆,serif ">&emsp;&emsp;对比度</p>
            <el-popover placement="top-start" width="100" title="对比度" trigger="hover" content="拉大高低亮度像素的距离，提高图片明暗对比程度。">
              <el-button style="margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link"
                circle></el-button>
            </el-popover>
          </div>
          <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
            <div
              style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低对比度</p>
              <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高对比度</p>
            </div>
            <div
              style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <input @change="showInfo()" type="range" id="contrastAdjustRange" min="0" max="200"
                v-model="contrastOffset">
              <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;overflow: hidden;">
                {{ contrastOffset }}</p>
              <el-button icon="el-icon-refresh-right" circle @click="contrastOffset = 100"></el-button>
            </div>
          </div>
        </div>
        <div class="adjustContainer">
          <div style="width: 20%; height: 100%;display: flex;justify-content: center;align-items: center;">
            <p style="font-family: 幼圆,serif">&emsp;&emsp;&emsp;明度</p>
            <el-popover placement="top-start" width="100" title="明度" trigger="hover" content="按SVD分解像素，高明度提高图片整体暗部。">
              <el-button style="margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link"
                circle></el-button>
            </el-popover>
          </div>
          <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
            <div
              style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低明度</p>
              <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高明度</p>
            </div>
            <div
              style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <input @change="showInfo()" type="range" id="numinosityAdjustRange" min="0" max="200"
                v-model="luminosityOffset">
              <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;overflow: hidden;">
                {{ luminosityOffset }}</p>
              <el-button icon="el-icon-refresh-right" circle @click="luminosityOffset = 100"></el-button>
            </div>
          </div>
        </div>
        <div class="adjustContainer">
          <div style="width: 20%; height: 100%;display: flex;justify-content: center;align-items: center;">
            <p style="font-family: 幼圆,serif">&emsp;&emsp;饱和度</p>
            <el-popover placement="top-start" width="100" title="饱和度" trigger="hover" content="按SVD分解像素，高饱和度色彩更加鲜艳。">
              <el-button style="margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link"
                circle></el-button>
            </el-popover>
          </div>
          <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
            <div
              style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低饱和度</p>
              <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高饱和度</p>
            </div>
            <div
              style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <input @change="showInfo()" type="range" id="saturationAdjustRange" min="0" max="200"
                v-model="saturationOffset">
              <p style="font-family: STHeiti;margin-left: 12px; color: #264b5d; width: 50px;height: 100%;overflow: hidden;"
                id="saturationOffsetValue">{{ saturationOffset }}</p>
              <el-button icon="el-icon-refresh-right" circle @click="saturationOffset = 100"></el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HistoryImageAdjust",
  data() {
    return {
      contrastOffset: 100,
      luminosityOffset: 100,
      saturationOffset: 100,
    }
  },
  mounted() {
    this.$bus.$on("sendAdjustImageInfo", () => {
      const toSend = {
        "isOpen": this.$refs.isAdjustImage.checked,
        "contrastOffset": this.contrastOffset,
        "luminosityOffset": this.luminosityOffset,
        "saturationOffset": this.saturationOffset,
      };
      //发送数据到send
      this.$bus.$emit("getAdjustImageInfo", toSend);
    })
  },
  beforeDestroy() {
    this.$bus.$off("sendAdjustImageInfo");
  },
  methods: {
    showInfo() {
      if (!this.$refs.isAdjustImage.checked) {
        this.$message({
          message: '仅有在勾选开启图片调整功能后该改动才能生效。',
          type: 'warning'
        });
      }
    },
  }
}
</script>

<style scoped>
#singleImage_adjust-container {
  width: 100%;
  height: 100%;
}

input[type="checkbox"] {
  height: 18px;
  width: 18px;
  border: 2px rgb(0, 94, 255);
  cursor: pointer;
}

#moreFunctionControlRange {
  width: 85%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
}

#contrastAdjustRange {
  background-color: rgb(0, 0, 66);
  border-radius: 10px;
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
  margin-top: 20px;
}

#numinosityAdjustRange {
  background-color: rgb(0, 0, 66);
  border-radius: 10px;
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
  margin-top: 20px;
}

#saturationAdjustRange {
  background-color: rgb(0, 0, 66);
  border-radius: 10px;
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
  margin-top: 20px;
}

#openFunctionContainer {
  width: 100%;
  height: 100%;
  display: flex;
  border-right: 1px gray solid;
  justify-content: center;
  align-items: center;
  font-family: Arial, Helvetica, sans-serif;
}

#controlPanelPart {
  width: 100%;
  height: 100%;
  padding-top: 5px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}

.adjustContainer {
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
  border-top: #bdbdbd 1px solid;
  border-bottom: #bdbdbd 1px solid;
}
</style>
