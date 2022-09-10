<template>
  <div class="table-container">
    <div class="table-header">
      <div style="width: 1%" class="table-header-index-td"><span class="table-header-index"></span></div>
      <div style="width: 11%"><span class="table-header-inner">图片</span></div>
      <div style="width: 15%"><span class="table-header-inner">样本名称</span></div>
      <div style="width: 10%"><span class="table-header-inner">部位</span></div>
      <div style="width: 15%"><span class="table-header-inner">术前诊断</span></div>
      <div style="width: 15%"><span class="table-header-inner">上传时间</span></div>
      <div style="width: 10%"><span class="table-header-inner">过期时间</span></div>
      <div style="width: 15%"><span class="table-header-inner">附加信息</span></div>
    </div>
    <ul v-if="itemVisible">
      <li v-for="(item,hisIndex) in this.historyList" :key="hisIndex">
        <HistoryItem :index="item.index" :Image_Compress="item.Image_Compress" :sampleName="item.sampleName"
         :part="item.part" :preDiagnosis="item.preDiagnosis" :lastChangeTime="item.lastChangeTime"
         :expireTime="item.expireTime" :_id="item._id">
        </HistoryItem>
      </li>
    </ul>
    <div v-if="!itemVisible" class="load-container">
      <HistoryLoadPage/>
    </div>
  </div>
</template>

<script>
import HistoryItem from '@/components/history/HistoryItem.vue'
import HistoryLoadPage from '@/components/history/HistoryLoadPage.vue'

export default {
  name: 'BatchImgList',
  components: {
    HistoryItem,
    HistoryLoadPage
  },
  data(){
    return{
      totalPage: 0,
      totalImage: 0,
      currentPage: 1,
      pageSize:5,
      historyList: [{
        index: '1',
        sampleName: "样本",
        part: "胃",
        preDiagnosis:"胃癌",
        lastChangeTime:"2022-09-06 16:14:13",
        expireTime: "2022-09-12 16:14:13" ,
        _id: "item._id"
      }],
      reset: true,
      filter:{
        isFilter: false,
        filterType: '',
        filterValue: '',
      },
    }
  },
  computed: {
    itemVisible() {
      return this.reset;
    }
  },
  mounted() {
    this.downloadHistory(this.currentPage,this.pageSize);
    this.$bus.$on('historyCPChange',(data)=>{
      this.currentPage = data;
      this.reset = false;
      if (this.filter.isFilter){
        this.downloadHistoryWithFilter(data, this.pageSize, this.filter.filterType, this.filter.filterValue);
      }
      else{
        this.downloadHistory(this.currentPage,this.pageSize);
      }

    });
    this.$bus.$on('historySizeChange',(data)=>{
      this.pageSize = data;
      if (this.filter.isFilter){
        this.downloadHistoryWithFilter(1, this.pageSize, this.filter.filterType, this.filter.filterValue);
      }
      else{
        this.downloadHistory(1,this.pageSize);
      }
    });
    this.$bus.$on('updateHistoryPage', ()=>{
      if (this.filter.isFilter){
        this.downloadHistoryWithFilter(1, this.pageSize, this.filter.filterType, this.filter.filterValue);
      }
      else{
        this.downloadHistory(this.currentPage,this.pageSize);
      }

    });
    this.$bus.$on('updateHistoryPageWithFilter', (data)=>{
      this.downloadHistoryWithFilter(1, this.pageSize, data.filterType, data.filterValue);
      this.filter.isFilter = true;
      this.filter.filterType = data.filterType;
      this.filter.filterValue = data.filterValue;
    });
    this.$bus.$on('noFilter',()=>{
      this.filter.isFilter = false;
    });
  },
  beforeDestroy() {
    this.$bus.$off('historyCPChange');
    this.$bus.$off('historySizeChange');
    this.$bus.$off('updateHistoryPage');
    this.$bus.$off('updateHistoryPageWithFilter');
    this.$bus.$off('noFilter');
  },
  methods: {
    // cookie
    getCookie(objName){//获取指定名称的cookie的值
      const arrStr = document.cookie.split("; ");
      for(let i = 0; i < arrStr.length; i ++){
        const temp = arrStr[i].split("=");
        if(temp[0] === objName) return temp[1];
      }
      return null;
    },
    getToken(){
      return this.getCookie("NBI_token");
    },
    getUID(){
      return this.getCookie("NBI_UID");
    },
    //根据条件搜索数据并显示
    downloadHistoryWithFilter(currentPage, pageCount, filterType, filterValue){
      let getHistoryFilterForm = new FormData();
      // 身份识别数据
      getHistoryFilterForm.append("uid", this.getUID());
      getHistoryFilterForm.append("token", this.getToken());
      //当前页面
      getHistoryFilterForm.append("currentPage", currentPage);
      //显示条数
      getHistoryFilterForm.append("pageCount", pageCount);
      //过滤类型
      getHistoryFilterForm.append("filterType", filterType);
      //值
      if (filterType === 3){
        getHistoryFilterForm.append("filterValue", [filterValue[0].getTime(), filterValue[1].getTime()]);
      }
      else{
        getHistoryFilterForm.append("filterValue", filterValue);
      }
      // console.log(getHistoryFilterForm.get('filterType'), getHistoryFilterForm.get('filterValue'));
      this.$axios.post("/NBI/History/getHistoryWithFilter/", getHistoryFilterForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '登录状态错误！请重新登录。',
            type: 'error'
          });
          this.$bus.$emit("changeStatus",{status: false, uname:''});
        }
        else {
          // console.log(response.data);
          this.loadHistory(response.data.info,response.data.totalPage,response.data.totalImage);
        }
      });
    },
    //下载当前页面历史数据
    downloadHistory(currentPage, pageCount){
      let getHistoryForm = new FormData();
      // 身份识别数据
      getHistoryForm.append("uid", this.getUID());
      getHistoryForm.append("token", this.getToken());
      //当前页面
      getHistoryForm.append("currentPage", currentPage);
      //显示条数
      getHistoryForm.append("pageCount", pageCount);
      this.$axios.post("/NBI/History/display/",getHistoryForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '登录状态错误！请重新登录。',
            type: 'error'
          });
          this.$bus.$emit("changeStatus",{status: false, uname:''});
        }
        else {
          this.loadHistory(response.data.info,response.data.totalPage,response.data.totalImage)
        }
      })
    },
    //载入下载的历史数据
    loadHistory(data,totalPage,totalImage){
      // console.log(totalPage);
      // for (var key in data) {
      //   var item = data[key];
      //   console.log(item);
      // }
      this.totalPage = totalPage;
      this.totalImage = totalImage;
      this.historyList.splice(0);
      for (var key in data) {
        var item = data[key];
        // console.log(item.Image_Compress);
        this.historyList.push({
          Image_Compress: item.Image_Compress,
          expireTime: item.expireTime,
          index: item.index,
          lastChangeTime: item.lastChangeTime,
          part: item.part,
          preDiagnosis: item.preDiagnosis,
          sampleName: item.sampleName,
          _id: item._id
        })
      }
      // // console.log(this.historyList);

      this.sendTotalPage();
      this.sendTotalImage();

      this.reset = true;//重建组件
      // console.log(this.itemVisible+'后');
    },
    sendTotalPage() {
      this.$bus.$emit('historyTotalPage',this.totalPage);
    },
    sendTotalImage() {
      this.$bus.$emit('historyTotalImage',this.totalImage);
    }
  },
}
</script>

<style scoped>
ul {
  margin: 0;
  padding: 0 0 5px 0;
  background: #fff;
}

li {
  list-style-type: none;
}

.table-container {
  width: 1300px;
  margin: 0 auto;
}

.table-header {
  background: #767ff6;
  border-radius: 3px 3px 0 0;
  margin-top: 5px;
  font-weight: 500;
  font-size: 16px;
  color: #fff;
  padding: 12px 0;
  border: #fff solid 7px;
  box-shadow: 0px 0px 8px #fff inset;;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
}

.table-header div {
  display: inline-block;
  text-align: center;
}

.table-header-index {
  width: 0;
  display: inline-block;
  text-align: center;
}

td {
  text-align: left;
  padding: 8px 31px;
}

.table-header-index-td {
  padding: 8px 20px;
}

.load-container {
  height: 429px;
  margin: 0 0 5px 0;
}
</style>