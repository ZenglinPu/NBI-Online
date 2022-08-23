<template>
  <div class="default-page">
    <div class="page-content">
      <img src="@/assets/history-default-icon.png" alt="查找完毕" />
      <p>{{defaultPageTips}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HistoryDefaultPage',
  data() {
    return {
        defaultPageTips:'无匹配对象'
    }
  },
}
</script>

<style scoped>
.default-page {
  width: 100%;
  position: relative;
}

.page-content {
  display: flex;
  /*实现垂直居中*/
  align-items: center;
  /*实现水平居中*/
  justify-content: center;
  margin-top: 165px;
}

.page-content img{
  width: 15%;
}

.page-content p{
  line-height: 39px;
  font-size: 13px;
  color: #9195a3;
}
</style>