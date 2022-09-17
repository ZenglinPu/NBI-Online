<template>
 <el-container>
   <el-dialog
      title="无法使用批处理功能？"
      :visible.sync="moreMessage.noBatch"
      width="30%"
      center>
      <span>点击<a @click="toInfoPage_batchProcess()" class="fontLink">这里</a>查看批处理权限规则</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="moreMessage.noBatch = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-aside width="355px">
      <div class="aside-button">
        <div v-show="!isUploaded" class="uploadPackageBtn" @click="chooseNewPackage()">
          <i ref="uploadPackageIcon" class="el-icon-upload" style="color: darkgray;font-size: 80px"></i>
          <div ref="uploadPackageFont" class="el-upload__text" style="color: dodgerblue;margin-top: 20px">点击上传</div>
        </div>
        <div v-show="isUploaded" class="uploadPackageBtn" @mouseenter="reUploadBtnShow = true" @mouseleave="reUploadBtnShow=false">
          <img style="height: 45%" src="/static/img/packageIcon.png">
          <el-button v-show="reUploadBtnShow" type="danger" style="width: 65%;transition: 0.2s ease; margin-top: -50%" @click="reUploadBtn">重新上传</el-button>
        </div>
        <div style="height: 10%;margin-top: 3%;width: 100%;text-align: center;color: #b6b6b6">只支持上传zip文件</div>
        <input @change="uploadNewPackage()" type="file" ref="compressPackageInput" style="visibility: hidden; height: 0">
        <div style="width: 80%;height: 10%;margin-bottom: 10px; font-family: 幼圆,serif; display: flex;align-items: center;justify-content: start;font-weight: bold">
          批次名称：{{batchTitle}}
        </div>
      </div>

      <div class="aside-block">
        <div style="width: 80%;height: 18%; font-family: 幼圆,serif; display: flex;align-items: center;justify-content: start;font-weight: bold">
          批次状态：
        </div>
        <div style="width: 80%;height: 82%; display: flex;justify-content: start;align-items: center">
          <el-timeline style="font-family: 幼圆,serif">
            <el-timeline-item
              v-for="(activity, index) in activities"
              :key="index"
              :icon="activity.icon"
              :type="activity.type"
              :color="activity.color"
              :size="activity.size"
              :timestamp="activity.timestamp">
              &emsp;{{activity.content}}
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-aside>
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4">
            <div class="header-title">
              <i class="el-icon-upload"></i>
              <span>  图片上传批处理</span>
            </div>
          </el-col>
          <el-col :span="16">
            <div class="header-follow">
              <el-popover
                placement="top-start"
                width="100"
                trigger="hover"
                content="上传原始图片压缩包，批量生成NBI图片。（点击查看批处理压缩包详细规则）">
                <el-button @click="toInfoPage_batchRequest()" style="cursor: pointer;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
              </el-popover>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="header-last">
              <el-button v-show="isFinish" type="success" style="width: 90%;margin-right: 4%;height: 36px; font-family: 幼圆,serif;">查看处理结果</el-button>
              <el-button v-show="!isFinish" @click="startProcess()" :disabled="!isPassCheck || isProcessing" type="danger" style="width: 90%;margin-right: 4%;height: 36px; font-family: 幼圆,serif;">{{ uploadBtnFont }}</el-button>
            </div>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table
          :cell-style="{color: '#666', fontSize:'14px', height:'85px'}"
          :header-cell-style="{color: '#222222', fontSize:'14px'}"
          :data="tableData"
          style="width: 100%;"
          max-height="603">
          <el-table-column
            prop="name"
            label="标本ID"
            width="242">
          </el-table-column>
          <el-table-column
            prop="blueCompress"
            label="蓝色光源图片"
            align="center"
            width="252">
            <template slot-scope="scope">
              <div style="height: 83px;display: flex;align-items: center;justify-content: center">
                <el-image
                  :src="'/static/Data/Blue/' + scope.row.blueCompress"
                  :fit="'contain'"
                  style="width: 80%;height: 80%"
                >
                </el-image>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="greenCompress"
            label="绿色光源图片"
            align="center"
            width="252">
            <template slot-scope="scope">
              <div style="height: 83px;display: flex;align-items: center;justify-content: center">
                <el-image
                  :src="'/static/Data/Green/' + scope.row.greenCompress"
                  :fit="'contain'"
                  style="width: 80%;height: 80%"
                >
                </el-image>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="whiteCompress"
            label="白色光源图片"
            align="center"
            width="252">
            <template slot-scope="scope">
              <div style="height: 83px;display: flex;align-items: center;justify-content: center">
                <el-image
                  v-show="scope.row.whiteCompress !== null"
                  :src="'/static/Data/White/' + scope.row.whiteCompress"
                  style="width: 80%;height: 80%"
                  :fit="'contain'"
                >
                </el-image>
                <p v-show="scope.row.whiteCompress === null">未上传白色标本图像</p>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            width="120">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="deleteRow(scope.$index)"
                type="text"
                size="small">
                <i class="el-icon-delete oneImageDeleteBtn"></i>移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "MultiImageProcess",
  data() {
    return {
      batchTitle: '',
      batchID: '',
      isUploaded: false,
      isPassCheck: false,
      isProcessing: false,
      isFinish: false,
      uploadBtnFont: "开始处理",
      reUploadBtnShow: false,
      activities: [
      {
        content: '等待上传',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-close',
        // icon: 'el-icon-check',
        color: '#ff9854',
        // color: '#0bbd87',
        // color: '#0bbd87',
      }, {
        content: '上传压缩包',
        timestamp: '',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-close',
        color: '#ff9854'
      }, {
        content: '检查压缩包',
        timestamp: '',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-close',
        color: '#ff9854'
      },{
        content: '处理图片组',
        timestamp: '',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-close',
        color: '#ff9854'
      }, {
        content: '处理完成',
        timestamp: '',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-close',
        color: '#ff9854'
      }],
      tableData: [
      // {
      //   name: '王小虎',
      //   blueCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
      //   greenCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
      //   whiteCompress: 'result_compress_10@10*com~gdztfkvc.jpg'
      // },
      ],
      moreMessage:{
        noBatch: false,
      },
      deleteImagePare: [], // 记录前端开始处理前打算去掉的图片组
    };
  },
  methods:{
    reUploadBtn(){
      this.isFinish = false;
      this.isUploaded = false;
      this.isPassCheck = false;

    },
    toInfoPage_batchProcess(){
      this.moreMessage.noBatch = false;
      this.$router.push({
        path: "/Info",
        query: {which: "userType"},
      })
    },
    toInfoPage_batchRequest(){
      this.$router.push({
        path: "/Info",
        query: {which: "batchRequest"},
      })
    },
    deleteRow(index){
      this.deleteImagePare.push(this.tableData[index].name);
      this.tableData.splice(index, 1);
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
    chooseNewPackage(){
      this.$refs.compressPackageInput.click();
    },
    startProcess(){
      let startProcessForm = new FormData();
      startProcessForm.append("uid", this.getUID());
      startProcessForm.append("token", this.getToken());
      startProcessForm.append("batchID", this.batchID);
      startProcessForm.append("ignoreImage", this.deleteImagePare);
      this.isProcessing = true;
      this.uploadBtnFont = "处理中";
      this.$axios.post("/NBI/Batch/startProcess/",startProcessForm,{
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1) {
          this.$message({
            showClose: true,
            message: '账户信息错误，上传失败！',
            type: 'error'
          });
          this.uploadBtnFont = "开始处理";
          this.isProcessing = false;
        }
        else if (response.data === 2) {
          this.$message({
            showClose: true,
            message: '错误，该批次无法被处理',
            type: 'error'
          });
          this.uploadBtnFont = "开始处理";
          this.isProcessing = false;
        }
        else if (response.data === 4) {
          this.$message({
            showClose: true,
            message: '错误，该批次为空',
            type: 'error'
          });
          this.uploadBtnFont = "开始处理";
          this.isProcessing = false;
        }
        else{
          this.$message({
            showClose: true,
            message: '已开始处理',
            type: 'success'
          });
        }
      });
    },
    showImageInfoInPackage(){
      let packageImageForm = new FormData();
      packageImageForm.append("uid", this.getUID());
      packageImageForm.append("token", this.getToken());
      packageImageForm.append("batchID", this.batchID);
      this.$axios.post("/NBI/Batch/getOriginImage/",packageImageForm,{
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        // console.log(response)
        if (response.data === 1) {
          this.$message({
            showClose: true,
            message: '账户信息错误，上传失败！',
            type: 'error'
          });
        }
        else{
          for (const key in response.data) {
            const item = response.data[key];
            this.tableData.push({
              name: item.imageName,
              blueCompress: item.imageBlue,
              greenCompress: item.imageGreen,
              whiteCompress: item.imageWhite,
            })
          }
        }
      });
    },
    updateProcessStatusShow(status, uploadTime, checkTime, finishTime, processedNum, batchSize){
      if (status === 1){
              // 上传中
              this.activities[1].color = "#ff9854";
              this.activities[1].icon = 'el-icon-loading';
            }
      if (status === 2){
        // 上传完成，检查中
        this.activities[1].color = "#0bbd87";
        this.activities[1].icon = 'el-icon-check';
        this.activities[1].timestamp = uploadTime;

        this.activities[2].color = "#ff9854";
        this.activities[2].icon = 'el-icon-loading';
      }
      if (status === 3){
        // 检查失败
        this.activities[1].color = "#0bbd87";
        this.activities[1].icon = 'el-icon-check';
        this.activities[1].timestamp = uploadTime;

        this.activities[2].color = "#ff4747";
        this.activities[2].icon = 'el-icon-close';
        this.activities[2].content = "检查失败，压缩包不符合要求";
      }
      if (status === 4){
        // 检查通过，处理中
        if (!this.isPassCheck){
          this.showImageInfoInPackage();
          this.isPassCheck = true;
        }

        if (this.isProcessing){
          this.uploadBtnFont = "处理中（"+processedNum+"/"+ batchSize+")";
        }

        this.activities[1].color = "#0bbd87";
        this.activities[1].icon = 'el-icon-check';
        this.activities[1].timestamp = uploadTime;

        this.activities[2].color = "#0bbd87";
        this.activities[2].icon = 'el-icon-check';
        this.activities[2].timestamp = checkTime;

        this.activities[3].color = "#ff9854";
        this.activities[3].icon = 'el-icon-close';
        this.activities[3].content = "处理图片组";
      }
      if (status === 5){
        // 检查通过，处理中
        if (!this.isPassCheck){
          this.showImageInfoInPackage();
          this.isPassCheck = true;
        }

        if (this.isProcessing){
          this.uploadBtnFont = "处理中（"+ processedNum+"/"+ batchSize+")";
        }

        this.activities[1].color = "#0bbd87";
        this.activities[1].icon = 'el-icon-check';
        this.activities[1].timestamp = uploadTime;

        this.activities[2].color = "#0bbd87";
        this.activities[2].icon = 'el-icon-check';
        this.activities[2].timestamp = checkTime;

        this.activities[3].color = "#ff9854";
        this.activities[3].icon = 'el-icon-loading';
        this.activities[3].content = "处理图片组("+processedNum+"/"+ batchSize+")";
      }
      if (status === 6){
        // 处理完成
        if (this.isProcessing){
          this.uploadBtnFont = "处理中（"+processedNum+"/"+batchSize+")";
          this.isProcessing = false;
        }
        if (!this.isFinish){
          this.isFinish = true;
          this.$message({
            showClose: true,
            message: '批处理已完成',
            type: 'success'
          });
        }

        this.activities[1].color = "#0bbd87";
        this.activities[1].icon = 'el-icon-check';
        this.activities[1].timestamp = uploadTime;

        this.activities[2].color = "#0bbd87";
        this.activities[2].icon = 'el-icon-check';
        this.activities[2].timestamp = checkTime;

        this.activities[3].color = "#0bbd87";
        this.activities[3].icon = 'el-icon-check';
        this.activities[3].content = "处理图片组("+ processedNum+"/"+ batchSize+")";
        this.activities[3].timestamp = finishTime;

        this.activities[4].color = "#0bbd87";
        this.activities[4].icon = "el-icon-check";
      }
      if (status === 7) {
        // 处理错误
        this.activities[4].color = "#ff4747";
        this.activities[4].icon = "el-icon-close";
        this.activities[4].content = "处理错误";
        if (!this.isFinish){
          this.isFinish = true;
          this.$message({
            showClose: true,
            message: '批处理处理错误',
            type: 'error'
          });
        }
      }
    },
    startCheckBatchStatus(){
      setInterval(()=>{
          let statusCheckForm = new FormData();
          // 身份识别数据
          statusCheckForm.append("uid", this.getUID());
          statusCheckForm.append("token", this.getToken());
          statusCheckForm.append("batchID", this.batchID);
          this.$axios.post("/NBI/Batch/checkStatus/",statusCheckForm,{
             headers: {'Content-Type': 'multipart/form-data'}
          }).then((response) => {
            this.updateProcessStatusShow(
                response.data.status,
                response.data.uploadTime,
                response.data.checkTime,
                response.data.finishTime,
                response.data.processedNum,
                response.data.batchSize,
            );
          })
      }, 5000);
    },
    uploadNewPackage(){
      let packageUploadForm = new FormData();
      // 身份识别数据
      packageUploadForm.append("uid", this.getUID());
      packageUploadForm.append("token", this.getToken());
      // 压缩包
      if (this.$refs.compressPackageInput.files[0].name.split('.')[1] !== "zip"){
        this.$message({
            showClose: true,
            message: '仅支持上传zip格式的压缩文件',
            type: 'error'
          });
          this.$refs.uploadPackageIcon.className = "el-icon-upload";
          this.$refs.uploadPackageFont.innerHTML = "点击上传";
          return;
      }
      packageUploadForm.append("package", this.$refs.compressPackageInput.files[0]);

      this.$refs.uploadPackageIcon.className = "el-icon-loading";
      this.$refs.uploadPackageFont.innerHTML = "上传中";

      this.$axios.post("/NBI/Batch/upload/compressPack/",packageUploadForm,{
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '账户信息错误，上传失败！',
            type: 'error'
          });
          this.$refs.uploadPackageIcon.className = "el-icon-upload";
          this.$refs.uploadPackageFont.innerHTML = "点击上传";
        }
        else if (response.data === 2){
          this.$message({
            showClose: true,
            message: '未能成功获取压缩包数据！',
            type: 'error'
          });
          this.$refs.uploadPackageIcon.className = "el-icon-upload";
          this.$refs.uploadPackageFont.innerHTML = "点击上传";
        }
        else if (response.data === 3){
          // 不是超级用户，不能上传
          this.$message({
            showClose: true,
            message: '您不是超级用户，不能使用批处理功能！',
            type: 'error'
          });
          this.$refs.uploadPackageIcon.className = "el-icon-upload";
          this.$refs.uploadPackageFont.innerHTML = "点击上传";
          this.moreMessage.noBatch = true;
        }
        else{
          // console.log(response.data);
          this.batchTitle = response.data.batchName;
          this.batchID = response.data.batchID
          this.isUploaded = true;
          this.activities[0].icon = "el-icon-check";
          this.activities[0].color = "#0bbd87";
          this.activities[1].icon = "el-icon-loading";
          this.activities[1].color = "#ff9854";

          this.startCheckBatchStatus();
        }
      });
    },
  },
  computed: {
    url(){
      return "/static/Data/Temp/"+this.Image_Compress + '?t=' + new Date().getTime();
    },
    srcList(){
      return [
        "/static/Data/Temp/"+this.Image_Compress + '?t=' + new Date().getTime(),
      ]
    },
  }

}
</script>

<style scoped>
button {
	border: none;
	outline: none;
}

.uploadPackageBtn{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 96%;
  margin-top: 3%;
  height: 82%;
  border: 2px dodgerblue dashed;
  background-color: #f3f3f3;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s ease;
}

.uploadPackageBtn:hover{
  border: 2px #004c94 dashed;
  background-color: #ffffff;
}

.aside-button {
  overflow: hidden;
  width: 350px;
  height: 45%;
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: column;
  border-right: solid 1px #e6e6e6;
  border-bottom: solid 1px #e6e6e6;
  position: relative;
}

.aside-block {
  overflow: hidden;
  width: 340px;
  height: 55%;
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: column;
  position: relative;
}

.el-header .header-title {
  font-weight: bold;
  font-size: 18px;
  text-align: left;
  line-height: 56px;
}

.el-header .header-last {
  height: 61px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-button {
  width: 90%;
  height: 35px;
  cursor: pointer;
  border: transparent 2px solid;
  /* background-clip: padding-box, border-box;
  background-origin: padding-box, border-box; */
  /* background-image: linear-gradient(#fff, #fff), linear-gradient(315deg, #6cc3de 0%, #767ff6 100%); */
  /* color: #6c8ede; */
  /* font-weight: bold; */
  box-shadow: 0px 0px 2px #409eff inset;
  border-radius: 3px;
  background-color: #409eff;
  color: white;
  transition: 0.3s ease;
  overflow: hidden;
}

.header-button:hover {
  /* color: #fff; */
  /* background-image: linear-gradient(135deg, #6cc3de 0%, #767ff6 100%); */
  border: solid 2px #fff;
  box-shadow: 0 0 4px #fff inset;
}

.el-header .header-follow {
  height: 61px;
  line-height: 61px;
  display: flex;
  justify-content: left;
  align-items: center;
}

.el-aside {
  text-align: center;
}

.el-main {
  background-color: #fff;
  text-align: center;
  padding: 0 7px 0 7px;
}

.el-container {
  background: linear-gradient(180deg,#f5f5fc,rgba(255,255,255,0) 100%);
  height: 100%;
  box-shadow: 0 20px 50px rgb(65 62 101 / 15%);
}

.el-table >>> .el-table__body .el-table__cell {
  padding: 1px 0;
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
</style>