<template>
  <div id="imgPart">
    <el-dialog
      title="无上传次数？"
      :visible.sync="moreMessage.noUpdateTime"
      width="30%"
      center>
      <span>点击<a @click="toInfoPage_upload()" class="fontLink">这里</a>查看图片上传规则</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="moreMessage.noUpdateTime = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="无法下载结果图片？"
      :visible.sync="moreMessage.noDownload"
      width="30%"
      center>
      <span>点击<a @click="toInfoPage_download()" class="fontLink">这里</a>查看图片下载规则</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="moreMessage.noDownload = false">确 定</el-button>
      </span>
    </el-dialog>
    <div class="subTitle">
      <p style="font-weight: bold;height: 50%;font-family: 幼圆,serif;color: #363636;display: flex;justify-content: center;margin-left: 2%;">图片上传(Image Upload):</p>
      <div style="width: 100%;height: 50%;display: flex;flex-direction: row;">
        <div id="uploadBtnContainer">
          <el-button icon="el-icon-upload2" type="primary" ref="uploadBtn" @click="uploadNewImage()" style="width: 90%;border-radius: 5px;font-size: small">开始上传</el-button>
        </div>
        <div id="uploadStatus">
            <p ref="uploadStatus" :class="uploadStatus_class">等待上传</p>
        </div>
        <div id="chooseLastImageBtn" @click="chooseLastImage()">
            <p>选择上次上传图片>>></p>
        </div>
      </div>
    </div>
    <div class="imgPart_inner">
      <div class="innerTitle">
          <p style="overflow: hidden;width:13%;font-family: 幼圆,serif;color: #363636;display: flex;justify-content: flex-start;margin-left: 3%">图片信息</p>
          <p style="margin-left: 5%;color: red;font-family: 幼圆,serif">*必须</p>
      </div>
      <div id="imgSendContainer">
          <div id="imgSendPart_blue" @click="chooseBlueImage()">
              <div id="blueImageShowField">
                  <img ref="imageShow_blue" src="@/assets/uploadicon.png" id="icon_blue" class="uploadIcon" alt="图片加载失败">
              </div>
              <div style="width: 100%; height: 16%;">
                  <div ref="blueImageShowBtn" class="uploadButton" @click="chooseBlueImage()">选择蓝色光源图片(415nm)</div>
                  <!--这个提交按钮太丑了，隐藏-->
                  <input ref="blueImageChooseBtn" id="blueImageButton" type="file" style="margin-top: 400px" @change="blueImageShowChange()">
              </div>
          </div>
          <div id="imgSendPart_green" @click="chooseGreenImage()">
              <div id="greenImageShowField">
                  <img ref="imageShow_green" src="@/assets/uploadicon.png" id="icon_green" class="uploadIcon" alt="图片加载失败">
              </div>
              <div style="width: 100%; height: 16%;">
                  <div ref="greenImageShowBtn" class="uploadButton" id="greenImageButton_Show" @click="chooseGreenImage()" style="color: rgb(49,143,63)">选择绿色光源图片(540nm)</div>
                  <input ref="greenImageChooseBtn" id="greenImageButton" type="file" style="margin-top: 400px" @change="greenImageShowChange()">
              </div>
          </div>
          <div id="imgSendPart_white" @click="chooseWhiteImage()">
              <div id="whiteImageShowField">
                  <img ref="imageShow_white" src="@/assets/uploadicon.png" id="icon_white" class="uploadIcon" alt="图片加载失败">
              </div>
              <div style="width: 100%; height: 16%;">
                  <div ref="whiteImageShowBtn" class="uploadButton" id="whiteImageButton_Show" @click="chooseWhiteImage()" style="background-color: rgba(255, 255, 255, 0.4); color: black;border: 2px solid #323232;">选择白色光源图片(非必须)</div>
                  <input ref="whiteImageChooseBtn" id="whiteImageButton" type="file" style="margin-top: 400px" @change="whiteImageShowChange()">
              </div>
          </div>
      </div>
      <div class="innerTitle" style="border-top: 1px #d0d0d0 solid; margin-top: 5px">
          <p style="overflow: hidden;width:13%;font-family: 幼圆,serif;color: #363636;display: flex;justify-content: flex-start;margin-left: 3%">附加信息</p>
          <!-- <p style="margin-left: 5%;color: rgb(19, 124, 0);font-family: 幼圆,serif">*非必须</p> -->
      </div>
      <div id="imgSend_addInfoContainer">
        <div style="width: 50%;height: 100%; display: block;justify-content: left;">
            <div class="addInfo">
                <p class="addInfo_formLabel">标本名称：<span style="margin-left: 5%;color: red;font-family: 幼圆,serif">*</span></p>
                <input v-model="additionInfo.sampleName" class="addInfo_formInput" id="addInfo_sampleName" AUTOCOMPLETE="off" type="text" placeholder="输入标本名称"/>
                <p style="color: red;width: 5%;text-align: center;"></p>
            </div>
            <div id="addInfo_bodyPart_Container" style="display: flex;flex-direction: column;">
                <div class="addInfo">
                    <p class="addInfo_formLabel">&emsp;部位：&emsp;<span style="margin-left: 5%;color: red;font-family: 幼圆,serif">*</span></p>
                    <select v-model="additionInfo.part" class="addInfo_choose" id="addInfo_bodyPart" @change="addInfoPartChange()">
                        <option>    食管</option>
                        <option>    胃</option>
                        <option>    小肠</option>
                        <option>    大肠</option>
                        <option>    其他</option>
                    </select>
                    <p style="color: red;width: 5%;text-align: center;"></p>
                </div>
                <div v-show="part_Other"  class="addInfo" id="addInfo_bodyPart_other_Container">
                  <p class="addInfo_formLabel"></p>
                  <input v-model="additionInfo.part_other" class="addInfo_formInput" id="addInfo_bodyPart_other" AUTOCOMPLETE="off" type="text" placeholder="输入其他标本部位名称"/>
                  <p style="color: red;width: 5%;text-align: center;"></p>
                </div>
            </div>
            <div class="addInfo">
                <p class="addInfo_formLabel">&emsp;备注：&emsp;<span style="margin-left: 5%;color: rgb(19, 124, 0);font-family: 幼圆,serif">*</span></p>
                <div style="width: 60%;height: 100px;display: flex;justify-content: center;align-items: center;overflow: hidden;">
                    <textarea v-model="additionInfo.remark" style="font-family: Arial, Helvetica, sans-serif; font-size: 14px;height: 92%; width: 100%;resize: none;" placeholder="备注"></textarea>
                </div>
                <p style="color: red;width: 5%;text-align: center;"></p>
            </div>
        </div>
        <div style="width: 50%; height: 100%; display: flex;flex-direction: column;">
            <div id="addInfo_diagnoseBefore_Container" style="display: flex;flex-direction: column;">
                <div class="addInfo">
                    <div class="addInfoInner">
                      <p class="addInfo_formLabel_special" style="margin: 0px;">术前诊断：<span style="margin-left: 5%;color: red;font-family: 幼圆,serif">*</span></p>
                      <p class="addInfo_formLabel_special" style="color: rgb(182, 182, 182);font-size: 10px;margin: 0px;">按住Shift/Ctrl多选</p>
                    </div>
                    <select multiple="multiple" style="width: 60%;height: 200px;" id="addInfo_diagnoseBefore" @change="addInfoDiagnoseBeforeChange()">
                        <option name="addInfo_diagnoseBefore_c" class="addInfo_choose" style="width: 100%; display: flex;align-items: center;justify-content: left;">    早癌</option>
                        <option name="addInfo_diagnoseBefore_c" class="addInfo_choose" style="width: 100%; display: flex;align-items: center;justify-content: left;">    LGIN</option>
                        <option name="addInfo_diagnoseBefore_c" class="addInfo_choose" style="width: 100%; display: flex;align-items: center;justify-content: left;">    腺瘤</option>
                        <option name="addInfo_diagnoseBefore_c" class="addInfo_choose" style="width: 100%; display: flex;align-items: center;justify-content: left;">    SMT</option>
                        <option name="addInfo_diagnoseBefore_c" class="addInfo_choose" style="width: 100%; display: flex;align-items: center;justify-content: left;">    炎症</option>
                        <option id="addInfo_diagnoseBefore_other_option" name="addInfo_diagnoseBefore_c" class="addInfo_choose" style="width: 100%; display: flex;align-items: center;justify-content: left;">    其他</option>
                    </select>
                </div>
                <div v-show="part_diagnose" class="addInfo" id="addInfo_diagnoseBefore_other_Container">
                    <p class="addInfo_formLabel"></p>
                    <input ref="addInfo_diagnoseBefore_other" class="addInfo_formInput" AUTOCOMPLETE="off" type="text" placeholder="    输入其他早期诊断结论"/>
                </div>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "singleImageProcess_imageSendPart",
  data(){
    return {
      isUploaded: false,
      uploadStatus_class: "uploadStatus_red",
      blueImageChoose: false,
      greenImageChoose: false,
      additionInfo:{
        sampleName: "",
        part: "",
        part_other: "",
        remark: "",
      },
      part_Other: false,
      part_diagnose: false,
      moreMessage:{
        noUpdateTime: false,
        noDownload: false,
      },
      imageInfoID: '',  //上传后返回图片信息id，通过这个id来生成结果图片
    }
  },
  mounted() {
    this.$bus.$on('sendUploadedInfoToGet',()=>{
      this.$bus.$emit("getUploadedInfo",{"uploadStatus":this.isUploaded, "gid": this.imageInfoID});
    });
    this.$bus.$on('showNoDownloadInfo',()=>{
      this.moreMessage.noDownload = true;
    })
  },
  beforeDestroy() {
    this.$bus.$off("sendUploadedInfoToGet");
    this.$bus.$off('showNoDownloadInfo');
  },
  methods:{
    toInfoPage_upload(){
      this.moreMessage.noUpdateTime = false;
      this.$router.push({
        path: "/Info",
        query: {which: "uploadTimes"},
      })
    },
    toInfoPage_download(){
      this.moreMessage.noDownload = false;
      this.$router.push({
        path: "/Info",
        query: {which: "userType"},
      })
    },
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
    uploadNewImage(){
      if (!this.greenImageChoose || !this.blueImageChoose){
        this.$message({
          showClose: true,
          message: '必须选择想要上传的原图片',
          type: 'error'
        });
        return;
      }
      if (this.additionInfo.sampleName.length == 0){
        this.$message({
          showClose: true,
          message: '必须填写标本名称',
          type: 'error'
        });
        return;
      }
      if (this.additionInfo.part.length == 0 || (this.additionInfo.part === '其他' && this.additionInfo.part_other.length == 0)){
        this.$message({
          showClose: true,
          message: '必须选择并完整填写标本部位',
          type: 'error'
        });
        return;
      }
      let uploadForm = new FormData();
      // 图片数据
      uploadForm.append("blueImage", document.getElementById("blueImageButton").files[0]);
      uploadForm.append("greenImage", document.getElementById("greenImageButton").files[0]);
      uploadForm.append("whiteImage", document.getElementById("whiteImageButton").files[0]);
      // 身份识别数据
      uploadForm.append("uid", this.getUID());
      uploadForm.append("token", this.getToken());
      // 图片附加数据
      uploadForm.append("sampleName", this.additionInfo.sampleName);
      uploadForm.append("remark", this.additionInfo.remark);
      const part = this.additionInfo.part === "其他"? this.additionInfo.part_other: this.additionInfo.part;
      uploadForm.append("part", part);
      const chooseList = document.getElementsByName("addInfo_diagnoseBefore_c");
      // 使用字符串数组，用于存放选择好了的数据
      const chooseResult = [];
      for(let i = 0;i < chooseList.length;i++) {
          if (chooseList[i].selected === true) {
            if (chooseList[i].value !== "其他"){
              chooseResult.push(chooseList[i].value);//这个是获取多选框中的值
            }
            else{
              chooseResult.push(this.$refs.addInfo_diagnoseBefore_other.value);//这个是获取多选框中的值
            }
          }
      }
      if (chooseResult.length === 0){
        this.$message({
          showClose: true,
          message: '必须选择术前诊断',
          type: 'error'
        });
        return;
      }
      uploadForm.append("diagnoseBefore", chooseResult);
      let config = {
         headers: {'Content-Type': 'multipart/form-data'}
      };
      this.$refs.uploadStatus.innerText = "上传中";
      this.uploadStatus_class = "uploadStatus_yellow";
      this.$refs.uploadBtn.disabled = true;
      this.$axios.post("/NBI/Image/upload/",uploadForm, config).then((response) => {
        if (response.data === 1){
            this.$message({
              showClose: true,
              message: '登录状态错误！请重新登录。',
              type: 'error'
            });
            this.$bus.$emit("changeStatus",{status: false, uname:''});
            this.$refs.uploadStatus.innerText = "等待上传";
            this.uploadStatus_class = "uploadStatus_red";
        }
        else if (response.data === 2){
            this.$message({
              showClose: true,
              message: '您提交的图片为空，请检查！',
              type: 'error'
            });
            this.$refs.uploadStatus.innerText = "等待上传";
            this.uploadStatus_class = "uploadStatus_red";
        }
        else if (response.data === 3){
            this.$message({
              showClose: true,
              message: '图片存储错误，目前仅支持常见图片格式。',
              type: 'error'
            });
            this.$refs.uploadStatus.innerText = "等待上传";
            this.uploadStatus_class = "uploadStatus_red";
        }
        else if (response.data === 4){
            this.$message({
              showClose: true,
              message: '上传失败，您是普通用户，并且已经没有上传次数。',
              type: 'error'
            });
            this.moreMessage.noUpdateTime = true;
            this.$refs.uploadStatus.innerText = "等待上传";
            this.uploadStatus_class = "uploadStatus_red";
        }
        else{
          const imageShow_blue = this.$refs.imageShow_blue;
          imageShow_blue.className = "uploadImageShow";
          imageShow_blue.src = "/static/Data/Blue/"+response.data.imageBlue;
          const imageShow_green = this.$refs.imageShow_green;
          imageShow_green.className = "uploadImageShow";
          imageShow_green.src = "/static/Data/Green/"+response.data.imageGreen;
          if (response.data.imageWhite !== null){
            const imageShow_white = this.$refs.imageShow_white;
            imageShow_white.className = "uploadImageShow";
            imageShow_white.src = "/static/Data/White/"+response.data.imageWhite;
          }
          this.$refs.uploadStatus.innerText = "已上传";
          this.uploadStatus_class = "uploadStatus_green";
          this.isUploaded = true;
          this.imageInfoID = response.data.gid;
        }
        this.$refs.uploadBtn.disabled = false;
      });
    },
    chooseLastImage(){
      let getLastUploadImageForm = new FormData();
      // 身份识别数据
      getLastUploadImageForm.append("uid", this.getUID());
      getLastUploadImageForm.append("token", this.getToken());
      let config = {
         headers: {'Content-Type': 'multipart/form-data'}
      };
      this.$axios.post("/NBI/Image/chooseLastImage/",getLastUploadImageForm, config).then((response) => {
        if (response.data === 2){
            this.$message({
              showClose: true,
              message: '登录状态错误！请重新登录。',
              type: 'error'
            });
            this.$bus.$emit("changeStatus",{status: false, uname:''});
        }
        else if (response.data === 1){
            this.$message({
              showClose: true,
              message: '未发现上次上传的图片',
              type: 'warning'
            });
        }
        else{
          const imageShow_blue = this.$refs.imageShow_blue;
          imageShow_blue.className = "uploadImageShow";
          imageShow_blue.src = "/static/Data/Blue/"+response.data.imageBlue;
          const imageShow_green = this.$refs.imageShow_green;
          imageShow_green.className = "uploadImageShow";
          imageShow_green.src = "/static/Data/Green/"+response.data.imageGreen;
          if (response.data.imageWhite !== null){
            const imageShow_white = this.$refs.imageShow_white;
            imageShow_white.className = "uploadImageShow";
            imageShow_white.src = "/static/Data/White/"+response.data.imageWhite;
            this.$refs.whiteImageShowBtn.innerText = "已选择："+this.cutFileName(response.data.imageWhite.split("~")[0]+'.'+response.data.imageWhite.split(".")[1]);
          }
          this.additionInfo.sampleName = response.data.sampleName;
          this.additionInfo.remark = response.data.remark;

          this.$refs.blueImageShowBtn.innerText = "已选择："+this.cutFileName(response.data.imageBlue.split("~")[0]+'.'+response.data.imageBlue.split(".")[1]);
          this.$refs.greenImageShowBtn.innerText = "已选择："+this.cutFileName(response.data.imageGreen.split("~")[0]+'.'+response.data.imageGreen.split(".")[1]);
          this.isUploaded = true;
          this.$refs.uploadStatus.innerText = "已上传";
          this.uploadStatus_class = "uploadStatus_green";
          this.imageInfoID = response.data.gid;
        }
      });
    },
    addInfoPartChange(){
      const choose = document.getElementById("addInfo_bodyPart").value;
      this.part_Other = choose === "其他";
    },
    addInfoDiagnoseBeforeChange(){
      const chooseList = document.getElementsByName("addInfo_diagnoseBefore_c");
      // 使用字符串数组，用于存放选择好了的数据
      const chooseResult = new Array(chooseList.length);
      for(let i = 0;i < chooseList.length;i++) {
          if (chooseList[i].selected === true) {
              chooseResult[i] = chooseList[i].value;//这个是获取多选框中的值
          }
      }
      this.part_diagnose = chooseResult[5] !== undefined;
    },
    chooseBlueImage(){
      this.blueImageChoose = true;
      this.$refs.blueImageChooseBtn.click();
    },
    chooseGreenImage(){
      this.greenImageChoose = true;
      this.$refs.greenImageChooseBtn.click();
    },
    chooseWhiteImage(){
      this.$refs.whiteImageChooseBtn.click();
    },
    getFileName(o){
      const pos = o.lastIndexOf("\\");
      if (o.length < pos+15){
        return o.substring(pos+1);
      }
      else{
        return o.substring(pos+1,pos+10) + "...";
      }
    },
    cutFileName(o){
      if (o.length < 15){
        return o;
      }
      else{
        return o.substring(0,15) + "...";
      }
    },
    getFileType(o){
      const pos = o.lastIndexOf(".");
      return o.slice(pos+1, o.length);
    },
    blueImageShowChange(){
      const imageShow = this.$refs.imageShow_blue;
      imageShow.className = "uploadIcon";
      const blue_input = this.$refs.blueImageChooseBtn;
      this.$refs.blueImageShowBtn.innerText = "已选择："+this.getFileName(blue_input.value);
      const fileType = this.getFileType(blue_input.value);
      if (fileType === "jpg" || fileType ==="JPG" || fileType==="jpeg"){
        const file = blue_input.files[0]; // 获取input上传的图片数据;
        let read = new FileReader(); // 创建FileReader对像;
        read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
        read.onload = function() {
          // 拿到读取结果;
          imageShow.src = read.result;
        }
        imageShow.className = "uploadImageShow";
      }else{
        imageShow.src = "/static/img/unknownImageTypeIcon.png";
      }
    },
    greenImageShowChange(){
      const imageShow = this.$refs.imageShow_green;
      imageShow.className = "uploadIcon";
      const green_input = this.$refs.greenImageChooseBtn;
      this.$refs.greenImageShowBtn.innerText = "已选择："+this.getFileName(green_input.value);
      const fileType = this.getFileType(green_input.value);
      if (fileType === "jpg" || fileType ==="JPG" || fileType==="jpeg"){
        const file = green_input.files[0]; // 获取input上传的图片数据;
        let read = new FileReader(); // 创建FileReader对像;
        read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
        read.onload = function() {
          // 拿到读取结果;
          imageShow.src = read.result;
        }
        imageShow.className = "uploadImageShow";
      }else{
        imageShow.src = "/static/img/unknownImageTypeIcon.png";
      }
    },
    whiteImageShowChange(){
      const imageShow = this.$refs.imageShow_white;
      imageShow.className = "uploadIcon";
      const white_input = this.$refs.whiteImageChooseBtn;
      this.$refs.whiteImageShowBtn.innerText = "已选择："+this.getFileName(white_input.value);
      const fileType = this.getFileType(white_input.value);
      if (fileType === "jpg" || fileType ==="JPG" || fileType==="jpeg"){
        const file = white_input.files[0]; // 获取input上传的图片数据;
        let read = new FileReader(); // 创建FileReader对像;
        read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
        read.onload = function() {
          // 拿到读取结果;
          imageShow.src = read.result;
        }
        imageShow.className = "uploadImageShow";
      }else{
        imageShow.src = "/static/img/unknownImageTypeIcon.png";
      }
    },
  },
}
</script>

<style scoped>
#imgPart{
  width: 100%;
  /* height: 100%; */
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
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
#uploadBtnContainer{
    width: 32%;
    height: 70%;
    margin-left: 3%;
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    overflow: hidden;
}
#chooseLastImageBtn{
    margin-left: 20%;
    margin-right: 3%;
    width: 30%;
    height: 70%;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: Arial, Helvetica, sans-serif;
    color: rgb(37, 70, 255);
    transition: 0.3s ease;
    font-size: small;
    border:rgb(37, 70, 255) 1px solid ;
    border-radius: 3px;
}

#chooseLastImageBtn:hover{
    color: rgb(91, 115, 255);
    border:rgb(91, 115, 255) 1px solid ;
}

#uploadStatus{
    margin-left: 0;
    width: 18%;
    height: 70%;
    display: flex;
    align-items: center;
    justify-content: start;
}
.uploadStatus_red{
  font-family: 幼圆,serif;
  font-weight: bold;
  color: rgb(217, 8, 8);
}
.uploadStatus_yellow{
  font-family: 幼圆,serif;
  font-weight: bold;
  color: rgb(255, 183, 82);
}
.uploadStatus_green{
  font-family: 幼圆,serif;
  font-weight: bold;
  color: rgb(34, 255, 0);
}

.imgPart_inner{
    width: 100%;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

#imgSendContainer{
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 180px;
    justify-content: start;
    align-items: center;
}

#imgSendPart_blue{
    width: 30%;
    height: 90%;
    border-radius: 3px;
    align-content: center;
    overflow: hidden;
    margin-right: 1%;
    margin-left: 3%;
}
#blueImageShowField{
  background-color: rgba(154, 198, 255, 0.95);
  border: 2px solid rgba(0, 0, 0, 0.8);
  width: 98%;
  height:80%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.3s;
  cursor: pointer;
}
#blueImageShowField:hover{
    background-color: rgba(154, 198, 255, 0.5);
}

#imgSendPart_green{
    width: 30%;
    height: 90%;
    border-radius: 3px;
    align-content: center;
    overflow: hidden;
    margin-right: 1%;
}

#greenImageShowField{
  background-color: rgba(154, 255, 171, 0.95);
  border: 2px solid rgba(0, 0, 0, 0.8);
  width: 98%;
  height:80%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.3s;
  cursor: pointer;
}
#greenImageShowField:hover{
    background-color: rgba(154, 255, 171, 0.5);
}

#imgSendPart_white{
    width: 30%;
    height: 90%;
    border-radius: 3px;
    align-content: center;
    transition: 0.3s;
    overflow: hidden;
}

#whiteImageShowField{
  background-color: rgba(154, 255, 171, 0);
  border: 2px solid rgba(0, 0, 0, 0.8);
  width: 98%;
  height:80%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.3s;
  cursor: pointer;
}
#whiteImageShowField:hover{
    background-color: rgba(228, 228, 228, 0.15);
}

.innerTitle{
    display: flex;
    align-items: center;
    flex-direction: row;
    justify-content: left;
    width: 100%;
    height: 30px;
    overflow: hidden;
}

.uploadButton {
    transition: 0.1s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1 1 auto;
    height: 95%;
    border: 2px solid black;
    border-radius: 5px;
    text-align: center;
    position: relative;
    overflow: hidden;
    font-family: STHeiti,serif;
    font-size: smaller;
    color: blue;
}
.uploadButton:after {
    position: absolute;
    transition: 0.3s;
    content: "";
    width: 0;
    left: 50%;
    bottom: 0;
    height: 3px;
    background: #ff906c;
}
.uploadButton:hover {
    cursor: pointer;
}
.uploadButton:hover:after {
    width: 100%;
    left: 0;
}

.uploadIcon{
    height: 60%;
    margin-top: 5%;
}
/*当展示上传的图片时显示这个样式*/
.uploadImageShow{
    height: 100%;
}

#imgSend_addInfoContainer{
    display: flex;
    flex-direction: row;
    margin-top: 10px;
    width: 100%;
    height: 280px;
    justify-content: center;
    align-items: center;
}
.addInfo{
    display: flex;
    flex-direction: row;
    width: 95%;
    justify-content: center;
    align-items: center;
}
.addInfo_formLabel{
    width: 40%;
    height: 26px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: small;
}
.addInfo_formInput{
    width: 60%;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    text-align:left;
    border-radius:4px;
    border:1px solid #c8cccf;
    color:#6a6f77;
}
.addInfo_choose{
    width: 60%;
    height: 40px;
	display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    text-align:left;
    border-radius:4px;
    border:1px solid #c8cccf;
    color:#6a6f77;
}
.fontLink{
  margin-left: 4px;
  margin-right: 4px;
  color: #1122AA;
  cursor: pointer;
}
.fontLink:hover{
  color: #2a3ff5;
}

.addInfoInner {
  width: 40%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.addInfo_formLabel_special {
  width: 100%;
  height: 26px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: small;
}
</style>