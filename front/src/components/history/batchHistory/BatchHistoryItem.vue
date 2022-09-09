<template>
  <div class="historyItemContainer">
    <span class="historyItemInner" style="width: 4%">
      <div id="history-index-inner">{{ index }}</div>
    </span>
    <span class="historyItemInner" style="width: 15%; font-weight: bold;">{{ batchName }}</span>
    <span class="historyItemInner" style="width: 20%">{{ lastChangeTimeShow }}</span>
    <span class="historyItemInner" style="width: 20%">
      <div id="expired-time" :style="expireBackground">{{ expireTimeShow }}</div>
    </span>
    <span class="historyItemInner" style="width: 15%">
      <el-button type="primary" plain @click="checkDetail(_id)">查看详情</el-button>
      <i class="el-icon-delete oneImageDeleteBtn" @click="deleteDetail(_id)"></i>
    </span>
  </div>
</template>
<script>
export default {
  name: "BatchHistoryItem",
  data() {
    return {

    };
  },
  props:{
    index:{
      type:String,
      required:true
    },
    batchName:{
      type:String,
      default:'未命名样本'
    },
    lastChangeTime:{
      type:String,
      required:true
    },
    expireTime:{
      type:String,
      required:true
    },
    //todo
    _id:{
      type:String,
      required:true
    }
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
    lastChangeTimeShow() {
      let date = new Date(parseInt(this.lastChangeTime) * 1000);
      let Year = date.getFullYear();
      let Month = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
      let Day = (date.getDate() < 10 ? '0' + date.getDate() : date.getDate());
      let Hour = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours());
      let Minute = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes());
      let Second = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
      let GMT =  Year + '-' + Month + '-' + Day + ' '+ Hour +':'+ Minute  + ':' + Second;

      //YEAR-MM-DD HH:mm:ss
      return GMT;
    },
    expireTimeShow() {
      let dateBegin = new Date(parseInt(Date.now()));
      let dateEnd = new Date(parseInt(this.expireTime) * 1000);
      // console.log(Date.now());
      // console.log(dateBegin);
      // console.log(this.expireTime);
      // console.log(dateEnd);
      
      //天
      let dateDiff = dateEnd.getTime() - dateBegin.getTime(); //时间差的毫秒数
      let dayDiff = Math.floor(dateDiff / (24 * 3600 * 1000)); //计算出相差天数
      //小时
      let leave1=dateDiff%(24*3600*1000); //计算天数后剩余的毫秒数
      let hours=Math.floor(leave1/(3600*1000)); //计算出小时数
      //分钟
      let leave2=leave1%(3600*1000); //计算小时数后剩余的毫秒数
      let minutes=Math.floor(leave2/(60*1000)); //计算相差分钟数
      //秒
      let leave3=leave2%(60*1000); //计算分钟数后剩余的毫秒数
      let seconds=Math.round(leave3/1000);

      let ret = '';
      // console.log("距离过期还有"+dayDiff+"天"+hours+"小时"+minutes+"分钟"+seconds+"秒");
      if (dayDiff > 0) {
        ret = dayDiff+'天';
      }else if (hours > 0) {
        ret = hours+'小时';
      }else if (minutes > 0) {
        ret = minutes+'分钟';
      }else if (seconds > 0) {
        ret = seconds+'秒';
      }else {
        ret = '过期'+(dayDiff*(-1)-1)+'天';
      }
      return ret;
    },
    //信息填写完整，才可以“保存结果”
    //永久显示绿色，暂时显示橙色，马上要删除显示红色
    expireBackground() {
      let str = this.expireTimeShow;
      let regOrange = RegExp('天');
      let regGray = RegExp('过');
      if (regGray.test(str)) {
        return { background: '#808080' };
      }else if (regOrange.test(str)) {
        return { background: '#ff9854' };
      }else {
        return { background: '#7ae588' };
      }
    },
  },
  methods: {
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
    //传入GID
    checkDetail(GID) {
      this.$router.push({
        name: 'HistoryItemDetailPage',
        params: {
          GID: GID
        }
      })
    },
    deleteDetail(GID) {
      this.$confirm('确认删除？（操作不可逆）')
      .then(() => {
        let deleteImageForm = new FormData();
        // 身份识别数据
        deleteImageForm.append("uid", this.getUID());
        deleteImageForm.append("token", this.getToken());
        //当前页面
        deleteImageForm.append("gid", GID);
        this.$axios.post("/NBI/History/deleteImage/", deleteImageForm, {
         headers: {'Content-Type': 'multipart/form-data'}
        }).then((response) => {
          if (response.data === 1){
            this.$message({
              showClose: true,
              message: '登录状态错误！请重新登录。',
              type: 'error'
            });
            this.$bus.$emit("changeStatus",{status: false, uname:''});
          }
          else if (response.data === 3){
            this.$message({
              showClose: true,
              message: '删除失败，处理错误！',
              type: 'error'
            });
          }
          else{
            this.$message({
              showClose: true,
              message: '图片已删除',
              type: 'success'
            });
            this.$bus.$emit("updateHistoryPage");
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
table {
  border-collapse: collapse;
  width: 100%;
}

#history-index-inner {
  font-size: 16px;
  /* padding-left: 7px; */
  width: 40px;
  height: 40px;
  background: #3ae6cc;
  color: ghostwhite;
  font-weight: bold;
  border-radius: 8%;
  margin: 0 auto;
  display:flex;
  justify-content: center;
  align-items: center;
}

.warning-row {
  background: oldlace;
}

.success-row {
  background: #f0f9eb;
}

#expired-time {
  font-weight: 500;
  font-size: 14px;
  color: #fff;
  width: 56px;
  padding: 6px 12px;
  border-radius: 10px;
  margin: 0 auto;
}

.historyItemContainer{
  height: 85px;
  border-bottom: .5px rgb(224, 224, 224) solid;
  background: #fefeff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
  margin: 0 7px;
}

.historyItemInner{
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  /* font-family: 幼圆,STHeiti,serif; */
  font-size: 14px;
  color: #9195a3;
}

.historyPageImageSmall{
  /*height: 100%;*/
  /*width: 100%;*/
  object-fit: contain;
}

.oneImageDeleteBtn{
  margin-left: 7px;
  cursor: pointer;
  transition: 0.3s ease;
}

.oneImageDeleteBtn:hover{
  background-color: white;
  color: red;
}

.el-button {
  padding: 8px 20px;
}

.el-button--primary.is-plain {
    color: #3ae6cc;
    background: #effffd;
    border-color: #3ae6cc;
}

.el-button--primary {
    color: #3ae6cc;
    background-color: #effffd;
    border-color: #3ae6cc;
}

.el-button--primary.is-plain:focus, .el-button--primary.is-plain:hover {
    background: #3ae6cc;
    border-color: #3ae6cc;
    color: #fff;
}

.el-button.is-plain:focus, .el-button.is-plain:hover {
    background: #3ae6cc;
    border-color: #3ae6cc;
    color: #fff;
}
</style>
