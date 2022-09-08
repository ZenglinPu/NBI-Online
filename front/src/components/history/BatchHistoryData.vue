<template>
  <div id="history-container">
    <BatchHistoryQuery/>
    <div id="history-content" v-show="total > 0">
      <BatchHistoryTable/>
      <BatchHistoryPagination
        :total="total"
        :algin="'right'"
      />
    </div>
    <HistoryDefaultPage
      v-show="total == 0"
    />
  </div>
</template>

<script>

import BatchHistoryTable from "@/components/history/batchHistory/BatchHistoryTable";
import HistoryDefaultPage from '@/components/history/HistoryDefaultPage.vue'
import BatchHistoryPagination from "@/components/history/batchHistory/BatchHistoryPagination";
import BatchHistoryQuery from "@/components/history/batchHistory/BatchHistoryQuery";

export default {
  name: "BatchHistoryData",
  components: {
    BatchHistoryQuery,
    BatchHistoryTable,
    HistoryDefaultPage,
    BatchHistoryPagination
  },
  data() {
    return {
      totalPage: 0,
      totalImage: 10
    }
  },
  computed: {
    total() {
      return this.totalImage;
    }
  },
  mounted() {
    this.$bus.$on('historyTotalPage',(data)=>{
      // console.log('我是HistoryData组件，收到了总页数为',data);
      this.totalPage = data;
    });
    this.$bus.$on('historyTotalImage',(data)=>{
      // console.log('我是HistoryData组件，收到了总条数为',data);
      this.totalImage = data;
    });
  },
  beforeDestroy() {
    this.$bus.$off('historyTotalPage');
    this.$bus.$off('historyTotalImage');
  }
}
</script>

<style scoped>
#history-container {
  min-height: 171px;
  padding: 20px 5% 5px;
  width: 100%;
  height: 96%;
  overflow: auto;
  background: linear-gradient(180deg,#f5f5fc,rgba(255,255,255,0) 100%);
}

#history-content {
  width: 1300px;
  margin: 0 auto;
  box-shadow: 0 20px 50px rgb(65 62 101 / 15%);
  border-radius: 3px;
}
</style>