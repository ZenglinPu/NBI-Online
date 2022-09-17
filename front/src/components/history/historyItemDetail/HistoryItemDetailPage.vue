<template>
  <div id="historyItemDetailContainer">
    <div id="detailTitleContainer">
      <div @click="backToHistory()" class="backBtn">
        <i class="el-icon-back"></i>
        <p>返回</p>
      </div>
      <div
          style="height: 100%;width: 30%;font-family: 幼圆,serif;font-size: large;font-weight: bolder;display: flex;justify-content: start;align-items: center;color: #2a2a2a">
        <p>&emsp;&emsp;标本名称:&emsp;{{ titleInfo.sampleName }}</p>
      </div>
      <div
          style="height: 100%;width: 20%;font-family: 幼圆,serif;font-size: small;font-weight: lighter;display: flex;flex-direction: column;justify-content: start;align-items: end;color: #00002c">
        <div style="width:100%;height:50%;text-align: left;">
          <p>&emsp;&emsp;上传时间:&emsp;{{ titleInfo.uploadTime }}</p>
        </div>
        <div style="width:100%;height:50%;text-align: left;">
          <p>&emsp;&emsp;过期时间:&emsp;{{ titleInfo.expiresTime }}</p>
        </div>
      </div>
      <div style="height: 100%;width: 40%;display: flex;justify-content: end;align-items: center;">
        <el-button style="width: 30%;height: 45%;display: flex;justify-content: center;align-items: center"
                   type="warning" icon="el-icon-download" @click="downloadResult()">下 载 结 果
        </el-button>
        <el-button style="width: 30%;height: 45%;display: flex;justify-content: center;align-items: center"
                   type="danger" icon="el-icon-delete" @click="deleteDetail()">删 除
        </el-button>
      </div>
    </div>
    <div id="detailInfoContainer">
      <div id="imageShowPart">
        <div
            style="height: 74%;width: 100%;display: flex;justify-content: center;align-items: center; background-color: #6a6f77">
          <el-image class="bigNBIImage" v-show="imageShowInfo.NBIImageName!=='None'" :src="imageShowInfo.NBIImageName"
                    :preview-src-list="imageShowInfo.srcList"></el-image>
        </div>
        <div
            style="height: 25%;margin-top: 1%;width: 100%;display: flex;justify-content: space-between;align-items: center;">
          <div
              style="height: 96%;width: 32%;display: flex;justify-content: center;align-items: center;border: 1px solid #e6e6e6; background-color: #6a6f77">
            <el-image class="bigNBIImage" v-show="imageShowInfo.src_blue!=='None'"
                      :src="imageShowInfo.src_blue"></el-image>
          </div>
          <div
              style="height: 96%;width: 32%;display: flex;justify-content: center;align-items: center;border: 1px solid #e6e6e6; background-color: #6a6f77">
            <el-image class="bigNBIImage" v-show="imageShowInfo.src_green!=='None'"
                      :src="imageShowInfo.src_green"></el-image>
          </div>
          <div
              style="height: 96%;width: 32%;display: flex;justify-content: center;align-items: center;border: 1px solid #e6e6e6; background-color: #6a6f77">
            <p v-show="imageShowInfo.src_white==='/static/Data/White/null'" style="color: whitesmoke">未上传白色图片</p>
            <el-image class="bigNBIImage" v-show="imageShowInfo.src_white!=='/static/Data/White/null'"
                      :src="imageShowInfo.src_white"></el-image>
          </div>
        </div>
      </div>
      <div id="imageAdjustPartContainer">
        <el-col :span="12">
          <ImageAdjust :GID="this.GID" ></ImageAdjust>
        </el-col>
        <el-col :span="12">
          <ImageInfoFormPart :GID="this.GID" ></ImageInfoFormPart>
        </el-col>
      </div>
    </div>
  </div>
</template>

<script>
import ImageInfoFormPart from "@/components/history/historyItemDetail/ImageInfoFormPart";
import ImageAdjust from "@/components/history/historyItemDetail/ImageAdjust";

export default {
  name: "HistoryItemDetailPage",
  props: ['GID'],
  components: {ImageAdjust, ImageInfoFormPart},
  data() {
    return {
      titleInfo: {
        sampleName: "",
        uploadTime: "",
        expiresTime: "",
      },
      imageShowInfo: {
        NBIImageName: "",
        src_blue: "",
        src_green: "",
        src_white: "",
        srcList: [],
      },
    }
  },
  mounted() {
    this.initDownloadImageInfo();
    //有些奇怪，权限还有问题
    this.$bus.$on("getAdjustImage",(data)=>{
      this.imageShowInfo.NBIImageName = "/static/Data/NBI/" + data.imageNBIName;
      this.imageShowInfo.srcList.push("/static/Data/NBI/" + data.imageNBIName);
      console.log("这里是hitoryItemDetailPage，更新后的srcList：",this.imageShowInfo.srcList)
    })
  },
  beforeDestroy() {
    this.$bus.$off("getAdjustImage")
  },
  methods: {
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
    initDownloadImageInfo() {
      let getItemInfoForm = new FormData();
      // 身份识别数据
      getItemInfoForm.append("uid", this.getUID());
      getItemInfoForm.append("token", this.getToken());
      // 图片_id
      getItemInfoForm.append("gid", this.GID);
      this.$axios.post("/NBI/HistoryDetail/", getItemInfoForm, {
        headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1) {
          this.$message({
            showClose: true,
            message: '登录状态错误！请重新登录。',
            type: 'error'
          });
          this.$bus.$emit("changeStatus", {status: false, uname: ''});
        } else {
          // console.log(response.data);
          this.titleInfo.sampleName = response.data.sampleName === "" ? '未命名' : response.data.sampleName;
          this.titleInfo.expiresTime = response.data.expiresTime;
          this.titleInfo.uploadTime = response.data.uploadTime;

          this.imageShowInfo.NBIImageName = "/static/Data/NBI/" + response.data.imageNBIName;
          this.imageShowInfo.srcList.push("/static/Data/NBI/" + response.data.imageNBIName);
          this.imageShowInfo.src_blue = "/static/Data/Blue/" + response.data.imageBlueName;
          this.imageShowInfo.src_green = "/static/Data/Green/" + response.data.imageGreenName;
          this.imageShowInfo.src_white = "/static/Data/White/" + response.data.imageWhiteName;
        }
      });
    },
    backToHistory() {
      window.history.back();
    },
    downloadResult() {
      return undefined;
    },
    deleteDetail() {
      this.$confirm('确认删除？（操作不可逆）')
          .then(() => {
            let deleteImageForm = new FormData();
            // 身份识别数据
            deleteImageForm.append("uid", this.getUID());
            deleteImageForm.append("token", this.getToken());
            //当前页面
            deleteImageForm.append("gid", this.GID);
            this.$axios.post("/NBI/History/deleteImage/", deleteImageForm, {
              headers: {'Content-Type': 'multipart/form-data'}
            }).then((response) => {
              if (response.data === 1) {
                this.$message({
                  showClose: true,
                  message: '登录状态错误！请重新登录。',
                  type: 'error'
                });
                this.$bus.$emit("changeStatus", {status: false, uname: ''});
              } else if (response.data === 3) {
                this.$message({
                  showClose: true,
                  message: '删除失败，处理错误！',
                  type: 'error'
                });
              } else {
                this.$message({
                  showClose: true,
                  message: '图片已删除',
                  type: 'success'
                });
                window.history.back();
                
              }
            });
          })
          .catch(() => {
          });
    },
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
  overflow: hidden;
}

#detailTitleContainer {
  width: 100%;
  height: 12%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  /* border-bottom: 2px solid #777777; */
  background: #f5f5fc;
}

#detailInfoContainer {
  width: 100%;
  height: 88%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

#imageShowPart {
  width: 45%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-top: 1px #e6e6e6 solid;
}

#imageAdjustPartContainer {
  width: 65%;
  height: 100%;
  border: 1px #e6e6e6 solid;
}

.bigNBIImage {
  height: 100%;
  object-fit: contain;
}

.backBtn {
  width: 5%;
  display: flex;
  justify-content: end;
  align-items: center;
  color: #2e46ff;
  transition: 0.3s ease;
  cursor: pointer;
}

.backBtn:hover {
  color: #000c73;
}
</style>