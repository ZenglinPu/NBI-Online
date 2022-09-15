<template>
  <div style="width: 100%;height: 100%">
    <div id="headerContainer">
      <c_header :singleOrMulti="singleOrMulti" :singleOrBatchHistory="singleOrBatchHistory" :switchFunctionPage="switchFunctionPage" :functionPage="functionPage" :accountPage="accountPage"></c_header>
    </div>
    <div id="mainFunctionContainer">
      <keep-alive include="SingleImageProcess,MultiImageProcess">
        <router-view></router-view>
      </keep-alive>
    </div>
    <div id="footerContainer">
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
      let arrstr = document.cookie.split("; ");
      for(let i = 0; i < arrstr.length; i ++){
        let temp = arrstr[i].split("=");
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
    },
    singleOrMulti(w){
      let functionPage = "/ImageProcess";
      if (w===1){
        functionPage = "/ImageProcess/SingleImage";
      }
      else if (w===2){
        functionPage = "/ImageProcess/MultiImage";
      }
      this.$router.push({
        path: functionPage,
      })
    },
    singleOrBatchHistory(w) {
      let functionPage = "/HistoryData";
      if (w===1){
        functionPage = "/HistoryData";
      }
      else if (w===2){
        functionPage = "/HistoryData/BatchHistoryData";
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
  min-width: 1500px;
  max-width: 1700px;
  min-height: 700px;
  max-height: 800px;
}
#headerContainer{
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#mainFunctionContainer{
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#footerContainer{
  width: 100%;
  height: 16%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
