<template>
  <el-row class="query-container">
    <button class="filter-first" :style="filterFirstBorder" @click="changeFilterState()">
      <div class="filter-holder">
        <i class="iconfont icon-shaixuan" style="vertical-align: middle"></i>
        <span>  筛选</span>
      </div>
    </button>
    <div style="width: 15%;height: 90%;justify-content: center;align-items: center;display: flex" v-show="isFiltrate">
      <el-select v-model="searchValue" placeholder="请选择搜索方式" :popper-append-to-body="false" @change="searchText='';dateRange='';isSearch=false">
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
    <div class="filter-third" style="width: 70%;height: 90%;justify-content: center;align-items: center;display: flex" v-show="isFiltrate">
      <el-input
        v-show="searchValue === '1'"
        placeholder="请输入标本名称"
        v-model="searchText"
        ref="search"
        clearable
        prefix-icon="el-icon-search"
        @keyup.enter.native="searchNewHistory()"
      ></el-input>
      <el-input
        v-show="searchValue === '2'"
        placeholder="请输入标本部位"
        v-model="searchText"
        ref="search"
        clearable
        prefix-icon="el-icon-search"
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
        style="width: 100%"
      >
      </el-date-picker>
    </div>
    <button class="filter-last" :style="filterLastBackground" @click="filterLastEvent()" v-show="isFiltrate">
      <div v-show="!isSearch" class="filter-starter">
        <i class="el-icon-check" style="vertical-align: middle"></i>
        <span>  确定</span>
      </div>
      <div v-show="isSearch" class="filter-closer">
        <i class="el-icon-close" style="vertical-align: middle"></i>
        <span>  取消</span>
      </div>
    </button>
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
      isFiltrate: false
    }
  },
  computed: {
    filterFirstBorder() {
      if (!this.isFiltrate) {
        return { 'border-radius': '40px 40px 40px 40px' };
      } else {
        return { 'border-radius': '40px 0 0 40px' };
      }
    },
    filterLastBackground(){
      if (!this.isSearch) {
        return { 'background-image': 'linear-gradient(135deg, #6cc3de 0%, #767ff6 100%)' };
      } else {
        return { 'background-image': 'linear-gradient(135deg, #ff833b 0%, #cc0c0c 74%)' };
      }
    }
  },
  methods:{
    changeFilterState() {
      this.isFiltrate = !this.isFiltrate;
    },
    filterLastEvent(){
      if (!this.isSearch) {
        this.searchNewHistory();
      } else {
        this.getAllHistory();
      }
    },
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
button {
	border-radius: 0;
	border: none;
	outline: none;
}

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

.filter-first {
  width: 7%;
  height: 40px;
  justify-content: center;
  align-items: center;
  display: flex;
  background-image: linear-gradient(45deg, #7de1ff 0%, #85FFBD 100%);
  cursor: pointer;
  transition: 0.15s ease;
}

.filter-holder {
  color: #ffffff;
  font-size: 14px;
  font-weight: bold;
  transition: 0.15s ease;
}

.filter-first:hover {
  opacity: .8;
}

.filter-first:hover .filter-holder{
  color: #1d5a7d;
}

.filter-last {
  width: 8%;
  height: 40px;
  justify-content: center;
  align-items: center;
  display: flex;
  border-radius: 0 40px 40px 0;
  cursor: pointer;
  transition: 0.15s ease;
}

.filter-last:hover {
  opacity: 0.8;
}

.filter-starter,.filter-closer {
  color: #ffffff;
  transition: 0.15s ease;
  font-size: 14px;
  font-weight: bold;
}

.filter-last:hover .filter-starter,.filter-closer{
  color: #e5e3e3;
}

.el-select .el-input__inner {
  border-radius: 0;
  border-left: transparent;
}

.el-select .el-input.is-focus .el-input__inner {
  border-color: #3ae6cc !important;
}

.el-select .el-input__inner:focus {
  border-color: #3ae6cc !important;
}

.el-select .el-scrollbar .el-select-dropdown__item.selected {
  color: #3ae6cc;
}

.el-input .el-input__inner {
  border-radius: 0;
}

.filter-third .el-input .el-input__inner:focus {
  border-color: #3ae6cc !important;
}

.filter-third .el-date-editor.el-input__inner {
  border-radius: 0;
}

.filter-third .el-range-editor.is-active {
  border-color: #3ae6cc !important;
}
</style>