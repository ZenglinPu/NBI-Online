<template>
  <div id="mainContainer">
    <div id="mainContainerInner">
      <div id="switchBtnContainer">
				<button class="switchBtn" @click="switchPage(1);" title="登录您的账号" id="user_loginBtn">登&emsp;&emsp;录</button>
				<button class="switchBtn" @click="switchPage(2);" title="注册新的账号" id="user_registerBtn">注&emsp;&emsp;册</button>
			</div>
      <div style="width: 94%;margin-left: 3%;margin-top: 6px;height: 3px;border-radius: 5%;background-color: #AAAAFF;"></div>
      <div id="mainContainer_switch">
        <div :class="sliderType">
          <!--账号登录-->
          <div id="user_subPage_login">
            <el-form class="loginForm" :rules="loginFormRule" ref="loginForm" :model="loginForm" label-width="50px">
              <el-form-item label="账户" prop="account">
                <el-input v-model="loginForm.account"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input type="password" v-model="loginForm.password" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item>
                <div style="width: 100%;display: flex;flex-direction: row;align-items: center;justify-content: center">
                  <div style="width: 50%;height: 100%">
                    <input ref="rememAC" type="checkbox" id="rememAC" name="rememAC"/>
                    <label for="rememAC" style="cursor: pointer;margin-right:9rem;color: blue;font-size: 16px;line-height: 30px;">记住我</label>
                  </div>
                  <div style="width: 45%;height: 100%;display: flex;justify-content: end;align-items: center;margin-right: 5%;">
                    <a class="fontLink" style="margin-left: 10%" @click="switchPage(2)">没有账号？立即注册</a>
                  </div>
                </div>
              </el-form-item>
              <input type="button" id="loginBtn" @click="loginCheck()" value="登      录"/>
            </el-form>
          </div>

          <!--账号注册-->
          <div id="user_subPage_register">
            <el-form class="registerForm" :rules="registerFormRule" ref="registerForm" :model="registerForm" label-width="18%">
              <el-form-item label="账户" prop="account">
                <el-input v-model="registerForm.account"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="registerForm.password" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="registerForm.checkPass" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="验证码" prop="vCode">
                <el-input style="width: 75%" v-model="registerForm.vCode" autocomplete="off"></el-input>
                <el-button style="margin-left: 5%;width: 20%;" type="primary" :loading="validateCodeSending">发送</el-button>
              </el-form-item>
              <input type="button" id="registerBtn" @click="registerCheck()" value="注      册"/>
            </el-form>
          </div>
        </div>
      </div>
    </div>
    <!-- slogan -->
    <div id="slogan">
        <p>-&emsp;登录NBI-Online解锁完整功能&emsp;-</p>
    </div>
  </div>

</template>

<script>
export default {
  name: "P_AccountPage",
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        if (this.registerForm.checkPass !== '') {
          this.$refs.registerForm.validateField('checkPass');
        }
        callback();
      }
    };
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.registerForm.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      sliderType: "mainContainer_switch_slider_left",
      validateCodeSending: false,
      loginForm: {
        account: "",
        password: "",
      },
      loginFormRule: {
        account: [
          { required: true, message: '请输入账户信息(邮箱地址)', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      registerForm:{
        account: "",
        password:"",
        checkPass: "",
        vCode: "",
      },
      registerFormRule: {
        account: [
          { required: true, message: '请输入账户信息(邮箱地址)', trigger: 'change' }
        ],
        password: [
          { required: true,  validator: validatePass, trigger: 'blur' }
        ],
        checkPass: [
          { required: true,  validator: validatePass2, trigger: 'blur' }
        ],
      },
    }
  },
  methods:{
    switchPage(w){
      if (w===1){
        this.sliderType = "mainContainer_switch_slider_left";
      }
      else if(w===2){
        this.sliderType = "mainContainer_switch_slider_right";
      }
    },
    getCookie(objname){//获取指定名称的cookie的值
      const arrstr = document.cookie.split("; ");
      for(var i = 0;i < arrstr.length;i ++){
          var temp = arrstr[i].split("=");
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
    loginCheck(){
      if (this.loginForm.account === "" || this.loginForm.password===""){
        this.$message({
          message: '请首先输入账号和密码',
          type: 'error'
        });
        return;
      }
      this.$axios.post('/NBI/User/checkLogin/', {
        "uid": this.loginForm.account,
        "pwd": this.loginForm.password,
        "token": this.getCookie("NBI_token"),
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            message: '该邮箱未注册！',
            type: 'error'
          });
        }
        else if (response.data === 2){
          this.$message({
            message: '密码错误！',
            type: 'error'
          });
        }
        else{
          // 登录成功
          this.setCookie("NBI_token",response.data.token, 2, "/NBI");
          this.setCookie("NBI_UID", response.data.uid, 72, "/NBI");
          this.$bus.$emit('changeStatus', {status: true, uname: response.data.uname});
          if (this.$refs.rememAC.checked){
            //记录pwd
            this.setCookie("NBI_pwd", this.loginForm.password, 72, "/NBI");
          }
          this.$message({
            message: '登录成功！页面将会自动跳转',
            type: 'success'
          });
          setTimeout(()=>{
            this.$router.push({path: "/ImageProcess"});
          }, 2000);
        }
      });
    },
    checkEmail(email){
      const myReg=/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
      return myReg.test(email);
    },
    registerCheck(){
      if (this.registerForm.checkPass !== this.registerForm.password){
        this.$message({
          message: '两次密码输入不一致',
          type: 'error'
        });
        return;
      }
      if (this.registerForm.account === null || this.registerForm.password === null){
        this.$message({
          message: '注册关键信息不能为空',
          type: 'error'
        });
        return;
      }
      if (!this.checkEmail(this.registerForm.account)){
        this.$message({
          message: '请输入符合规范的电子邮箱',
          type: 'error'
        });
        return;
      }
      this.$axios.post('/NBI/User/register/', {
        "email": this.registerForm.account,
        "pw": this.registerForm.password,
      }).then((response) => {
        if (response.data === 0){
          this.$message({
            message: '注册失败，该邮箱地址已被注册！',
            type: 'error'
          });
          this.registerForm.account = "";
          this.registerForm.password = "";
        }
        else if (response.data === 1){
          this.$message({
            message: '注册成功！请登录。',
            type: 'success'
          });
          setTimeout(()=>{
            this.switchPage(1);
          }, 3000);
        }
      });
    },
  },
  mounted(){
    const pwd = this.getCookie("NBI_pwd");
    if (pwd != null){
      this.loginForm.password = pwd;
      this.loginForm.account = this.getCookie("NBI_UID");
      this.$refs.rememAC.checked = true;
    }
    this.switchPage(this.$route.query.w);
  },
}
</script>

<style scoped>
#mainContainer{
    width: 34%;
    height: 80%;
    padding-top: 80px;
    overflow: hidden;
    /* display: flex; */
    align-items: center;
    /* justify-content: center; */
}

#mainContainerInner{
    width: 100%;
    /* 48 - 58 */
    /* height: 48%; */
    background-color: rgba(18, 124, 238, 0.19);
    transition: 0.2s ease;
    overflow: hidden;
}

#switchBtnContainer{
	width: 100%;
	padding-top: 20px;
	display: flex;
	justify-content: center;
}
.switchBtn{
	width: 46%;
	height: 40px;
	margin: 5px;
	border: royalblue solid 1px;
	background: #F8F8FF;
	cursor: pointer;
	transition: all 0.2s ease;
}
.switchBtn:hover{
	background: #AAAAFF;
}

#mainContainer_switch{
    overflow: hidden;
}

.mainContainer_switch_slider_left{
    margin-top: 3%;
    margin-left: 0;
    width: 200%;
    height: 285px;
    display: flex;
    flex-direction: row;
    transition: all 0.2s ease;
}

.mainContainer_switch_slider_right{
    margin-top: 3%;
    margin-left: -100%;
    width: 200%;
    height: 350px;
    display: flex;
    flex-direction: row;
    transition: all 0.2s ease;
}

#user_subPage_login{
  width: 100%;
  /*height: 100%;*/
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  transition: all 0.2s ease;
}

#user_subPage_register{
  width: 100%;
  /*height: 100%;*/
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  transition: all 0.2s ease;
}

.loginForm{
	width: 90%;
	white-space: nowrap;
}

.registerForm{
  width: 90%;
	white-space: nowrap;
}

input[type="checkbox"] {
    height: 18px;
    width: 18px;
    margin-top: 18px;
    margin-left: 10px;
}

#rememAC{
	margin-left: -30px;
  cursor: pointer;
}
#loginBtn{
	width: 100%;
	height: 45px;
	border: #1122AA solid 1px;
	background: transparent;
	cursor: pointer;
	transition: all 0.2s ease;
}
#loginBtn:hover{
    background-color: rgba(61, 255, 61, 0.378);
}
input[type="checkbox"] {
    height: 18px;
    width: 18px;
    margin-top: 18px;
    margin-left: 10px;
}

.fontLink{
	color: #1122AA;
	font-size: 16px;
}
.fontLink:hover{
	color: rgb(52, 86, 255);
	cursor: pointer;
}

#registerBtn{
	width: 100%;
	height: 45px;
    margin-top: 2px;
	border: #1122AA solid 1px;
	background: transparent;
	cursor: pointer;
	transition: all 0.2s ease;
}
#registerBtn:hover{
	color: white;
    background-color: #2244CC;
}
#slogan{
	width: 100%;
	margin-top: 20px;
	display: flex;
	justify-content: center;
	align-items: center;
	font-family: Arial, Helvetica, sans-serif;
	color: grey;
}
</style>