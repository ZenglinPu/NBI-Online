<template>
 <el-container>
    <el-aside width="350px">
      <button class="aside-button">
        <div id="uploadPackageBtn" @click="chooseNewPackage()">
            <i ref="uploadPackageIcon" class="el-icon-upload" style="color: darkgray;font-size: 80px"></i>
            <div ref="uploadPackageFont" class="el-upload__text" style="color: dodgerblue;margin-top: 20px">点击上传</div>
        </div>
        <div style="height: 18%;margin-top: 3%;width: 100%;text-align: center;color: #b6b6b6">只能上传zip/rar文件</div>
        <input @change="uploadNewPackage()" type="file" ref="compressPackageInput" style="visibility: hidden; height: 0">
    </button>
    <div class="aside-block-title">
        批次名称：{{batchTitle}}
      </div>
    <div class="aside-block">
        <el-timeline style="height: 353px; margin-top: 15px">
          <el-timeline-item
            v-for="(activity, index) in activities"
            :key="index"
            :icon="activity.icon"
            :type="activity.type"
            :color="activity.color"
            :size="activity.size"
            :timestamp="activity.timestamp">
            {{activity.content}}
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-aside>
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="4">
            <div class="header-title">
              <i class="el-icon-upload"></i>
              <span>  图片上传批处理</span>
            </div>
          </el-col>
          <el-col :span="16">
            <div class="header-follow">
              <el-popover
                placement="top-start"
                width="100"
                trigger="hover"
                content="写什么呢？大概是批处理的使用提示吧！">
                <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
              </el-popover>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="header-last">
              <button class="header-button">生成结果</button>
            </div>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-table
          :cell-style="{color: '#666', fontSize:'14px', height:'85px'}"
          :header-cell-style="{color: '#222222', fontSize:'14px'}"
          :data="tableData"
          style="width: 100%;"
          max-height="573">
          <el-table-column
            fixed
            prop="name"
            label="标本名称"
            width="262">
          </el-table-column>
          <el-table-column
            prop="blueCompress"
            label="蓝色光源图片"
            width="262">
            <template slot-scope="scope">
              <div style="height: 83px;display: flex;align-items: center;">
                <el-image
                  :src="'/static/Data/Temp/' + scope.row.blueCompress"
                  style="height: 83px;"
                >
                </el-image>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="greenCompress"
            label="绿色光源图片"
            width="262">
            <template slot-scope="scope">
              <div style="height: 83px;display: flex;align-items: center;">
                <el-image
                  :src="'/static/Data/Temp/' + scope.row.greenCompress"
                  style="height: 83px;"
                >
                </el-image>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            prop="whiteCompress"
            label="白色光源图片"
            width="262">
            <template slot-scope="scope">
              <div style="height: 83px;display: flex;align-items: center;">
                <el-image
                  :src="'/static/Data/Temp/' + scope.row.whiteCompress"
                  style="height: 83px;"
                >
                </el-image>
              </div>
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="120">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="deleteRow(scope.$index, tableData)"
                type="text"
                size="small">
                <i class="el-icon-delete oneImageDeleteBtn"></i>移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: "MultiImageProcess",
  data() {
    return {
      batchTitle: '',
      activities: [{
        content: '上传压缩包',
        timestamp: '2022-09-03 20:46',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-check',
        color: '#0bbd87'
      }, {
        content: '检查压缩包',
        timestamp: '2022-09-03 20:46',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-check',
        color: '#0bbd87'
      },{
        content: '处理图片组（18/18）',
        timestamp: '2022-09-03 20:46',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-check',
        color: '#0bbd87'
      }, {
        content: '打包处理结果',
        timestamp: '',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-loading',
        color: '#ff9854'
      }, {
        content: '',
        timestamp: '',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-more',
        color: '#808080'
      }],
      tableData: [{
        name: '王小虎',
        blueCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        greenCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        whiteCompress: 'result_compress_10@10*com~gdztfkvc.jpg'
      }, {
        name: '王小虎',
        blueCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        greenCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        whiteCompress: 'result_compress_10@10*com~gdztfkvc.jpg'
      }, {
        name: '王小虎',
        blueCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        greenCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        whiteCompress: 'result_compress_10@10*com~gdztfkvc.jpg'
      }, {
        name: '王小虎',
        blueCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        greenCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        whiteCompress: 'result_compress_10@10*com~gdztfkvc.jpg'
      }, {
        name: '王小虎',
        blueCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        greenCompress: 'result_compress_10@10*com~gdztfkvc.jpg',
        whiteCompress: 'result_compress_10@10*com~gdztfkvc.jpg'
      },]
    };
  },
  methods:{
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
    chooseNewPackage(){
      this.$refs.compressPackageInput.click();
    },
    uploadNewPackage(){
      let packageUploadForm = new FormData();
      // 身份识别数据
      packageUploadForm.append("uid", this.getUID());
      packageUploadForm.append("token", this.getToken());
      // 压缩包
      packageUploadForm.append("package", this.$refs.compressPackageInput.files[0]);

      this.$refs.uploadPackageIcon.className = "el-icon-loading";
      this.$refs.uploadPackageFont.innerHTML = "上传中";

      this.$axios.post("/NBI/Batch/upload/compressPack/",packageUploadForm,{
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message.error("账户信息错误，上传失败！");
          this.$refs.uploadPackageIcon.className = "el-icon-upload";
          this.$refs.uploadPackageFont.innerHTML = "点击上传";
        }
        else{
          console.log(response);
        }
      });
    }
  },
  computed: {
    url(){
      return "/static/Data/Temp/"+this.Image_Compress + '?t=' + new Date().getTime();
    },
    srcList(){
      return [
        "/static/Data/Temp/"+this.Image_Compress + '?t=' + new Date().getTime(),
      ]
    },
  }

}
</script>

<style scoped>
button {
	border: none;
	outline: none;
}

#uploadPackageBtn{
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 96%;
  margin-top: 3%;
  height: 82%;
  border: 2px dodgerblue dashed;
  background-color: #f3f3f3;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s ease;
}

#uploadPackageBtn:hover{
  border: 2px #004c94 dashed;
  background-color: #ffffff;
}

.aside-button {
  overflow: hidden;
  width: 100%;
  height: 35%;
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: column;
  background-color: #fff;
  border-right: solid 1px #e6e6e6;
  border-bottom: solid 1px #e6e6e6;
  position: relative;
}

.aside-block {
  position: relative;
  height: 55%;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column;
}

.aside-block-title {
  width: 70%;
  margin-left: 15%;
  height: 60px;
  justify-content: start;
  align-items: center;
  display: flex;
  color: #2e3857;
  font-family: 幼圆,serif;
  font-weight: bold;
}

.el-header {
  /* color: #fff; */
  text-align: center;
  height: 75px !important;
  /* background-image: linear-gradient(135deg, #6cc3de 0%, #767ff6 100%); */
  /* border: #fff solid 7px; */
  border: #fff solid 7px;
  /* box-shadow: 0px 0px 8px #fff inset; */
}

.el-header .header-title {
  font-weight: bold;
  font-size: 18px;
  text-align: left;
  line-height: 56px;
}

.el-header .header-last {
  height: 61px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-button {
  width: 50%;
  height: 30px;
  cursor: pointer;
  transition: 0.15s ease;
  border: transparent 2px solid;
  border-radius: 15px;
  background-clip: padding-box, border-box;
  background-origin: padding-box, border-box;
  /* background-image: linear-gradient(#fff, #fff), linear-gradient(315deg, #6cc3de 0%, #767ff6 100%); */
  /* color: #6c8ede; */
  font-weight: bold;
  box-shadow: 0px 0px 2px #6c8ede inset;
}

.header-button:hover {
  /* color: #fff; */
  /* background-image: linear-gradient(135deg, #6cc3de 0%, #767ff6 100%); */
  border: solid 2px #fff;
  box-shadow: 0px 0px 4px #fff inset;
}

.el-header .header-follow {
  height: 61px;
  line-height: 61px;
  display: flex;
  justify-content: left;
  align-items: center;
}

.el-aside {
  text-align: center;
}

.el-main {
  background-color: #fff;
  text-align: center;
  padding: 0 7px 0 7px;
}

.el-container {
  background: linear-gradient(180deg,#f5f5fc,rgba(255,255,255,0) 100%);
  height: 100%;
  box-shadow: 0 20px 50px rgb(65 62 101 / 15%);
}

.el-table >>> .el-table__body .el-table__cell {
  padding: 1px 0;
}
</style>