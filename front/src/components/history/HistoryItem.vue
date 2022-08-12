<template>
  <div >
    <tr :style="rowBackground">
      <td>
        <el-image style="width: 20px; height: 20px" :src="url" :preview-src-list="srcList">
        </el-image>
      </td>
      <td>{{ userName }}</td>
      <td>{{ sampleName }}</td>
      <td>{{partName}}</td>
      <td>{{diagnosis}}</td>
      <td>{{ uploadTime }}</td>
      <td>
        <button @click="checkDetail">查看详情</button>
      </td>
    </tr>
    <span></span>
  </div>
</template>
<script>
export default {
  data() {
    return {
      url: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      srcList: [
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
        "https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg",
        "https://fuss10.elemecdn.com/1/8e/aeffeb4de74e2fde4bd74fc7b4486jpeg.jpeg",
      ],
      userName: 'bob',
      sampleName: 'bob的标本',//标本名称
      partName:'胃',//部位
      diagnosis:'炎症',//术前诊断
      uploadTime: '2022-8-11',//
    };
  },
  computed: {
    //信息填写完整，才可以“保存结果”
    //永久显示绿色，暂时显示橙色，马上要删除显示红色
    //todo
    rowBackground() {
      return {background:'#f0f9eb'}
    }
  },
  methods: {
    checkDetail(){
      return
    }
  },
  name: "App",
};
</script>
<style>
table {
  border-collapse: collapse;
  width: 100%;
}

td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #8cdddd;
}

.warning-row {
  background: oldlace;
}

.success-row {
  background: #f0f9eb;
}

</style>
