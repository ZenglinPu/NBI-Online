<template>
  <div id="userCenterPageContainer">
    <div v-show="isLogin" id="userCenterInner">
      <div id="userCenterHeader">
        <div style="width: 15%;height: 70%;display: flex;justify-content: center;align-items: center;">
          <img :src="headerIconSrc" id="userCenterHeader_icon" alt="加载失败">
        </div>
        <div style="width: 25%;height: 70%;display: flex;flex-direction: column;justify-content: center;align-items: start">
          <div style="width: 100%;height: 60%; display: flex;justify-content: start;align-items: center;">
            <p v-show="!isChangeUName" id="headerNameFont">{{uname}}</p>
            <el-tooltip v-show="isChangeUName" class="item" effect="dark" content="输入后按Enter键确认，最大长度为10个字符。" placement="top">
              <input maxlength="10" id="newUName" type="text" :value="uname" @blur="isChangeUName = false" @keyup.enter="uploadNewUName()" style="height: 68%;width: 90%;border-radius: 4px;border: 1px #0b007e solid;"/>
            </el-tooltip>
            <div @click="isChangeUName = true" class="el-icon-edit changeBtn"></div>
          </div>
          <div style="width: 100%;height: 35%; display: flex;justify-content: start;align-items: center;" :class="headerFont">
            <p>欢迎：{{rank===1?'普通':'尊贵的超级'}}用户</p>
            <el-popover
              placement="top-start"
              width="100"
              title="用户等级"
              trigger="hover"
              content="超级用户可以无限次生成/保存图片，且享有快速处理通道。">
              <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
            </el-popover>
          </div>
        </div>
        <div style="width: 60%;height: 70%;display: flex;flex-direction: row;justify-content: end; align-items: center">
          <div @click="isChangePWD = true" id="changePWDBtn" title="注销"><p>Change Password</p></div>
          <div @click="userLogOut()" id="logOutBtn" title="注销"><p>Sign Out</p></div>
        </div>
        <el-drawer
          title="修改密码"
          :visible.sync="isChangePWD"
          direction="ltr"
          >
          <div style="height: 80%;width: 90%;">
            <el-form ref="pwdForm" label-width="100px" class="demo-ruleForm">
              <el-form-item label="原密码" prop="oldPwd">
                <el-input type="password" v-model="pwdForm.oldPwd" autocomplete="off" show-password></el-input>
              </el-form-item>
              <el-form-item label="新密码" prop="newPwd">
                <el-input type="password" v-model="pwdForm.newPwd" autocomplete="off" show-password></el-input>
              </el-form-item>
              <el-form-item label="确认密码" prop="checkPwd">
                <el-input type="password" v-model="pwdForm.checkPwd" autocomplete="off" show-password></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitForm()">提交</el-button>
                <el-button @click="resetForm()">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-drawer>
      </div>
      <div id="userCenterInfo">
        <div style="border-bottom: 1px #0b007e solid;width: 100%;height: 29%;display: flex;flex-direction: row;align-items: center;justify-content: center;">
          <div class="infoTitle">
            <p>注册信息</p>
          </div>
          <div class="infoContent">
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 50%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              &emsp;&emsp;注册邮箱:&emsp;{{uid}}
            </div>
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 50%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              &emsp;&emsp;注册时间:&emsp;{{registerTime}}
            </div>
          </div>
        </div>
        <div style="border-bottom: 1px #0b007e solid;width: 100%;height: 29%;display: flex;flex-direction: row;align-items: center;justify-content: center;">
          <div class="infoTitle">
            <p>附加信息</p>
            <el-button @click="isChangeAdditionInfo = true" v-show="!isChangeAdditionInfo" icon="el-icon-edit" style="font-size: small;height: 20%;width: 20%;margin-left: 10px;display: flex;justify-content: center;align-items: center">修改</el-button>
            <el-button @click="uploadNewAdditionalInfo()" v-show="isChangeAdditionInfo" icon="el-icon-folder-checked" style="font-size: small;height: 20%;width: 20%;margin-left: 10px;display: flex;justify-content: center;align-items: center">保存</el-button>
          </div>
          <div class="infoContent">
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 50%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              <div style="width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;工作单位:&emsp;
                <p v-show="!isChangeAdditionInfo">
                  {{workPlace}}
                </p>
                <input type="text" @keyup.enter="uploadNewAdditionalInfo()" v-show="isChangeAdditionInfo" ref="workPlaceInput" :value="workPlace" style="height: 55%;width: 55%;border-radius: 4px;border: 1px #0b007e solid;"/>
              </div>
              <div style="border: 1px solid gray;border-right: none;width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;工作部门:&emsp;
                <p v-show="!isChangeAdditionInfo">
                  {{department}}
                </p>
                <input type="text" @keyup.enter="uploadNewAdditionalInfo()" v-show="isChangeAdditionInfo" ref="departmentInput" :value="department" style="height: 55%;width: 55%;border-radius: 4px;border: 1px #0b007e solid;"/>
              </div>
            </div>
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 50%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              <div style="border-right: 1px solid gray;width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;当前职称:&emsp;
                <p v-show="!isChangeAdditionInfo">
                  {{competent}}
                </p>
                <input type="text" @keyup.enter="uploadNewAdditionalInfo()" v-show="isChangeAdditionInfo" ref="competentInput" :value="competent" style="height: 55%;width: 55%;border-radius: 4px;border: 1px #0b007e solid;"/>
              </div>
            </div>
          </div>
        </div>
        <div style="border-bottom: 1px #0b007e solid;width: 100%;height: 30%;display: flex;flex-direction: row;align-items: center;justify-content: center;">
          <div class="infoTitle">
            <p>NBI相关信息</p>
          </div>
          <div class="infoContent">
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 50%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              <div style="height: 100%;width: 30%;display: flex;flex-direction: column;justify-content: start;align-items: center">
                <div style="height: 40%;width: 100%;margin: 0">
                  <p>&emsp;&emsp;用户等级:&emsp;{{rank===1?'普通':'超级'}}用户</p>
                </div>
                <div style="height: 20%;width: 100%;margin: 0">
                  <p style="height: 20%;font-size: small;font-family: 幼圆,serif;color: #0b007e" v-show="rank===2">&emsp;&emsp;过期时间:&emsp;{{expiresTime}}</p>
                </div>
              </div>
              <div style="height: 100%;width: 20%;display: flex;justify-content: center;align-items: center">
                <p class="fontLink">
                  超级用户有什么用？
                </p>
              </div>
              <div style="height: 100%;width: 20%;display: flex;justify-content: center;align-items: center">
                <p class="fontLink">
                  如何成为超级用户？
                </p>
              </div>
            </div>
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 50%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              <div style="width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;剩余次数:&emsp;
                {{leftTimes===-1?'不限':leftTimes}}
              </div>
              <div style="border: 1px solid gray;border-right: none;width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;总共生成次数:&emsp;
                {{totalTimes}}
              </div>
            </div>
          </div>
        </div>
        <div style="border-bottom: 1px #0b007e solid;width: 100%;height: 12%;display: flex;flex-direction: row;align-items: center;justify-content: center;">
          <div class="infoTitle">
            <p>邀请码</p>
            <el-popover
              placement="top-start"
              width="100"
              title="邀请码"
              trigger="hover"
              content="新用户注册当天内输入对方邀请码即可为对方增加30天超级用户权限！（每人仅限一次赠送机会，但是可以多次接收）">
              <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
            </el-popover>
          </div>
          <div class="infoContent">
            <div style="border: 1px solid gray;border-right: none;width:100%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
              <div style="background-color: black;border: 1px solid gray;border-right: none;width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;
                <p style="font-family: 幼圆,serif; font-size: medium;color: white;">{{inviteCode}}</p>
              </div>
              <div style="border: 1px solid gray;border-right: none;width:50%;height: 100%;display: flex; flex-direction: row;justify-content: start; align-items: center;">
                &emsp;&emsp;输入对方邀请码：
                <el-tooltip class="item" effect="dark" content="输入后按Enter键确认" placement="top">
                  <input type="text" ref="othersInviteCode" style="height: 55%;width: 55%;border-radius: 4px;border: 1px #0b007e solid;" @keyup.enter="inputInviteCode()"/>
                </el-tooltip>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-show="!isLogin" id="noInfoShow">
      <img src="/static/img/userCenterBG.png" style="width: 28%">
    </div>
  </div>
</template>

<script>
export default {
  name: "P_UserCenter",
  data(){
    return {
      isLogin: true,
      uname: "",
      uid: this.getUID(),
      rank: 1,
      registerTime: "",
      workPlace: "",
      department: "",
      competent: "",
      leftTimes: "",
      totalTimes: "",
      expiresTime: "",
      inviteCode: "",
      isChangeUName: false,
      isChangeAdditionInfo: false,
      isChangePWD: false,
      pwdForm:{
        oldPwd: "",
        newPwd: "",
        checkPwd: "",
      },
    }
  },
  computed:{
    headerIconSrc(){
      if (this.rank === 1){
        return "/static/img/normalUser.png";
      }
      else{
        return "/static/img/superUser.png";
      }
    },
    headerFont(){
      if (this.rank === 1){
        return "headerNormalFont";
      }
      else{
        return "headerSuperFont";
      }
    }
  },
  mounted() {
    this.getUserCenterInfo();
  },
  methods:{
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
    submitForm() {
      if (this.pwdForm.newPwd === "" || this.pwdForm.checkPwd === "" || this.pwdForm.oldPwd === ""){
        this.$message({
          showClose: true,
          message: '您必须输入原密码和新密码',
          type: 'error',
        });
        return;
      }
      if (this.pwdForm.newPwd !== this.pwdForm.checkPwd){
        this.$message({
          showClose: true,
          message: '您前后输入的新密码不一致',
          type: 'error',
        });
        return;
      }
      let changePwdForm = new FormData();
      changePwdForm.append("token", this.getToken());
      changePwdForm.append("uid", this.getUID());
      changePwdForm.append("oldPwd", this.pwdForm.oldPwd);
      changePwdForm.append("newPwd", this.pwdForm.newPwd);
      this.$axios.post("/NBI/User/uploadNewPwd/",changePwdForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response)=>{
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '您的账号状态错误！',
            type: 'error',
          });
        }
        else if(response.data === 2){
          this.$message({
            showClose: true,
            message: '原始密码错误，修改失败！',
            type: 'error',
          });
          this.resetForm();
        }
        else if (response.data === 3){
          this.$message({
            showClose: true,
            message: '新密码设置成功',
            type: 'success',
          });
          this.isChangePWD = false;
          this.resetForm();
        }
      });
    },
    resetForm() {
      this.pwdForm.oldPwd = "";
      this.pwdForm.newPwd = "";
      this.pwdForm.checkPwd = "";
      this.$refs.pwdForm.clearValidate();
    },
    inputInviteCode(){
      // 可以反复赠送的问题还没有解决
      let inviteCodeForm = new FormData();
      inviteCodeForm.append("token", this.getToken());
      inviteCodeForm.append("uid", this.getUID());
      inviteCodeForm.append("inviteCode", this.$refs.othersInviteCode.value);
      this.$axios.post("/NBI/User/inputInviteCode/",inviteCodeForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response)=>{
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '邀请码激活成功！已经为对方增加30天超级用户权限！',
            type: 'success',
          });
        }
        else if (response.data === -1){
          this.$message({
            showClose: true,
            message: '您已注册超过24小时，不能赠送',
            type: 'error',
          });
        }
        else if (response.data === -2){
          this.$message({
            showClose: true,
            message: '找不到目标用户，请检查您的邀请码是否正确',
            type: 'error',
          });
        }
        else if (response.data === -3){
          this.$message({
            showClose: true,
            message: '不能给自己赠送哦',
            type: 'error',
          });
        }
        else if (response.data === -4){
          this.$message({
            showClose: true,
            message: '您已经激活过了，一个账号仅可一次赠送，但可以多次接受赠送',
            type: 'error',
          });
        }
      });
    },
    uploadNewUName(){
      this.isChangeUName = false;
      let changeUnameForm = new FormData();
      changeUnameForm.append("token", this.getToken());
      changeUnameForm.append("uid", this.getUID());
      this.uname = document.getElementById("newUName").value;
      changeUnameForm.append("name",this.uname);
      this.$axios.post("/NBI/User/uploadNewUName/",changeUnameForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response)=>{
        if (response.data===1){
          this.$message({
            showClose: true,
            message: '您的账号状态错误！',
            type: 'error',
          });
        }else{
          this.$message({
            showClose: true,
            message: '修改用户名成功！',
            type: 'success',
          });
          this.$bus.$emit('changeStatus', {status: true, uname: this.uname});
        }
      });
    },
    uploadNewAdditionalInfo(){
      this.isChangeAdditionInfo = false;
      let newAddInfo = new FormData();
      newAddInfo.append("token", this.getToken());
      newAddInfo.append("uid", this.getUID());
      newAddInfo.append("workPlace", this.$refs.workPlaceInput.value);
      newAddInfo.append("department", this.$refs.departmentInput.value);
      newAddInfo.append("competent", this.$refs.competentInput.value);
      this.$axios.post("/NBI/User/uploadNewAddInfo/",newAddInfo, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response)=>{
        if (response.data===1){
          this.$message({
            showClose: true,
            message: '您的账号状态错误！',
            type: 'error',
          });
        }else{
          this.$message({
            showClose: true,
            message: '修改附加信息成功！',
            type: 'success',
          });
          this.workPlace = response.data.workPlace;
          this.department = response.data.department;
          this.competent = response.data.competent;
        }
      });
    },
    getUserCenterInfo(){
      let getUserInfoForm = new FormData();
      getUserInfoForm.append("token", this.getToken());
      getUserInfoForm.append("uid", this.getUID());
      let config = {
         headers: {'Content-Type': 'multipart/form-data'}
      };
      this.$axios.post("/NBI/User/getUserInfo/",getUserInfoForm, config).then((response)=>{
        // console.log(response)
        if (response.data===1){
          this.isLogin = false;
          this.$message({
            showClose: true,
            message: '没有找到您的用户信息，您可能是没有登录或通信不畅',
            type: 'error'
          });
        }else{
          this.isLogin = true;
          this.uname = response.data.name;
          this.rank = response.data.rank;
          this.registerTime = response.data.registerTime;
          this.workPlace = response.data.workPlace;
          this.department = response.data.department;
          this.competent = response.data.competent;
          this.leftTimes = response.data.TIMES_generate;
          this.totalTimes = response.data.SUM_generate;
          this.expiresTime = response.data.expiresTime;
          this.inviteCode = response.data.inviteCode;
        }
      });
    },
    userLogOut(){
      // 注销
      let logoutForm = new FormData();
      logoutForm.append("token", this.getToken());
      logoutForm.append("uid", this.getUID());
      this.$axios.post("/NBI/User/logout/",logoutForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response)=>{
        console.log(response)
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '注销失败，您的账号状态错误！',
            type: 'error'
          });
        }
        else if (response.data === 2){
          this.$message({
            showClose: true,
            message: '您已注销',
            type: 'warning',
          });
          this.isLogin = false;
          this.$bus.$emit('changeStatus', {status: false, uname: ""});
        }
      })
    },
  },
}
</script>

<style scoped>
#userCenterPageContainer{
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#userCenterInner{
  width: 75%;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
#noInfoShow{
  width: 75%;
  height: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#userCenterHeader{
  height: 20%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid #07004f;
}
#userCenterInfo{
  height: 77%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
#userCenterHeader_icon{
  height: 80%;
  border-radius: 5px;
  border: 1px #07004f solid;
}
.headerSuperFont{
  color: goldenrod;
  font-family: 幼圆,serif;
}
.headerNormalFont{
  color: gray;
  font-family: 幼圆,serif;
}
#headerNameFont{
  color: #07004f;
  font-family: "Droid Sans Mono", "DejaVu Sans Mono", monospace;
  font-weight: bolder;
  font-size: x-large;
  cursor: pointer;
  transition: 0.3s ease;
}
#headerNameFont:hover{
  color: #0b007e;
}
#logOutBtn{
  width: 25%;
  margin-left: 4%;
  height: 40%;
  border: 2px solid #ff4b4b;
  color: #0b007e;
  font-family: "Droid Sans Mono", "DejaVu Sans Mono", monospace;
  margin-right: 5%;
  transition: 0.3s ease;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: small;
}
#logOutBtn:hover{
  cursor: pointer;
  background-color: red;
  color: white;
}
#changePWDBtn{
  width: 25%;
  margin-left: 2%;
  height: 40%;
  border: 2px solid #006c00;
  color: #0b007e;
  font-family: "Droid Sans Mono", "DejaVu Sans Mono", monospace;
  transition: 0.3s ease;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: small;
}
#changePWDBtn:hover{
  cursor: pointer;
  background-color: #00ce02;
  color: white;
}
.changeBtn{
  margin-left: 10px;
  cursor:pointer;
  width: 20px;
  height: 20px;
  transition: 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}
.changeBtn:hover{
  background-color: gray;
}
.infoTitle{
  width: 24%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bolder;
  font-family: 幼圆,serif;
}
.infoContent{
  width: 76%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  font-family: 幼圆,serif;
}
.fontLink {
  font-size: small;
  font-family: 幼圆, serif;
  transition: 0.3s ease;
  color: #1122AA;
  cursor: pointer;
}
.fontLink:hover{
  color: #2e46ff;
}
</style>