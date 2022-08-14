<template>
  <el-row class="query-container" :span="24">
    <QuerySearch></QuerySearch>
  </el-row>
</template>

<script>
import QuerySearch from '@/components/history/QuerySearch.vue'

export default {
  name: 'HistoryQuery',
  components: {
    QuerySearch
  }
}
</script>

<style>
.query-container {
  width: 1300px;
  margin: 0 auto;
}
</style>