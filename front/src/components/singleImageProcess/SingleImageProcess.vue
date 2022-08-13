<template>
 <div id="singleImageProcess-container">
   <singleImageProcess_imageSendPart></singleImageProcess_imageSendPart>
   <singleImageProcess_imageGetPart></singleImageProcess_imageGetPart>
   <singleImageProcess_imageAdjust></singleImageProcess_imageAdjust>
 </div>
</template>

<script>
import singleImageProcess_imageSendPart from "@/components/singleImageProcess/singleImageProcess_imageSendPart";
import singleImageProcess_imageGetPart from "@/components/singleImageProcess/singleImageProcess_imageGetPart";
import singleImageProcess_imageAdjust from "@/components/singleImageProcess/singleImageProcess_imageAdjust";
export default {
  name: "SingleImageProcess",
  components:{singleImageProcess_imageSendPart, singleImageProcess_imageGetPart,singleImageProcess_imageAdjust}
}
</script>

<style scoped>
#singleImageProcess-container{
  width: 100%;
  height: 100%;
  overflow: auto;
  /*display: flex;*/
  /*flex-direction: column;*/
  /*align-items: center;*/
}
</style>