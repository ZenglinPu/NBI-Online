<template>
  <div id="footer-container">
    <div class="info-container">
      <div class="footerImage-container">
        <img alt="图片加载失败" class="footerIcon" src="@/assets/icon01.png">
      </div>
      <p class="footerText">北京大学第一医院</p>
    </div>
    <div class="info-container">
      <div class="footerImage-container">
        <img alt="图片加载失败" class="footerIcon" src="@/assets/icon02.png">
      </div>
      <p class="footerText">北京邮电大学</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "C_Footer",
}
</script>

<style scoped>
#footer-container{
  width: 100%;
  height: 120px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  background-color: #07004f;
}
.info-container{
  width: 40%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}
.footerImage-container{
  width: 40%;
  height: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.footerIcon{
  width: 70%;
  object-fit: contain;
}
.footerText{
  color: white;
  font-weight: bold;
  font-family: 幼圆;
}
</style>