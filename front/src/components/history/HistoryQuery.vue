<template>
  <el-row class="query-container">
    <div style="width: 15%;height: 90%;justify-content: center;align-items: center;display: flex">
      <el-select v-model="searchValue" placeholder="请选择搜索方式" style="border: #767ff6 solid 1px;border-radius: 4px" @change="searchText='';dateRange='';isSearch=false">
        <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :disabled="item.disabled"
        >
        </el-option>
      </el-select>
    </div>
    <div style="width: 77%;height: 90%;justify-content: center;align-items: center;display: flex">
      <el-input
        v-show="searchValue === '1'"
        placeholder="请输入标本名称"
        v-model="searchText"
        ref="search"
        clearable
        prefix-icon="el-icon-search"
        style="border: #767ff6 solid 1px;border-radius: 4px"
        @keyup.enter.native="searchNewHistory()"
      ></el-input>
      <el-input
        v-show="searchValue === '2'"
        placeholder="请输入标本部位"
        v-model="searchText"
        ref="search"
        clearable
        prefix-icon="el-icon-search"
        style="border: #767ff6 solid 1px;border-radius: 4px"
        @keyup.enter.native="searchNewHistory()"
      ></el-input>
      <el-date-picker
        v-show="searchValue === '3'"
        v-model="dateRange"
        type="daterange"
        align="right"
        unlink-panels
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        :picker-options="pickerOptions"
        @blur="searchNewHistory()"
        style="border: #767ff6 solid 1px;border-radius: 4px;width: 100%;"
      >
      </el-date-picker>
    </div>
    <div style="width: 8%;height: 90%;justify-content: center;align-items: center;display: flex">
      <div v-show="!isSearch" @click="searchNewHistory()" class="filter-holder">
        <i class="iconfont icon-shaixuan" style="vertical-align: middle"></i>
        <span>  筛选</span>
      </div>
      <div v-show="isSearch" @click="getAllHistory()" class="filter-closer">
        <i class="el-icon-close" style="vertical-align: middle"></i>
        <span>  取消</span>
      </div>
    </div>
  </el-row>
</template>

<script>

export default {
  name: 'HistoryQuery',

  data() {
    return {
      options: [{
        value: '1',
        label: '标本名称',
        disabled: false,
      }, {
        value: '2',
        label: '标本部位',
        disabled: false,
      }, {
        value: '3',
        label: '上传时间',
        disabled: false,
      }],
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            picker.$emit('pick', [start, end]);
          }
        }]
      },
      searchValue: '1',
      searchText: '',
      dateRange: '',
      isSearch: false,
    }
  },
  methods:{
    searchNewHistory(){
      if (this.searchValue === '1'){
        // 根据标本名字搜索
        this.$bus.$emit('updateHistoryPageWithFilter', {"filterType": 1, "filterValue": this.searchText});
      }
      else if (this.searchValue === '2'){
        // 根据标本部位搜索
        this.$bus.$emit('updateHistoryPageWithFilter', {"filterType": 2, "filterValue": this.searchText});
      }
      else if (this.searchValue === '3'){
        // 根据标本上传时间段搜索
        if (this.dateRange === ''){
          this.$message({
            showClose: true,
            message: '搜索条件不能为空',
            type: 'error'
          });
          return;
        }
        this.$bus.$emit('updateHistoryPageWithFilter', {"filterType": 3, "filterValue": this.dateRange});
      }
      this.isSearch = true;
    },
    getAllHistory(){
      this.$bus.$emit('updateHistoryPage');
      this.isSearch = false;
    }
  }
}
</script>

<style>
.query-container {
  width: 1300px;
  height: 75px;
  margin: 0 auto;
  padding-bottom: 10px;
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: row;
}
.filter-holder {
  color: #4b56ff;
  cursor: pointer;
  transition: 0.3s ease;

}
.filter-holder:hover{
  color: #989ffc;
}
.filter-holder:focus{
  color: #989ffc;
}

.filter-closer {
  color: #d30000;
  cursor: pointer;
  transition: 0.3s ease;

}
.filter-closer:hover{
  color: #ff4c4c;
}
.filter-closer:focus{
  color: #ff4c4c;
}

</style>