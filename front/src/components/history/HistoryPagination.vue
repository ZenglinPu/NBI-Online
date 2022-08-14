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
  name: 'HistoryPagination',
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
      default: 10,
    },
    pageSizes: {
      type: Array,
      default() {
        return [10, 20, 30, 50]
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
        return this.page
      },
      set(val) {
        this.$emit('update:page', val)
      },
    },
    pageSize: {
      get() {
        return this.limit
      },
      set(val) {
        this.$emit('update:limit', val)
      },
    },
  },
  methods: {
    handleSizeChange(val) {
      this.$emit('pagination', { page: this.currentPage, limit: val })
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    },
    handleCurrentChange(val) {
      this.$emit('pagination', { page: val, limit: this.pageSize })
      if (this.autoScroll) {
        scrollTo(0, 800)
      }
    },
  },
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
</style>