<template>
  <div class="table-container">
    <div class="table-header">
      <div style="width: 1%" class="table-header-index-td"><span class="table-header-index"></span></div>
      <div style="width: 15%"><span class="table-header-inner">批次名称</span></div>
      <div style="width: 15%"><span class="table-header-inner">上传时间</span></div>
      <div style="width: 10%"><span class="table-header-inner">过期时间</span></div>
      <div style="width: 15%"><span class="table-header-inner">附加信息</span></div>
    </div>
    <ul v-if="itemVisible">
      <li v-for="(item,hisIndex) in this.batchHistoryList" :key="hisIndex">
        <BatchHistoryItem :index="item.index" :batchName="item.batchName" :lastChangeTime="item.lastChangeTime"
         :expireTime="item.expireTime" :_id="item._id">
        </BatchHistoryItem>
      </li>
    </ul>
    <div v-if="!itemVisible" class="load-container">
      <HistoryLoadPage/>
    </div>
  </div>
</template>

<script>
import BatchHistoryItem from "@/components/history/batchHistory/BatchHistoryItem";
import HistoryLoadPage from '@/components/history/HistoryLoadPage.vue'

export default {
  name: 'BatchHistoryTable',
  components: {
    BatchHistoryItem,
    HistoryLoadPage
  },
  data(){
    return{
      totalPage: 1,
      currentPage: 1,
      pageSize:5,
      batchHistoryList: [{
          index: 1,
          batchName: "bob的批次",
          lastChangeTime:"2022-09-06 16:14:13",
          expireTime: "2022-09-12 16:14:13" ,
          _id: "item._id"
      }],
      reset: true,
      filter:{
        isFilter: false,
        filterType: '',
        filterValue: '',
      },
    }
  },
  computed: {
    itemVisible() {
      return this.reset;
    }
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
  },
}
</script>

<style scoped>
ul {
  margin: 0;
  padding: 0 0 5px 0;
  background: #fff;
}

li {
  list-style-type: none;
}

.table-container {
  width: 1300px;
  margin: 0 auto;
}

.table-header {
  background: #767ff6;
  border-radius: 3px 3px 0 0;
  margin-top: 5px;
  font-weight: 500;
  font-size: 16px;
  color: #fff;
  padding: 12px 0;
  border: #fff solid 7px;
  box-shadow: 0px 0px 8px #fff inset;;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
}

.table-header div {
  display: inline-block;
  text-align: center;
}

.table-header-index {
  width: 0;
  display: inline-block;
  text-align: center;
}

td {
  text-align: left;
  padding: 8px 31px;
}

.table-header-index-td {
  padding: 8px 20px;
}

.load-container {
  height: 429px;
  margin: 0 0 5px 0;
}
</style>