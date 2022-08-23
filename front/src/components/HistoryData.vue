<template>
  <div id="history-container">
    <HistoryQuery/>
    <HistoryTable
      v-show="total > 0"
    />
    <HistoryDefaultPage
      v-show="total == 0"
    />
    <HistoryPagination
      v-show="total > 0"
      :total="total"
      :algin="'right'"
    />
  </div>
</template>

<script>
import HistoryQuery from '@/components/history/HistoryQuery.vue';
import HistoryTable from '@/components/history/HistoryTable.vue';
import HistoryDefaultPage from '@/components/history/HistoryDefaultPage.vue'
import HistoryPagination from '@/components/history/HistoryPagination.vue';

export default {
  name: "HistoryData",
  components: {
    HistoryQuery,
    HistoryTable,
    HistoryDefaultPage,
    HistoryPagination
  },
  data() {
    return {
      totalPage: 0,
      totalImage: 0
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
}
</style>