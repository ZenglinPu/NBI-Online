<template>
  <div class="table-container">
    <div class="table-header">
      <td><span class="table-header-inner">序号</span></td>
      <td><span class="table-header-inner">图片</span></td>
      <!-- <td>上传用户</td> -->
      <td><span class="table-header-inner">样本名称</span></td>
      <td><span class="table-header-inner">部位</span></td>
      <td><span class="table-header-inner">症状</span></td>
      <td><span class="table-header-inner">上传时间</span></td>
      <td><span class="table-header-inner">过期时间</span></td>
      <td><span class="table-header-inner">附加信息</span></td>
    </div>
    <ul>
      <li v-for="(item,hisIndex) in this.historyList" :key="hisIndex">
        <HistoryItem :index="item.index" :Image_Compress="item.Image_Compress" :sampleName="item.sampleName" 
         :part="item.part" :preDiagnosis="item.preDiagnosis" :lastChangeTime="item.lastChangeTime" 
         :expireTime="item.expireTime" :_id="item._id">
        </HistoryItem>
    </ul>
  </div>
</template>

<script>
import HistoryItem from '@/components/history/HistoryItem.vue'

export default {
  name: 'HistoryTable',
  components: {
    HistoryItem
  },
  data(){
    return{
      totalPage: 0,
      historyList: []
    }
  },
  mounted() {
    this.downloadHistory(1,5);
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
    //下载当前页面历史数据
    downloadHistory(currentPage, pageCount){
      let getHistoryForm = new FormData();
      // 身份识别数据
      getHistoryForm.append("uid", this.getUID());
      getHistoryForm.append("token", this.getToken());
      //当前页面
      getHistoryForm.append("currentPage", currentPage);
      //显示条数
      getHistoryForm.append("pageCount", pageCount);
      this.$axios.post("/NBI/History/display/",getHistoryForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '登录状态错误！请重新登录。',
            type: 'error'
          });
        }
        else {
          this.loadHistory(response.data.info,response.data.totalPage)
        }
      })
    },
    //载入下载的历史数据
    loadHistory(data,totalPage){
      console.log(totalPage);
      // for (var key in data) {
      //   var item = data[key];
      //   console.log(item);
      // }
      this.totalPage = totalPage;
      for (var key in data) {
        var item = data[key];
        this.historyList.push({
          Image_Compress: item.Image_Compress,
          expireTime: item.expireTime,
          index: item.index,
          lastChangeTime: item.lastChangeTime,
          part: item.part,
          preDiagnosis: item.preDiagnosis,
          sampleName: item.sampleName,
          _id: item._id
        })
      }
      console.log(this.historyList);
    }
  },
}
</script>

<style scoped>
ul {
  margin: 0;
  padding: 0;
}

li {
  list-style-type: none;
}

.table-container {
  width: 1300px;
  margin: 0 auto;
}

.table-header {
  background: rgb(81, 158, 245);
  border-radius: 5px 5px 0 0;
  margin-top: 5px;
  font-weight: 500;
  font-size: 16px;
  color: #fff;
  padding: 12px 0;
}

.table-header-inner {
  width: 100px;
  display: inline-block;
  text-align: center;
}

td {
  text-align: left;
  padding: 8px 31px;
}
</style>