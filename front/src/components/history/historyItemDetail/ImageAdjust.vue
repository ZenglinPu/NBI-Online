<template>
  <div id="singleImage_adjust-container">
    <div id="controlPanelPart">
      <div class="controlTitle">
        <div id="openFunctionContainer">
          <p style="padding-right: 5px;">图片调整</p>
          <div class="autoConsole">
            <div class="outerCon outerLeft" :class="consoleMode===0? selectedBtnLeft:''"><button class="consoleBtn consoleLeft" autofocus @click="switchConsoleMode(0)"><i class="el-icon-setting"></i>手动</button></div>
            <div class="outerCon outerRight" :class="consoleMode===1? selectedBtnRight:''"><button class="consoleBtn consoleRight" @click="switchConsoleMode(1)"><i class="iconfont icon-zhinengyouhua" style="font-weight: normal;"></i>智能</button></div>
          </div>
        </div>
      </div>
      <div id="mainControlPart">
        <div id="mainControlRange">
          <div class="mainControlRange_container">
            <div class="mainControlRange_title">
              <el-col :span="12">
                <div
                  style="width: 85%;height: 30%;display: flex;flex-direction: row;justify-content: start;align-items: center; padding-left: 20px;">
                  <p style="font-family: 幼圆,serif;">通道偏移调整：</p>
                  <div style="width: 30px;height: 100%;display: flex;justify-content: start;align-items: center">
                    <p style="color: #2244CC">{{ channelOffset }}</p>
                  </div>
                  <el-popover placement="top-start" width="100" trigger="hover"
                    content="通道偏移，手动调整输入图片强度，在自动调整的基础上可以进一步修改。自动调整使用后台算法调整输入图片强度，避免因为输入图片亮度不统一而造成的色彩偏移问题。">
                    <el-button style="cursor: help;margin-right: 10px;" size="small" slot="reference"
                      icon="el-icon-link" circle></el-button>
                  </el-popover>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="mainControlBtn">
                  <div
                    style="font-family: Arial, Helvetica, sans-serif;width:85%; display:flex;flex-direction: row; justify-content: right;align-items: center;">
                    <input type="checkbox" ref="isAutoChannel">
                    <p style="font-family: 幼圆,serif;">自动调整通道</p>
                  </div>
                </div>
              </el-col>
            </div>
            <div style="width:85%; height: 50%;display: flex;flex-direction: column;">
              <div style="width:100%; height: 30%;display: flex;flex-direction: row;">
                <p
                  style="height: 100%;font-size: small;width: 50%;text-align: left;color: rgb(255, 33, 33);font-family: Arial, Helvetica, sans-serif;">
                  红色增强</p>
                <p
                  style="height: 100%;font-size: small;width: 50%;text-align: right;color: rgb(0, 174, 255);font-family: Arial, Helvetica, sans-serif;">
                  青色增强</p>
              </div>
              <div
                style="width:100%; height: 70%;display: flex;flex-direction: row;align-items: center;justify-content: center">
                <input type="range" id="channelAdjustRange" min="-30" max="30" v-model="channelOffset">
              </div>
            </div>
          </div>
          <div class="mainControlRange_container">
            <div class="mainControlRange_title">
              <el-col :span="12">
                <div
                  style="width: 85%;height:30%;display: flex;flex-direction: row;justify-content: start;align-items: center; padding-left: 20px;">
                  <p style="font-family: 幼圆,serif;">亮度偏移调整：</p>
                  <div style="width: 30px;height: 100%;display: flex;justify-content: start;align-items: center">
                    <p style="color: #2244CC">{{ brightnessOffset }}</p>
                  </div>
                  <el-popover placement="top-start" width="100" trigger="hover"
                    content="亮度偏移，调整最终生成图片的亮度，在自动调整的基础上可以进一步修改。自动调整可使最终生成图片的亮度更适合观察。">
                    <el-button style="cursor: help;margin-right: 10px;" size="small" slot="reference"
                      icon="el-icon-link" circle></el-button>
                  </el-popover>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="mainControlBtn">
                  <div
                    style="font-family: Arial, Helvetica, sans-serif;width:85%; display:flex;flex-direction: row; justify-content: right;align-items: center;">
                    <input type="checkbox" ref="isAutoBrightness">
                    <p style="font-family: 幼圆,serif;">自动调整亮度</p>
                  </div>
                </div>
              </el-col>
            </div>
            <div style="width:85%; height: 50%;display: flex;flex-direction: column;">
              <div style="width:100%; height: 30%;display: flex;flex-direction: row;font-size: small;">
                <p style="width: 50%;text-align: left;font-family: Arial, Helvetica, sans-serif;">降低亮度</p>
                <p style="width: 50%;text-align: right;font-family: Arial, Helvetica, sans-serif;">提高亮度</p>
              </div>
              <div
                style="width:100%; height: 70%;display: flex;flex-direction: row;align-items: center;justify-content: center">
                <input type="range" id="brightnessAdjustRange" class="checke" min="-80" max="80"
                  v-model="brightnessOffset">
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="moreControlTitle" v-show="consoleMode===0">
        更多操作&emsp;
        <input type="checkbox" ref="isAdjustImage" @change="changeMoreFunctionActive()">
        <span>启用更多</span>
      </div>
      <div class="moreControlTitle" v-show="consoleMode===1">
        操作进度&emsp;
      </div>
      <div id="moreFunctionControlRange" :style="moreFunctionShow" v-show="consoleMode===0">
        <div class="adjustContainer">
          <div style="width: 20%;display: flex;justify-content: center;align-items: center;">
            <p style="font-family: 幼圆,serif ">&emsp;对比度</p>
            <!-- <el-popover placement="top-start" width="100" title="对比度" trigger="hover" content="拉大高低亮度像素的距离，提高图片明暗对比程度。">
              <el-button style="margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link"
                circle></el-button>
            </el-popover> -->
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
                {{contrastOffset}}</p>
              <el-button icon="el-icon-refresh-right" circle @click="contrastOffset=100"></el-button>
            </div>
          </div>
        </div>
        <div class="adjustContainer">
          <div style="width: 20%; height: 100%;display: flex;justify-content: center;align-items: center;">
            <p style="font-family: 幼圆,serif">明度</p>
            <!-- <el-popover placement="top-start" width="100" title="明度" trigger="hover" content="按SVD分解像素，高明度提高图片整体暗部。">
              <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference"
                icon="el-icon-link" circle></el-button>
            </el-popover> -->
          </div>
          <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
            <div
              style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低明度</p>
              <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高明度</p>
            </div>
            <div
              style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
              <input @change="showInfo()" type="range" id="luminosityAdjustRange" min="0" max="100"
                v-model="luminosityOffset">
              <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;overflow: hidden;">
                {{luminosityOffset}}</p>
              <el-button icon="el-icon-refresh-right" circle @click="luminosityOffset=100"></el-button>
            </div>
          </div>
        </div>
        <div class="adjustContainer">
          <div style="width: 20%; height: 100%;display: flex;justify-content: center;align-items: center;">
            <p style="font-family: 幼圆,serif">&emsp;饱和度</p>
            <!-- <el-popover placement="top-start" width="100" title="饱和度" trigger="hover" content="按SVD分解像素，高饱和度色彩更加鲜艳。">
              <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference"
                icon="el-icon-link" circle></el-button>
            </el-popover> -->
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
              <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;height: 100%;overflow: hidden;"
                id="saturationOffsetValue">{{saturationOffset}}</p>
              <el-button icon="el-icon-refresh-right" circle @click="saturationOffset=100"></el-button>
            </div>
          </div>
        </div>
      </div>
      <div class="progress-container" v-show="consoleMode===1">
        <div class="progress-status-inner">
            <el-steps direction="vertical" :active="-1" process-status="finish" finish-status="success">
                <el-step ref="el_step_channel" :title="this.showChannelOffset" icon="el-icon-setting"></el-step>
                <el-step title="生成图片" icon="el-icon-picture-outline-round"></el-step>
                <el-step title="自动调优" icon="el-icon-magic-stick"></el-step>
                <el-step ref="el_step_brightness" :title="this.showBrightnessOffset" icon="el-icon-setting"></el-step>
                <el-step title="更新数据" icon="el-icon-document-copy"></el-step>
            </el-steps>
        </div>
        <div class="progress-bar-inner">
          <el-progress type="dashboard" :percentage="percentage" :color="colors"></el-progress>
        </div>
      </div>
      <div id="generateBtn">
        <el-button v-show="isGenerating" id="getResultImage" type="primary" :loading="true">生成中</el-button>
        <button v-show="!isGenerating" id="getResultImage" @click="getResultImage()">重新生成</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ImageAdjust",
  props: ['GID'],
  data() {
    return {
      contrastOffset: 100,
      luminosityOffset: 100,
      saturationOffset: 100,
      channelOffset: 0,
      brightnessOffset: 0,
      isGenerating: false,
      isUploaded_fromSend: true,
      recordRealResult: "",
      imageResultSrc: "",
      moreFunctionActive: false,
      consoleMode: 0,
      selectedBtnLeft: 'selectedBtnLeft',
      selectedBtnRight: 'selectedBtnRight',
      percentage: 70,
      colors: [
        {color: '#f56c6c', percentage: 20},
        {color: '#e6a23c', percentage: 40},
        {color: '#5cb87a', percentage: 60},
        {color: '#1989fa', percentage: 80},
        {color: '#6f7ad3', percentage: 100}
      ]
    }
  },
  computed: {
    moreFunctionShow() {
      if (this.moreFunctionActive) {
        return { 'opacity': '1' };
      }
      else {
        return { 'opacity': '.4' };
      }
    },
    showChannelOffset(){
        return '调整通道：偏移为'+this.channelOffset
    },
    showBrightnessOffset(){
        return '调整亮度：偏移为'+this.brightnessOffset
    }
  },
  //   updated() {
  //     this.$bus.$emit("sendLastArg")
  //   },
  mounted() {
    this.getLastAdjustArg()

    //被emit后将数据送给infoFormPart->getAdjustImageInfo
    // this.$bus.$on("sendAdjustImageInfo", () => {
    //   const toSend = {
    //     "isOpen": this.$refs.isAdjustImage.checked,
    //     "contrastOffset": this.contrastOffset,
    //     "luminosityOffset": this.luminosityOffset,
    //     "saturationOffset": this.saturationOffset,
    //   };
    //   //发送数据到send
    //   this.$bus.$emit("getAdjustImageInfo", toSend);
    // })
    // this.$bus.$on("getlastArg", (data) => {
    //   this.saturationOffset = data.saturationOffset;
    //   this.contrastOffset = data.contrastOffset;
    //   this.luminosityOffset = data.luminosityOffset;
    //   console.log("我是adjust组件收到信息：", this.saturationOffset, this.contrastOffset)
    // })

    //这个数据总线getUploadedInfo貌似没啥用，考虑去掉？
    // this.$bus.$on("getUploadedInfo", (data) => {
    //   this.isUploaded_fromSend = data;
    // });

    // this.$bus.$on("sendLastArg", () => {
    //   const toSend = {
    //     "contrastOffset": this.fromAdjust.contrastOffset,
    //     "luminosityOffset": this.fromAdjust.luminosityOffset,
    //     "saturationOffset": this.fromAdjust.saturationOffset,
    //   };
    //   //发送数据到send
    //   this.$bus.$emit("getlastArg", toSend);
    // }) 

    // this.$bus.$on("getAdjustImageInfo", (data) => {
    //   this.fromAdjust.isOpen = data.isOpen;
    //   this.fromAdjust.contrastOffset = data.contrastOffset;
    //   this.fromAdjust.luminosityOffset = data.luminosityOffset;
    //   this.fromAdjust.saturationOffset = data.saturationOffset;
    // });
  },
  //   beforeDestroy() {
  //     this.$bus.$off("sendAdjustImageInfo");
  //     this.$bus.$off("getlastArg");

  //     // this.$bus.$off("getUploadedInfo");
  //     this.$bus.$off("getAdjustImageInfo");
  //     this.$bus.$off("sendLastArg");
  //   },
  methods: {
    changeMoreFunctionActive() {
      this.moreFunctionActive = !this.moreFunctionActive;
    },
    showInfo() {
      if (!this.$refs.isAdjustImage.checked) {
        this.$message({
          showClose: true,
          message: '仅有在勾选开启图片调整更多功能后该改动才能生效。',
          type: 'warning'
        });
      }
    },
    // cookie
    getCookie(objName) {//获取指定名称的cookie的值
      const arrStr = document.cookie.split("; ");
      for (let i = 0; i < arrStr.length; i++) {
        const temp = arrStr[i].split("=");
        if (temp[0] === objName) return temp[1];
      }
      return null;
    },
    getToken() {
      return this.getCookie("NBI_token");
    },
    getUID() {
      return this.getCookie("NBI_UID");
    },
    // checkUploaded() {
    //   // 发送信号给send让他调用我的事件，传输数据
    //   this.$bus.$emit("sendUploadedInfoToGet");
    // },
    //获取对比度等信息
    // getAdjustImageInfo() {
    //   this.$bus.$emit("sendAdjustImageInfo");
    // },
    getResultImage() {
      // this.checkUploaded();
      if (!this.isUploaded_fromSend) {
        this.$message({
          showClose: true,
          message: "请先完成图片上传",
          type: 'warning'
        });
        return;
      }
      this.isGenerating = true;
      //   this.getAdjustImageInfo();
      let getResultForm = new FormData();
      if (!this.moreFunctionActive) {
        //简单生成
        getResultForm.append("gid", this.GID)
        getResultForm.append("token", this.getToken());
        getResultForm.append("user", this.getUID());
        getResultForm.append("channelOffset", this.channelOffset);
        getResultForm.append("brightnessAdjust", this.brightnessOffset);
        getResultForm.append("isAutoChannel", this.$refs.isAutoChannel.checked);
        getResultForm.append("isAutoBrightness", this.$refs.isAutoBrightness.checked);
        getResultForm.append("mode", "easy")
      } else {
        getResultForm.append("gid", this.GID)
        getResultForm.append("token", this.getToken());
        getResultForm.append("user", this.getUID());
        getResultForm.append("channelOffset", this.channelOffset);
        getResultForm.append("brightnessAdjust", this.brightnessOffset);
        getResultForm.append("isAutoChannel", this.$refs.isAutoChannel.checked);
        getResultForm.append("isAutoBrightness", this.$refs.isAutoBrightness.checked);
        getResultForm.append("contrastOffset", this.contrastOffset);
        getResultForm.append("luminosityOffset", this.luminosityOffset);
        getResultForm.append("saturationOffset", this.saturationOffset);
        getResultForm.append("mode", "full");
      }
      let config = {
        headers: { 'Content-Type': 'multipart/form-data' }
      };
      this.$axios.post("/NBI/Image/getResult/", getResultForm, config).then((response) => {
        if (response.data === 1) {
          this.$message({
            showClose: true,
            message: '登录状态错误！',
            type: 'error'
          });
          this.$bus.$emit("changeStatus", { status: false, uname: '' });
        } else if (response.data === 2) {
          this.$message({
            showClose: true,
            message: '请求方式错误！',
            type: 'error'
          });
        } else if (response.data === 3) {
          this.$message({
            showClose: true,
            message: '图片处理错误！',
            type: 'error'
          });
        } else {
          this.updatePageNBIImage(response.data);
          this.brightnessOffset = parseInt(response.data.brightnessAdjustValue);
        }
        this.isGenerating = false;
      });
    },
    updatePageNBIImage(data) {
      this.imageResultSrc = data.resultImage;
      const toSend = {
        "imageNBIName": data.resultImage,
      };
      this.$bus.$emit("getAdjustImage", toSend)
    },
    getLastAdjustArg() {
      let config = {
        headers: { 'Content-Type': 'multipart/form-data' }
      };
      let getLastAdjustArgForm = new FormData();
      getLastAdjustArgForm.append("token", this.getToken());
      getLastAdjustArgForm.append("uid", this.getUID());
      getLastAdjustArgForm.append("gid", this.GID);
      this.$axios.post("/NBI/Image/getLastAdjustArg/", getLastAdjustArgForm, config).then((response) => {
        if (response.data === 1) {
          this.$message({
            showClose: true,
            message: '登录状态错误！',
            type: 'error'
          });
        } else {
          // console.log("getLastAdjustArg得到的数据是", response.data, this.fromAdjust)
          this.channelOffset = response.data.channelOffset;
          this.brightnessOffset = response.data.brightness;
          this.contrastOffset = response.data.contrast;
          this.saturationOffset = response.data.saturation;
          this.luminosityOffset = response.data.luminosity;
        }
      });
    },
    switchConsoleMode(newMod) {
      this.consoleMode = newMod;
      // console.log(newMod)
    }
  }
}
</script>

<style scoped>
#singleImage_adjust-container {
  width: 100%;
  height: 100%;
}

input[type="checkbox"] {
  height: 18px !important;
  width: 18px !important;
  border: 2px rgb(0, 94, 255);
  cursor: pointer;
}

#moreFunctionControlRange {
  width: 100%;
  height: 30%;
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

#luminosityAdjustRange {
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
  /* justify-content: center; */
  align-items: center;
  font-family: Arial, Helvetica, sans-serif;
}

.moreControlTitle span {
  font-size: 10px;
  color: #b6b6b6;
}

.moreControlTitle input {
  margin-top: 5px;
}

#controlPanelPart {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.adjustContainer {
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
}

.controlTitle {
  width: calc(100% - 20px);
  height: 40px;
  line-height: 40px;
  padding-left: 20px;
  font-weight: bold;
  /* border-left: 1px solid #e6e6e6; */
  /* border-right: 1px solid #e6e6e6; */
  background-image: linear-gradient(180deg, #fbfbff 0%, #fff 100%);
}

.moreControlTitle {
  width: 100%;
  height: 40px;
  line-height: 40px;
  padding-left: 20px;
  font-weight: bold;
  display: flex;
  align-items: center;
  font-family: Arial, Helvetica, sans-serif;
  margin-top: 31px;
}

#brightnessAdjustRange {
  background-image: linear-gradient(to right, rgb(0, 0, 0, 1), rgba(160, 160, 160, 0.2));
  ;
  border-radius: 10px;
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
}

#channelAdjustRange {
  background-image: linear-gradient(to right, rgb(183, 0, 0), rgb(0, 234, 255));
  ;
  border-radius: 10px;
  width: 100%;
  -webkit-appearance: none;
  height: 4px;
}

#mainControlPart {
  display: flex;
  flex-direction: column;
  height: 40%;
  justify-content: center;
  align-items: center;
}

#generateBtn {
  width: 100%;
  height: 68px;
  display: flex;
  /*flex-direction: column;*/
  justify-content: left;
  align-items: center;
}

.mainControlBtn {
  width: 100%;
  height: 25%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#mainControlRange {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: flex-start;
}

.mainControlRange_container {
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.mainControlRange_title {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

#getResultImage {
  height: 30px;
  width: 78px;
  padding: 7px 15px;
  font-size: 12px;
  margin-left: 9%;
  cursor: pointer;
  border-radius: 3px;
  background-color: #409eff;
  color: white;
  transition: 0.3s ease;
  overflow: hidden;
  border: none;
}

#getResultImage:hover {
  opacity: .8;
}


.autoConsole {
  margin-left: auto;
  margin-right: 15px;
}
.autoConsole button {
  border: none;
  outline: none;
}
.outerCon {
  width: 60px;
  height: 20px;
  display: inline-block;
  position: relative;
  transition: .3s ease;
}
.outerLeft {
  border-left: transparent 2px solid;
  /* border-top: transparent 2px solid; */
  border-radius: 6px 0 0 4px;
}
.selectedBtnLeft {
  border-left: #4b4b4b 2px solid;
  /* border-top: #4b4b4b 2px solid; */
}
.outerRight {
  border-right: transparent 2px solid;
  /* border-bottom: transparent 2px solid; */
  border-radius: 0 4px 6px 0;
}
.selectedBtnRight {
  border-right: #d9d9d9 2px solid;
  /* border-bottom: #d9d9d9 2px solid; */
}
.consoleBtn {
  cursor: pointer;
  width: 60px;
  height: 20px;
  font-size: 12px;
  font-weight: bold;
  letter-spacing: 1px;
  /* background-color: #f3f3f3; */
  opacity: 20%;
  transition: .3s ease;
}
.consoleBtn:active, .consoleBtn:focus {
  opacity: 100%;
}
.consoleLeft {
  border-radius: 4px 0 0 4px;
  color: #3a3a3a;
  background: linear-gradient(-75deg, transparent 6px, #f3f3f3 0) right;
  clip-path: polygon(
      0 0,
      100% 0,
      calc(100% - 6px) 100%,
      0 100%
  );
}
.consoleRight {
  border-radius: 0 4px 4px 0;
  color: #fff;
  background: linear-gradient(105deg, transparent 6px, #3a3a3a 0) left;
  clip-path: polygon(
      6px 0,
      100% 0,
      100% 100%,
      0 100%
  );
}
.consoleLeft:after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  transform: rotate(15deg);
  box-shadow: 0 0 10px 0px rgba(122, 122, 122, 0.55);
  bottom: -3px;
  right: -17px;
}
.consoleRight:before {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  transform: rotate(15deg);
  box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.55);
  top: -3px;
  left: -17px;
}
.iconfont {
  font-size: 12px;
}

.progress-container {
    flex-grow: 1; 
    height: 180px;
    z-index: 1;
    display: flex;
    overflow: hidden;
    flex-direction: row;
    justify-content: center;
    /* background: linear-gradient(180deg,rgba(255,255,255,0),#f5f5fc 5%); */
}
.progress-status-inner {
    width: calc(50% - 70px);
    height: calc(100% - 20px);
    padding: 10px 35px;
}
.progress-bar-inner {
    flex-grow: 1;
    height: 100%;
    position: relative
}
.progress-bar-inner .el-progress {
    position:absolute; 
    left:50%; 
    top:50%; 
    transform:translate(-50%,-50%);
}
.el-step >>> .el-step__title {
    font-size: 13px;
}
.el-step >>> .el-step__head {
    margin-right: 6px;
}
</style>
