<template>
  <div id="history-container">
    <HistoryQuery/>
    <HistoryTable/>
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
import HistoryPagination from '@/components/history/HistoryPagination.vue';

export default {
  name: "HistoryData",
  components: {
    HistoryQuery,
    HistoryTable,
    HistoryPagination
  },
  data() {
    return {
      totalPage: 0
    }
  },
  computed: {
    total() {
      return this.totalPage*5;
    }
  },
  mounted() {
    this.$bus.$on('historyTotalPage',(data)=>{
      console.log('我是HistoryData组件，收到了总页数为',data);
      this.totalPage = data;
    });
  },
  beforeDestroy() {
    this.$bus.$off('historyTotalPage');
  }
}
</script>

<style scoped>
#history-container {
  min-height: 171px;
  padding: 20px 5% 5px;
  width: 100%;
  height: 100%;
  overflow: auto;
}
</style>