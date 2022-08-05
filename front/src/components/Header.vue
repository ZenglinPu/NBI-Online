<template>
    <div id="mainPageHeader">
        <div id="iconContainer">
            <img src="@/assets/webicon.jpg" alt="图片加载失败" style="height: 80%; align-self: center; border-radius: 8%">
        </div>
        <div id="nameContainer">
            <div style="width: 100%; text-align: left; height: 45%; display: inline-flex">
                <p style="font-size: 120%;font-style: italic;line-height: 90%;vertical-align: center;font-weight: bolder">
                        NBI
                </p>
                <p style="font-size: 120%;font-style: normal;line-height: 90%;vertical-align: center;font-weight: bolder;margin-left: 30px">
                        Image
                    </p>
                <p style="font-size: 120%;font-style: normal;line-height: 90%;vertical-align: center;font-weight: bolder;margin-left: 30px">
                        Transformer
                    </p>
            </div>
            <div style="width: 100%; text-align: left; height: 25%; display: inline-flex;cursor: pointer" onclick="jumpToIDMG()">
                <p style="font-size: 86%;margin-top: 4%;font-style: normal;line-height: 90%;vertical-align: center;">
                        BUPT
                </p>
                <p style="font-size: 86%;margin-top: 4%;font-style: normal;line-height: 90%;vertical-align: center;margin-left: 5px">
                        -
                </p>
                <p style="font-size: 86%;margin-top: 4%;font-style: normal;line-height: 90%;vertical-align: center;margin-left: 5px">
                        IDMG
                </p>
            </div>
        </div>
        <div id="headerSwitchContainer">
            <div id="accountStatusContainer" @click="switchFunctionPage(4)">
                <p v-show="user.status" id="accountInfo">{{user.name}}</p>
                <p id="accountStatus" :style="userStatusColor">{{user.status === false? "登录 / 注册":"欢迎您"}}</p>
            </div>
            <div class="headerButton" :class="functionPage===1? selectedBtnClass:''"  @click="switchFunctionPage(1)"><p>图片处理</p></div>
            <div class="headerButton" :class="functionPage===2? selectedBtnClass:''"  @click="switchFunctionPage(2)"><p>用户中心</p></div>
            <div class="headerButton" :class="functionPage===3? selectedBtnClass:''"  @click="switchFunctionPage(3)"><p>历史数据</p></div>
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
  props:['switchFunctionPage', 'functionPage'],
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
      this.$axios.post('/NBI/User/checkByToken/', {
        "uid": uid,
        "token": token,
      }).then((response) => {
        const checkResult = response.data.check;
        const newToken = response.data.token;
        const uname = response.data.uname;
        if (checkResult === 0){
          this.user.status = false;
        }
        else if(checkResult === 1){
          this.user.status = false;
          alert("登录已过期，请重新登录");
          this.clearCookie("NBI_token");
        }
        else if(checkResult === 2){
          this.setCookie("NBI_token",newToken, 2, "/NBI");
          this.user.name = uname;
          this.user.status = true;
        }
      });
    },
  }
}

</script>

<style scoped>
#mainPageHeader{
    width: 100%;
    height: 90px;
    /*background-image: linear-gradient(to right, rgb(220, 244, 255) , rgb(168, 227, 255));*/
    background-color: rgb(168, 227, 255);
    background-repeat:no-repeat;
    overflow: hidden;
    float: right;
    display: inline-flex;
    z-index: 100;
}

#iconContainer{
    height: 100%;
    width: 8%;
    margin-left: 80px;
    display: flex;
    justify-content: center;
    overflow: hidden;
}

#nameContainer{
    height: 100%;
    width: 25%;
    margin-left: 3%;
}

#headerSwitchContainer{
    height: 100%;
    width: 60%;
    /* margin-left: 6%; */
    display: inline-flex;
    justify-content: right;
    overflow: hidden;
}

.headerButton{
    cursor: pointer;
    font-family: STHeiti;
    height: 100%;
    width: 20%;
    margin-right: 2%;
    transition: 0.3s ease;
    background: rgba(255, 255, 255, 0);
    display: flex;
    justify-content: center;
    align-items: center;
}

.headerButton:hover{
    background: rgba(255, 255, 255, 0.25);
    color: #000042;
}

.headerButton_selected{
    background: rgba(255, 255, 255, 0.28);
    color: #000042;
    border-bottom: white 2px solid;
}

#accountStatusContainer{
    width: 40%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: 0.2s ease;
    flex-direction: column;
    cursor: pointer;
    overflow: hidden;
}
#accountStatus{
    color: #2e2e2e;
    font-family: Arial, Helvetica, sans-serif;
    line-height: 20%;
    margin-top: 5px;
}
#accountInfo{
    color: #c91400;
    font-family: Arial, Helvetica, sans-serif;
    line-height: 20%;
}
</style>