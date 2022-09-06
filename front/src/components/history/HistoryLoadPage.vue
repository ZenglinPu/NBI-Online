<template>
  <div class="load-page">
    <div class="page-content">
      <i class="el-icon-loading"></i>
      <p>{{loadPageTips}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HistoryDefaultPage',
  data() {
    return {
        loadPageTips:'加载中'
    }
  },
}
</script>

<style scoped>
.load-page {
  position: relative;
  margin: 0 7px;
}

.page-content {
  display: flex;
  /*实现垂直居中*/
  align-items: center;
  /*实现水平居中*/
  justify-content: center;
  padding-top: 135px;
}

.page-content p{
  line-height: 39px;
  font-size: 13px;
  color: #9195a3;
}
</style>