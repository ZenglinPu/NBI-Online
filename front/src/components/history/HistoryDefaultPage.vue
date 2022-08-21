<template>
  <div class="default-page">
    <div class="page-content">
      <img :src="defaultPageImgUrl" alt="" />
      <p>{{defaultPageTips}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ZnDefaultPage',
  data() {
    return {
        defaultPageImgUrl:'todo',
        defaultPageTips:'暂无数据'
    }
  },
}
</script>

<style scoped>
.default-page {
  width: 100%;
  height: 100%;
  position: relative;
}
</style>