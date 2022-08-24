<template>
  <div
    class="public-search"
    :class="{ isActive: isActive }"
    @click.stop="handleSearch"
  >
    <el-input
      :placeholder="placeholderText"
      v-model="searchText"
      class="search"
      ref="search"
      clearable
      prefix-icon="el-icon-search"
      @input="searchHandler"
    ></el-input>
  </div>
</template>

<script>
export default {
  name: 'QuerySearch',
  data() {
    return {
      isActive: false,
      searchText: '',
    }
  },
  computed:{
    placeholderText() {
      if (!this.isActive) {
        return '搜索'
      }
      else {
        return '输入样本名关键字'
      }
    }
  },
  methods: {
    handleSearch() {
      let _this = this
      this.isActive = true
      this.$refs.search.focus()
      function otherClick() {
        if (_this.searchText == '') {
          _this.isActive = false
          document.body.removeEventListener('click', otherClick)
        }
      }
      document.body.addEventListener('click', otherClick)
    },
    searchHandler() {
      this.$emit('up-Search', this.searchText) //改变搜索字段的value
    },
  },
}
</script>

<style scoped>
.el-input, .search {
  line-height: 34px;
  padding: 0;
  pointer-events: none;
  font-size: 14px;
}

.el-input, .search >>> .el-input__inner {
  cursor: pointer;
  border: none;
}

.el-input, .search >>> .el-input__prefix {
  color: #767ff6;
}

.public-search {
  display: inline-block;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.3s ease-in-out;
}

.public-search >>> .el-input__inner {
  width: 70px;
  padding-right: 0;
  transition: all 0.3s ease-in-out;
}

.public-search >>>.el-input__inner::placeholder {
  color: #767ff6;
  transition: all 0.5s ease-in-out;
}

.isActive {
  box-shadow: inset 0 0px 1px rgb(0 0 0 / 0%), 0 6px 6px -6px #767ff6;
  transition: all 0.4s ease-in-out;
}

.isActive >>> .el-input__inner {
  width: 210px;
}

.isActive >>> .el-input__inner::placeholder {
  color: #b3b6c3;
  transition: all 0.5s ease-in-out;
}

.isActive >>> .el-input__prefix {
  color: #b3b6c3;
}
</style>