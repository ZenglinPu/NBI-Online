<template>
 <div id="singleImageProcess-container">
   <div id="imageSendPartContainer">
     <singleImageProcess_imageSendPart></singleImageProcess_imageSendPart>
   </div>
   <div id="imageShowPartContainer">
     <singleImageProcess_imageGetPart></singleImageProcess_imageGetPart>
     <singleImageProcess_imageAdjust></singleImageProcess_imageAdjust>
   </div>
 </div>
</template>

<script>
import singleImageProcess_imageSendPart from "@/components/singleImageProcess/singleImageProcess_imageSendPart";
import singleImageProcess_imageGetPart from "@/components/singleImageProcess/singleImageProcess_imageGetPart";
import singleImageProcess_imageAdjust from "@/components/singleImageProcess/singleImageProcess_imageAdjust";
export default {
  name: "SingleImageProcess",
  components:{singleImageProcess_imageSendPart, singleImageProcess_imageGetPart, singleImageProcess_imageAdjust}
}
</script>

<style scoped>
#singleImageProcess-container{
  width: 100%;
  height: 100%;
  overflow: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
#imageSendPartContainer{
  width: 40%;
  height: 100%;
  border: 1px rgb(0, 149, 255) solid;
  border-right: none;
}
#imageShowPartContainer{
  width: 60%;
  height: 100%;
  border: 1px rgb(0, 149, 255) solid;
}
</style>