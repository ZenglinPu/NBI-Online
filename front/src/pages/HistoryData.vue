<template>
  <div id="history-container">
    <HistoryQuery/>
    <HistoryTable/>
    <HistoryPagination
      v-show="total > 0"
      :total="total"
      :page.sync="queryForm.page"
      :limit.sync="queryForm.listRows"
      :algin="'right'"
    />
  </div>
</template>

<script>
import HistoryQuery from '@/components/history/HistoryQuery.vue';
import HistoryTable from '@/components/history/HistoryTable.vue';
import HistoryPagination from '@/components/history/HistoryPagination.vue';

export default {
  name: "P_HistoryData",
  components: {
    HistoryQuery,
    HistoryTable,
    HistoryPagination
  },
  data() {
    return {
      total: 1,
      tableList: [],
      listLoading: false,
      queryForm: {
        page: 1,
        listRows: 10,
        keywords: '',
        _filter: {}, //头部筛选
      },
      deatilsPath: '', //表格当前行跳转路径
      options: [],
      conditionList: [], //自定义筛选条件
      columns: [], //筛选条件中的数据
      checkList: [], //筛选条件中选中的数据
      multipleList: [], //表格复选多选中的数据
    }
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