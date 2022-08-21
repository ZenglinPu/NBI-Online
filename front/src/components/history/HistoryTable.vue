<template>
  <div class="table-container">
    <div class="table-header">
      <td>图片</td>
      <td>上传用户</td>
      <td>样本名称</td>
      <td>部位</td>
      <td>症状</td>
      <td>上传时间</td>
      <td>过期时间</td>
      <td>附加信息</td>
    </div>
    <ul>
      <li v-for="count in 10" :key="count"><HistoryItem></HistoryItem></li>
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
      historyShow:{

      }
    }
  },
  mounted() {
    this.downloadHistory(2,2);
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
    downloadHistory(currentPage, pageCount){
      let getHistoryForm = new FormData();
      // 身份识别数据
      getHistoryForm.append("uid", this.getUID());
      getHistoryForm.append("token", this.getToken());
      getHistoryForm.append("currentPage", currentPage);
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
          console.log(response.data);
        }
      })
    }
  },
}
</script>

<style scoped>
ul {
  margin: 0;
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

td {
  text-align: left;
  padding: 8px 53.5px;
}
</style>