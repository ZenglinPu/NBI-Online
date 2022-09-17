<template>
  <div :class="{ hidden: hidden }" class="pagination-container">
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :style="{'text-align':algin}"
      :background="background"
      :page-sizes="pageSizes"
      :page-size.sync="pageSize"
      :layout="layout"
      :total="total"
      v-bind="$attrs"
    />
  </div>
</template>

<script>
// import { scrollTo } from '@/utils/scroll-to'

export default {
  name: 'BatchHistoryPagination',
  props: {
    total: {
      required: true,
      type: Number,
    },
    page: {
      type: Number,
      default: 1,
    },
    limit: {
      type: Number,
      default: 5,
    },
    pageSizes: {
      type: Array,
      default() {
        return [5, 10, 15, 20]
      },
    },
    layout: {
      type: String,
      default: 'total, sizes, prev, pager, next, jumper',
    },
    background: {
      type: Boolean,
      default: true,
    },
    autoScroll: {
      type: Boolean,
      default: true,
    },
    hidden: {
      type: Boolean,
      default: false,
    },
    algin: {
      type: String,
      default: ()=>'center',
    },
  },
  computed: {
    currentPage: {
      get() {
        return this.page;
      },
      set(val) {
        this.$emit('update:page', val);
      },
    },
    pageSize: {
      get() {
        return this.limit;
      },
      set(val) {
        this.$emit('update:limit', val);
      },
    },
  },
  methods: {
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      this.$bus.$emit('historySizeChange',val);
    },
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
      this.$bus.$emit('historyCPChange',val);
    },
  }
}
</script>

<style scoped>
.pagination-container {
  background: #fefeff;
  width: 1300px;
  margin: 0 auto;
  border-radius: 0 0 5px 5px;
}
.pagination-container.hidden {
  display: none;
}

.el-pagination.is-background >>> .el-pager li:not(.disabled):hover {
    color: #cdb8ef;
}

.el-pagination.is-background >>> .el-pager li:not(.disabled).active {
    background-color: #f4edff;
    color: rgb(68, 68, 68);
}
</style>