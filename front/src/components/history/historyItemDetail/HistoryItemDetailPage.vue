<template>
    <div id="historyItemDetailContainer">
      <div id="detailTitleContainer">
        <div style="margin-left: 5%;height: 100%;width: 30%;font-family: 幼圆,serif;font-size: large;font-weight: bolder;display: flex;justify-content: start;align-items: center;color: #2a2a2a">
          <p>&emsp;&emsp;标本名称:&emsp;{{titleInfo.sampleName}}</p>
        </div>
        <div style="height: 100%;width: 20%;font-family: 幼圆,serif;font-size: small;font-weight: lighter;display: flex;flex-direction: column;justify-content: start;align-items: end;color: #00002c">
          <div style="width:100%;height:50%;text-align: left;">
            <p>&emsp;&emsp;上传时间:&emsp;{{titleInfo.uploadTime}}</p>
          </div>
          <div style="width:100%;height:50%;text-align: left;">
            <p>&emsp;&emsp;过期时间:&emsp;{{titleInfo.expiresTime}}</p>
          </div>
        </div>
        <div style="height: 100%;width: 40%;display: flex;justify-content: end;align-items: center;">
          <el-button style="width: 30%;height: 45%;display: flex;justify-content: center;align-items: center" type="danger" icon="el-icon-delete">删 除</el-button>
        </div>
      </div>
      <div id="detailInfoContainer">
        <div id="imageShowPart">
          <div style="height: 100%;width: 100%;display: flex;flex-direction: column;justify-content: center;align-items: center">
            <div style="height: 70%;margin-bottom: 5%;width: 90%;background-color: #2a2a2a;border: 3px solid black;display: flex;justify-content: center;align-items: center;">
              <img class="bigNBIImage" :src="imageShowInfo.NBIImageName">
            </div>
            <div style="height: 25%;width: 90%;display: flex;flex-direction: row;justify-content: space-between;align-items: center">
              <img class="srcImage" :src="imageShowInfo.src_blue">
              <img class="srcImage" :src="imageShowInfo.src_green">
              <img class="srcImage" :src="imageShowInfo.src_white">
            </div>
          </div>
        </div>
        <div id="imageAdjustPart">

        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: "HistoryItemDetailPage",
  props: ['GID'],
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
  mounted(){
    this.initDownloadImageInfo();
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
    initDownloadImageInfo(){
       let getItemInfoForm = new FormData();
      // 身份识别数据
      getItemInfoForm.append("uid", this.getUID());
      getItemInfoForm.append("token", this.getToken());
      // 图片_id
      getItemInfoForm.append("gid", this.GID);
      this.$axios.post("/NBI/HistoryDetail/",getItemInfoForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '登录状态错误！请重新登录。',
            type: 'error'
          });
        }
        else{
          console.log(response.data);
          this.titleInfo.sampleName = response.data.sampleName===""?'未命名':response.data.sampleName;
          this.titleInfo.expiresTime = response.data.expiresTime;
          this.titleInfo.uploadTime = response.data.uploadTime;

          this.imageShowInfo.NBIImageName = "/static/Data/NBI/"+response.data.imageNBIName;
          this.imageShowInfo.src_blue = "/static/Data/Blue/"+response.data.imageBlueName;
          this.imageShowInfo.src_green = "/static/Data/Green/"+response.data.imageGreenName;
          this.imageShowInfo.src_white = "/static/Data/White/"+response.data.imageWhiteName;
        }
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
.bigNBIImage{
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>