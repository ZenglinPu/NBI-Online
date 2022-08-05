<template>
  <div id="side-container">
    <div style="margin-top: 30px; margin-left: 10px">
      <el-tree class="sideLabel" :data="choice_single" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
      <div style="height: 20px"></div>
      <el-tree class="sideLabel" :data="choice_multi" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
    </div>
  </div>
</template>

<script>
export default {
  name: "C_ImageProcess_Side",
  data(){
    return {
      choice_single: [
        {
          label: '单张图片生成',
          children: [
            {
              label: '源图片上传',
            },
            {
              label: 'NBI图片生成',
            },
            {
              label: '参数调整',
            }
          ]
        },
      ],
      choice_multi: [
        {
          label: '多张图片批量生成',
          children: [
            {
              label: '源图片上传',
            },
            {
              label: 'NBI图片生成',
            },
            {
              label: '参数调整',
            }
          ]
        },
      ],
      defaultProps: {
        children: 'children',
        label: 'label'
      }
    };
  },
  props:['singleOrMulti', 'whichProcessType'],
  methods: {
    handleNodeClick(data) {
      if (data.label === "单张图片生成" && this.whichProcessType !== 1){
        this.singleOrMulti(1);
      }
      else if (data.label === "多张图片批量生成"  && this.whichProcessType !== 2){
        this.singleOrMulti(2);
      }
      else{
        console.log(data.label);
      }
    }
  },
}
</script>

<style scoped>
#side-container{
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: start;
  background-color: rgb(168, 216, 255);
  overflow: hidden;
}
.sideLabel{
  background-color: rgba(239, 239, 255, 0);
  color: rgba(0, 0, 0, 0.75);
  font-family: Arial;
  padding-top: 3px;
  font-size: xxx-large;
}
</style>