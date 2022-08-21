<template>
  <el-row class="query-container" :span="24">
    <QuerySearch></QuerySearch>
    <QueryFilter></QueryFilter>
  </el-row>
</template>

<script>
import QuerySearch from '@/components/history/QuerySearch.vue'
import QueryFilter from '@/components/history/QueryFilter.vue'

export default {
  name: 'HistoryQuery',
  components: {
    QuerySearch,
    QueryFilter
  }
}
</script>

<style>
.query-container {
  width: 1300px;
  margin: 0 auto;
}
</style>