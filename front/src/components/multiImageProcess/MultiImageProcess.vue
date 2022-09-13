<template>
 <el-container>
    <el-aside width="350px">
      <div style="height: 5%; position: relative; background: #fff; border-right: solid 1px #e6e6e6;"></div>
      <button class="aside-button">
        <div class="aside-plus">
          <el-upload
            class="upload-demo"
            drag
            action="/NBI/Batch/upload/compressPack/"
            :headers="uploadPackageHeaders"
            >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">只能上传zip/rar文件</div>
          </el-upload>
        </div>
      </button>
      <!-- <div class="aside-block-title">
        批次名称：{{batchTitle}}
      </div> -->
      <div class="aside-block">
        <el-timeline style="margin-top: 55px">
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
      // batchTitle: '',
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
    uploadPackageHeaders(){
      return {
        "utoken": this.getToken(),
        "uid": this.getUID(),
      }
    }
  }

}
</script>

<style scoped>
button {
	border: none;
	outline: none;
}

.aside-button {
  width: 100%;
  height: 40%;
  justify-content: center;
  /* align-items: center; */
  display: flex;
  background-color: #fff;
  /* cursor: pointer; */
  transition: 0.15s ease;
  /* border-image: linear-gradient(225deg, #7de1ff 0%, #6cc3de 100%); */
  border-right: solid 1px #e6e6e6;
  border-bottom: solid 1px #e6e6e6;
  position: relative;
}

.aside-plus .upload-demo >>> .el-upload-dragger {
  width: 330px;
  transition: 0.15s ease;
}

.aside-plus .upload-demo >>> .el-upload-dragger:hover .el-upload__text {
  color: #9195a3;
  transition: 0.15s ease;
}

.aside-plus .upload-demo >>> .el-upload__tip {
  color: #9195a3;
}

.aside-block {
  position: relative;
  align-items: center;
  display: flex;
  flex-direction: column;
}

/* .aside-block-title {
  width: 100%;
  height: 5%;
  justify-content: center;
  align-items: center;
  display: flex;
  color: #9195a3;
  font-weight: bold;
  background-color: #fff;
  border-right: solid 1px #e6e6e6;
  border-bottom: solid 1px #e6e6e6;
  position: relative;
} */

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
  /* background-clip: padding-box, border-box;
  background-origin: padding-box, border-box; */
  /* background-image: linear-gradient(#fff, #fff), linear-gradient(315deg, #6cc3de 0%, #767ff6 100%); */
  /* color: #6c8ede; */
  /* font-weight: bold; */
  box-shadow: 0px 0px 2px #409eff inset;
  border-radius: 3px;
  background-color: #409eff;
  color: white;
  transition: 0.3s ease;
  overflow: hidden;
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