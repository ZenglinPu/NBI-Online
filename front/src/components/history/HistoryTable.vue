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
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
    <HistoryItem></HistoryItem>
  </div>
</template>

<script>
import HistoryItem from '@/components/history/HistoryItem.vue'

export default {
  name: 'HistoryTable',
  components: {
    HistoryItem
  }
}
</script>

<style scoped>
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