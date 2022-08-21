<template>
  <div>
    <tr :style="rowBackground">
      <td>
        <el-image style="width: 20px; height: 20px" :src="url" :preview-src-list="srcList">
        </el-image>
      </td>
      <!-- <td>{{ userName }}</td> -->
      <td>{{ sampleName }}</td>
      <td>{{ partName }}</td>
      <td>{{ diagnosis }}</td>
      <td>{{ uploadTime }}</td>
      <td>
        <div id="expired-time">{{ expiredTime }}</div>
      </td>
      <td>
        <el-button type="primary" plain @click="checkDetail('g1')">查看详情</el-button>
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
      partName: '胃',//部位
      diagnosis: '炎症',//术前诊断
      uploadTime: '2022-8-11',//
      expiredTime: '永久保存',//
    };
  },
  computed: {
    //信息填写完整，才可以“保存结果”
    //永久显示绿色，暂时显示橙色，马上要删除显示红色
    //todo
    rowBackground() {
      return { background: '#fefeff' }
    }
  },
  methods: {
    //传入GID
    checkDetail(GID) {
      this.$router.push({
        name: 'HistoryItemDetailPage',
        params: {
          GID: GID
        }
      })
    }
  },
  name: "HistoryItem",
};
</script>
<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
}

td {
  text-align: center;
  padding: 8px;
  width: 8.5%;
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

#expired-time {
  font-weight: 500;
  font-size: 14px;
  color: #fff;
  width: 56px;
  background: rgb(122, 229, 136);
  padding: 6px 12px;
  border-radius: 10px;
  margin: 0 auto;
}

.el-button {
  padding: 8px 20px;
}
</style>
