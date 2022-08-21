<template>
  <div id="imgShowPart">
    <div class="subTitle">
      <p style="height: 50%;font-family: STHeiti,serif;color: #363636;display: flex;justify-content: center;align-items: center;margin: 0 0 0 2%;">生成结果(Get Result):</p>
      <div style="width: 100%;height: 50%;display: flex;flex-direction: row;">
        <div style="width: 60%;height: 100%;display: flex;flex-direction: row;">
          <el-button v-show="isGenerating" id="getResultImage" type="primary" :loading="true">生成中</el-button>
          <button v-show="!isGenerating" id="getResultImage" @click="getResultImage()">生成图片</button>
<!--          TODO-->
          <button id="saveImage">保存结果</button>
          <el-popover
            placement="top-start"
            width="100"
            trigger="hover"
            content="是否在历史记录中保存此次提交，未保存的数据仅会在历史记录中保存24小时！">
            <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
          </el-popover>
        </div>
        <div style="height: 100%;width: 40%;display: flex;justify-content: end;">
          <el-button id="downloadResult" type="warning" icon="el-icon-download" @click="downloadResult()">下载结果</el-button>
        </div>
      </div>
    </div>
    <div class="imgPart_inner" style="height: 340px;margin-top: 10px;">
        <div style="width: 100%;height:100%;display:flex;justify-content: left;align-items: center;">
            <div id="imgBackPart">
                <p id="outImageDefault" v-show="!isShowResult">/*生成图片后查看结果*/</p>
                <img v-show="isShowResult" :src="imageResultSrc" id="ShowResult" alt="图片加载错误">
            </div>
            <div id="mainControlPart">
                <div id="mainControlBtn">
                  <div style="font-family: Arial, Helvetica, sans-serif;width:85%; display:flex;flex-direction: row;height:20%; justify-content: center;align-items: center;">
                    <el-popover
                      placement="top-start"
                      width="100"
                      trigger="hover"
                      content="使用后台算法自动调整输入图片强度，避免因为输入图片亮度不统一而造成的色彩偏移问题。">
                      <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                    </el-popover>
                    <p style="font-family: 幼圆,serif;">自动调整通道</p>
                    <input type="checkbox" ref="isAutoChannel">
                  </div>
                  <div style="margin-top: 25px;font-family: Arial, Helvetica, sans-serif;width:85%; display:flex;flex-direction: row;height:20%; justify-content: center;align-items: center;">
                    <el-popover
                      placement="top-start"
                      width="100"
                      trigger="hover"
                      content="自动调整最终生成图片的亮度，更适合观察">
                      <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                    </el-popover>
                    <p style="font-family: 幼圆,serif;">自动调整亮度</p>
                    <input type="checkbox" ref="isAutoBrightness">
                  </div>
                </div>
                <div id="mainControlRange">
                  <div class="mainControlRange_container">
                    <div style="width: 85%;height: 30%;display: flex;flex-direction: row;justify-content: start;align-items: center">
                      <p style="font-family: 幼圆,serif;">通道偏移调整：</p>
                      <div style="width: 30px;height: 100%;display: flex;justify-content: start;align-items: center">
                        <p style="color: #2244CC">{{channelOffset}}</p>
                      </div>
                      <el-popover
                        placement="top-start"
                        width="100"
                        trigger="hover"
                        content="通道偏移，手动调整输入图片强度，在自动调整的基础上可以进一步修改。">
                        <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                      </el-popover>
                    </div>
                    <div style="width:85%; height: 50%;display: flex;flex-direction: column;">
                        <div style="width:100%; height: 30%;display: flex;flex-direction: row;">
                            <p style="height: 100%;font-size: small;width: 50%;text-align: left;color: rgb(255, 33, 33);font-family: Arial, Helvetica, sans-serif;">红色增强</p>
                            <p style="height: 100%;font-size: small;width: 50%;text-align: right;color: rgb(0, 174, 255);font-family: Arial, Helvetica, sans-serif;">青色增强</p>
                        </div>
                        <div style="width:100%; height: 70%;display: flex;flex-direction: row;align-items: center;justify-content: center">
                            <input type="range" id="channelAdjustRange" min="-30" max="30" v-model="channelOffset">
                        </div>
                    </div>
                  </div>
                  <div class="mainControlRange_container">
                    <div style="width: 85%;height:30%;display: flex;flex-direction: row;justify-content: start;align-items: center">
                      <p style="font-family: 幼圆,serif;">亮度偏移调整：</p>
                      <div style="width: 30px;height: 100%;display: flex;justify-content: start;align-items: center">
                        <p style="color: #2244CC">{{brightnessOffset}}</p>
                      </div>
                      <el-popover
                        placement="top-start"
                        width="100"
                        trigger="hover"
                        content="亮度偏移，调整最终生成图片的亮度，在自动调整的基础上可以进一步修改。">
                        <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                      </el-popover>
                    </div>
                    <div style="width:85%; height: 50%;display: flex;flex-direction: column;">
                        <div style="width:100%; height: 30%;display: flex;flex-direction: row;font-size: small;">
                            <p style="width: 50%;text-align: left;font-family: Arial, Helvetica, sans-serif;">降低亮度</p>
                            <p style="width: 50%;text-align: right;font-family: Arial, Helvetica, sans-serif;">提高亮度</p>
                        </div>
                        <div style="width:100%; height: 70%;display: flex;flex-direction: row;align-items: center;justify-content: center">
                            <input type="range" id="brightnessAdjustRange" class="checke" min="-80" max="80" v-model="brightnessOffset">
                        </div>
                    </div>
                  </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "singleImageProcess_imageGetPart",
  data(){
    return{
      channelOffset: 0,
      brightnessOffset: 0,
      isGenerating: false,
      isUploaded_fromSend: false,
      fromAdjust:{
        isOpen: false,
        contrastOffset: 0,
        luminosityOffset: 0,
        saturationOffset: 0,
      },
      recordRealResult: "",
      isShowResult: false,
      imageResultSrc: "",
    }
  },
  mounted() {
    this.$bus.$on("getUploadedInfo",(data)=>{
      this.isUploaded_fromSend = data;
    });
    this.$bus.$on("getAdjustImageInfo", (data)=>{
      this.fromAdjust.isOpen = data.isOpen;
      this.fromAdjust.contrastOffset = data.contrastOffset;
      this.fromAdjust.luminosityOffset = data.luminosityOffset;
      this.fromAdjust.saturationOffset = data.saturationOffset;
    });
  },
  beforeDestroy() {
    this.$bus.$off("getUploadedInfo");
    this.$bus.$off("getAdjustImageInfo");
  },
  methods:{
    // cookie
    getCookie(objName){//获取指定名称的cookie的值
      const arrStr = document.cookie.split("; ");
      for(let i = 0; i < arrStr.length; i ++){
        const temp = arrStr[i].split("=");
        if(temp[0] === objName) return temp[1];
      }
      return null;
    },
    getToken(){
      return this.getCookie("NBI_token");
    },
    getUID(){
      return this.getCookie("NBI_UID");
    },
    checkUploaded(){
      // 发送信号给send让他调用我的事件，传输数据
      this.$bus.$emit("sendUploadedInfoToGet");
    },
    getAdjustImageInfo(){
      this.$bus.$emit("sendAdjustImageInfo");
    },
    getResultImage(){
      this.checkUploaded();
      if (!this.isUploaded_fromSend){
        this.$message({
          showClose: true,
          message: "请先完成图片上传",
          type: 'warning'
        });
        return;
      }
      this.isGenerating = true;
      this.getAdjustImageInfo();
      let getResultForm = new FormData();
      if (!this.fromAdjust.isOpen){
        //简单生成
        getResultForm.append("token", this.getToken());
        getResultForm.append("user", this.getUID());
        getResultForm.append("channelOffset", this.channelOffset);
        getResultForm.append("brightnessAdjust", this.brightnessOffset);
        getResultForm.append("isAutoChannel", this.$refs.isAutoChannel.checked);
        getResultForm.append("isAutoBrightness", this.$refs.isAutoBrightness.checked);
        getResultForm.append("mode", "easy")
      }
      else{
        getResultForm.append("token", this.getToken());
        getResultForm.append("user", this.getUID());
        getResultForm.append("channelOffset", this.channelOffset);
        getResultForm.append("brightnessAdjust", this.brightnessOffset);
        getResultForm.append("isAutoChannel", this.$refs.isAutoChannel.checked);
        getResultForm.append("isAutoBrightness", this.$refs.isAutoBrightness.checked);
        getResultForm.append("contrastOffset", this.fromAdjust.contrastOffset);
        getResultForm.append("luminosityOffset", this.fromAdjust.luminosityOffset);
        getResultForm.append("saturationOffset", this.fromAdjust.saturationOffset);
        getResultForm.append("mode", "full");
      }
      let config = {
         headers: {'Content-Type': 'multipart/form-data'}
      };
      this.$axios.post("/NBI/Image/getResult/",getResultForm, config).then((response) => {
        if (response.data === 1){
            this.$message({
              showClose: true,
              message: '登录状态错误！',
              type: 'error'
            });
        }
        else if (response.data === 2){
          this.$message({
            showClose: true,
            message: '请求方式错误！',
            type: 'error'
          });
        }
        else if (response.data === 3){
          this.$message({
            showClose: true,
            message: '图片处理错误！',
            type: 'error'
          });
        }
        else{
            this.showResultImage(response.data);
        }
        this.isGenerating = false;
      });
    },
    downloadResult(){
        // 检查是否存在生成图片
        if (this.recordRealResult === ""){
          this.$message({
            showClose: true,
            message: '请先点击生成图片！',
            type: 'error'
          });
          return -1;
        }
        this.$message({
          showClose: true,
          message: '已开始下载。',
          type: 'success',
        });
        this.downloadImage("/static/Data/NBI/"+this.recordRealResult, "resultNBI.jpg");
    },
    downloadImage(imgSrc, fileName){
        var alink = document.createElement("a");
        alink.href = imgSrc;
        alink.download = fileName; //fileName保存提示中用作预先填写的文件名
        alink.click();
    },
    showResultImage(data){
      this.isShowResult = true;
      this.imageResultSrc = "/static/Data/Temp/"+data.showImage;
      this.recordRealResult = data.resultImage;
    },
  }
}
</script>

<style scoped>
#ShowResult{
  width: 100%;
  height: 100%;
  object-fit: contain;
}
#brightnessAdjustRange{
    background-image: linear-gradient(to right, rgb(0, 0, 0, 1) , rgba(160, 160, 160, 0.2));;
    border-radius: 10px;
    width: 100%;
    -webkit-appearance: none;
    height:4px;
}
#channelAdjustRange{
    background-image: linear-gradient(to right, rgb(183, 0, 0) , rgb(0, 234, 255));;
    border-radius: 10px;
    width: 100%;
    -webkit-appearance: none;
    height:4px;
}
#imgShowPart{
    width: 100%;
    height: 100%;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    border-bottom: 1px grey solid;
}
.subTitle{
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    justify-content: left;
    width: 100%;
    height: 100px;
    border-bottom: 1px #cbcbcb solid;
    overflow: hidden;
}
#getResultImage{
    height: 70%;
    width: 30%;
    margin-left: 3%;
    cursor: pointer;
    border-radius: 3px;
    background-color: #409eff;
    color: white;
    transition: 0.3s ease;
    overflow: hidden;
}
#getResultImage:hover{
    background-color: rgba(56, 56, 56, 0.78);
    color: #edecd6;
}
#downloadResult{
  width: 48%;
  height: 70%;
  font-size: small;
  border: 1px grey solid;
  margin-right: 5%;
}
#saveImage{
    line-height: 100%;
    height: 70%;
    width: 30%;
    margin-left: 2%;
    cursor: pointer;
    border-radius: 3px;
    background-color: rgba(60, 197, 60, 0.78);
    color: white;
    transition: 0.3s ease;
    overflow: hidden;
}
.imgPart_inner{
    width: 98%;
    display: flex;
    justify-content: center;
    flex-direction: column;
}
#saveImage:hover{
    background-color: rgba(56, 56, 56, 0.78);
    color: #caffb1;
}
#imgBackPart{
    width: 70%;
    height: 95%;
    background-color: rgba(126, 126, 126, 0.25);
    border: 2px solid black;
    /* border-radius: 40px; */
    font-family: STHeiti,serif;
    color: #363636;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    transition: 0.3s;
}

#imgBackPart:hover{
    background-color: rgba(126, 126, 126, 0.15);
}
#mainControlPart{
    width: 30%;
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: center;
    align-items: center;
}
input[type="checkbox"] {
  height: 22px;
  width: 22px;
  border: 3px rgb(0, 94, 255);
  cursor: pointer;
}
#mainControlBtn{
    width: 100%;
    height: 25%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-bottom: 1px grey solid;
}
#mainControlRange{
    width: 100%;
    height: 75%;
    display: flex;
    flex-direction: column;
    justify-content: start;
    align-items: flex-start;
}
.mainControlRange_container{
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

</style>