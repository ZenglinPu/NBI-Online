<template>
    <div id="mainPageHeader">
        <div id="iconContainer">
            <img src="@/assets/webicon.jpg" alt="图片加载失败" style="height: 82%; align-self: center; border-radius: 50%">
        </div>
        <div id="nameContainer">
            <div style="width: 100%; text-align: left; height: 45%; display: inline-flex;">
                <p class="headerFont" style="color: #d1ffd3">
                        NBI
                </p>
                <p class="headerFont" style="margin-left: 10px; color: rgba(154,198,255,0.95)">
                        -
                </p>
                <p class="headerFont" style="margin-left: 10px">
                        Online
                </p>
            </div>
            <div style="width: 100%; text-align: left; height: 25%; display: inline-flex;cursor: pointer" @click="jumpToIDMG()">
                <p class="headerFont2">
                        BUPT
                </p>
                <p class="headerFont2" style="margin-left: 10px">
                        IDMG
                </p>
            </div>
        </div>
<!--        <div id="headerSwitchContainer">-->
<!--            <div id="accountStatusContainer" @click="switchFunctionPage(4)">-->
<!--                <p v-show="user.status" id="accountInfo">{{user.name}}</p>-->
<!--                <p id="accountStatus" :style="userStatusColor">{{user.status === false? "登录 / 注册":"欢迎您"}}</p>-->
<!--            </div>-->
<!--            <div class="headerButton" :class="functionPage===1? selectedBtnClass:''"  @click="switchFunctionPage(1)"><p>图片处理</p></div>-->
<!--            <div class="headerButton" :class="functionPage===2? selectedBtnClass:''"  @click="switchFunctionPage(2)"><p>用户中心</p></div>-->
<!--            <div class="headerButton" :class="functionPage===3? selectedBtnClass:''"  @click="switchFunctionPage(3)"><p>历史数据</p></div>-->
<!--        </div>-->
        <div id="accountInfoContainer">
          <div v-show="user.status" id="loginStatusContainer">
            <div class="accountName" title="用户中心" @click="switchFunctionPage(2)">{{ user.name }}</div>
          </div>
          <div v-show="!user.status" id="accountStatusContainer">-->
            <div class="accountBtn" title="登录" @click="accountPage(1)">Sign In</div>
            <div style="width: 2px; height: 50%;margin-left:10px;margin-right: 10px;background-color: #F8F8FF;"></div>
            <div class="accountBtn" title="注册" @click="accountPage(2)">Sign Up</div>
          </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "C_Header",
  data(){
    return {
      user:{
          name: "",
          status: false, // true表示登录
      },
      selectedBtnClass: "headerButton_selected",
    }
  },
  props:['accountPage', 'functionPage', 'switchFunctionPage'],
  computed:{
    userStatusColor(){
      if (this.user.status){
        return {color: "forestgreen"};
      }
      else{
        return {color: "red"};
      }
    }
  },
  mounted(){
    // 检查账户状态
    this.accountStatusCheck();
    this.$bus.$on('changeStatus', (data)=>{
      this.user.status = data.status;
      this.user.name = data.uname;
    });
  },
  beforeDestroy() {
    this.$bus.$off('changeStatus');
  },
  methods:{
    // cookie
    getCookie(objname){//获取指定名称的cookie的值
      const arrstr = document.cookie.split("; ");
      for(let i = 0; i < arrstr.length; i ++){
        const temp = arrstr[i].split("=");
        if(temp[0] === objname) return temp[1];
      }
      return null;
    },
    setCookie(name, value, hours, path) {
      const expires = new Date();
      expires.setTime(expires.getTime() + hours * 3600000);
      path = path === "" ? "" : ";path=" + path;
      const _expires = (typeof hours) == "string" ? "" : ";expires=" + expires.toUTCString();
      document.cookie = name + "=" + value + _expires + path;
    },
    clearCookie(name) {
      this.setCookie(name, "", -1, "/NBI");
    },
    getToken(){
      return this.getCookie("NBI_token");
    },
    getUID(){
      return this.getCookie("NBI_UID");
    },
    accountStatusCheck(){
      // 本地无token，未登录
      const token = this.getToken();
      if (token === null){
        this.user.status = false;
        return;
      }

      // 本地有token，与uid一起上传
      const uid = this.getUID();
      const fd = new FormData();
      fd.append("uid",uid);
      fd.append("token",token);
      let config = {
         headers: {'Content-Type': 'multipart/form-data'}
      };
      this.$axios.post('/NBI/User/checkByToken/', fd, config).then((response) => {
        const checkResult = response.data.check;
        const newToken = response.data.token;
        const uname = response.data.uname;
        if (checkResult === 0){
          this.user.status = false;
        }
        else if(checkResult === 1){
          this.user.status = false;
          this.$message({
            message: '您的登录已过期！',
            type: 'error',
          });
          this.clearCookie("NBI_token");
        }
        else if(checkResult === 2){
          this.setCookie("NBI_token",newToken, 2, "/NBI");
          this.user.name = uname;
          this.user.status = true;
        }
      });
    },
    jumpToIDMG(){
      window.location.href = "https://teacher.bupt.edu.cn/shaoyingxia/zh_CN/";
    }
  }
}

</script>

<style scoped>
#mainPageHeader{
    width: 100%;
    height: 70px;
    background-color: #07004f;
    background-repeat:no-repeat;
    overflow: hidden;
    float: right;
    display: flex;
    align-items: center;
    z-index: 100;
}
.headerFont{
  color: #f0f7ff;
  line-height: 90%;
  vertical-align: center;
  font-family: STHeiti;
}
.headerFont2{
  color: #f0f7ff;
  font-size: 70%;
  line-height: 90%;
  vertical-align: center;
  font-family: STHeiti;
}
#iconContainer{
    height: 70%;
    margin-left: 4%;
    width: 6%;
    display: flex;
    justify-content: center;
    overflow: hidden;
}

#nameContainer{
    height: 100%;
    width: 22%;
    margin-left: 3%;
}
#accountInfoContainer{
  height: 100%;
  width: 65%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
}
#accountStatusContainer{
    width: 40%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    overflow: hidden;
}
#loginStatusContainer{
    width: 40%;
    height: 100%;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    flex-direction: row;
    overflow: hidden;
    margin-right: 5%;
}
.accountBtn{
  width: 30%;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff0d5;
  font-family: STHeiti;
  font-size: small;
  border-radius: 5px;
  border: #F8F8FF 2px solid;
  transition: 0.3s ease;
}
.accountBtn:hover{
  cursor: pointer;
  background-color: #F8F8FF;
  color: #2a2a2a;
}
.accountName{
  width: 50%;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff0d5;
  font-family: STHeiti;
  font-size: small;
  border-bottom: rgba(248, 248, 255, 0.3) 2px solid;
  background-color: rgba(248, 248, 255, 0.15);
  border-radius: 5px;
  overflow: hidden;
  cursor: pointer;
}
</style>