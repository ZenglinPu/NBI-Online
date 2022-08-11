<template>
  <div style="width: 100%;height: 100%">
    <div id="header-container">
       <c_header :functionPage="functionPage" :accountPage="accountPage"></c_header>
    </div>
    <div id="mainFunction-container">
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </div>
    <div>
      <c_footer></c_footer>
    </div>
  </div>
</template>

<script>
import c_header from '@/components/Header'
import c_footer from '@/components/Footer'

export default {
  name: 'App',
  components: {
    c_header,
    c_footer,
  },
  data(){
    return {
      functionPage: 1,
    }
  },
  methods:{
    getCookie(objname){//获取指定名称的cookie的值
      var arrstr = document.cookie.split("; ");
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
    accountPage(w){
      this.$router.push({
        path: "/AccountPage",
        query: {w: w},
      })
    },
    switchFunctionPage(w){
      this.functionPage = w;
      let functionPage = "/ImageProcess";
      if (w===2){
        functionPage = "/UserCenter";
      }
      else if (w===3){
        functionPage = "/HistoryData";
      }
      this.$router.push({
        path: functionPage,
      })
    }
  }
}
</script>

<style>
html,body{
  height: 100%;
  margin: 0;
  padding: 0;
}
#header-container{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#mainFunction-container{
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #F8F8FF;
}
</style>
