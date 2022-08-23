<template>
  <div>
    <tr style="background: '#fefeff'">
      <td class="history-index"><div id="history-index-inner">{{ index }}</div></td>
      <td class="history-content">
        <el-image style="height: 20px" :src="url" :preview-src-list="srcList">
        </el-image>
      </td>
      <!-- <td>{{ userName }}</td> -->
      <td class="history-content">{{ sampleName }}</td>
      <td class="history-content">{{ part }}</td>
      <td class="history-content">{{ preDiagnosis }}</td>
      <td class="history-content">{{ lastChangeTimeShow }}</td>
      <td class="history-content">
        <div id="expired-time" :style="expireBackground">{{ expireTimeShow }}</div>
      </td>
      <td class="history-content">
        <el-button type="primary" plain @click="checkDetail(_id)">查看详情</el-button>
      </td>
    </tr>
    <span></span>
  </div>
</template>
<script>
export default {
  data() {
    return {
      url: "/static/Data/Temp/"+this.Image_Compress,
      srcList: [
        "/static/Data/Temp/"+this.Image_Compress,
        "https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg",
        "https://fuss10.elemecdn.com/1/8e/aeffeb4de74e2fde4bd74fc7b4486jpeg.jpeg",
      ],
    };
  },
  props:{
    index:{
      type:String,
      required:true
    },
    Image_Compress:{
      type:String,
      default:''
    },
    sampleName:{
      type:String,
      default:'未命名样本'
    },
    part:{
      type:String,
      default:'未知'
    },
    preDiagnosis:{
      type:String,
      default:'未知'
    },
    lastChangeTime:{
      type:String,
      required:true
    },
    expireTime:{
      type:String,
      required:true
    },
    _id:{
      type:String,
      required:true
    }
  },
  computed: {
    lastChangeTimeShow() {
      let date = new Date(parseInt(this.lastChangeTime) * 1000);
      let Year = date.getFullYear();
      let Month = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
      let Day = (date.getDate() < 10 ? '0' + date.getDate() : date.getDate());
      let Hour = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours());
      let Minute = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes());
      let Second = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
      let GMT =  Year + '-' + Month + '-' + Day + ' '+ Hour +':'+ Minute  + ':' + Second;

      //YEAR-MM-DD HH:mm:ss
      return GMT;
    },
    expireTimeShow() {
      let dateBegin = new Date(parseInt(Date.now()));
      let dateEnd = new Date(parseInt(this.expireTime) * 1000);

      console.log(Date.now());
      console.log(dateBegin);
      console.log(this.expireTime);
      console.log(dateEnd);
      
      //天
      let dateDiff = dateEnd.getTime() - dateBegin.getTime(); //时间差的毫秒数
      let dayDiff = Math.floor(dateDiff / (24 * 3600 * 1000)); //计算出相差天数
      //小时
      let leave1=dateDiff%(24*3600*1000); //计算天数后剩余的毫秒数
      let hours=Math.floor(leave1/(3600*1000)); //计算出小时数
      //分钟
      let leave2=leave1%(3600*1000); //计算小时数后剩余的毫秒数
      let minutes=Math.floor(leave2/(60*1000)); //计算相差分钟数
      //秒
      let leave3=leave2%(60*1000); //计算分钟数后剩余的毫秒数
      let seconds=Math.round(leave3/1000);

      let ret = '';
      console.log("距离过期还有"+dayDiff+"天"+hours+"小时"+minutes+"分钟"+seconds+"秒");
      if (dayDiff > 0) {
        ret = dayDiff+'天';
      }else if (hours > 0) {
        ret = hours+'小时';
      }else if (minutes > 0) {
        ret = minutes+'分钟';
      }else if (seconds > 0) {
        ret = seconds+'秒';
      }else {
        ret = '过期'+(dayDiff*(-1)-1)+'天';
      }
      return ret;
    },
    //信息填写完整，才可以“保存结果”
    //永久显示绿色，暂时显示橙色，马上要删除显示红色
    expireBackground() {
      let str = this.expireTimeShow;
      let regOrange = RegExp('天');
      let regGray = RegExp('过');
      if (regGray.test(str)) {
        return { background: '#808080' };
      }else if (regOrange.test(str)) {
        return { background: '#ff9854' };
      }else {
        return { background: '#7ae588' };
      }
    },
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
  font-size: 14px;
  color: #9195a3;
}

.history-index {
  width: .1%;
  font-size: 16px;
  padding-left: 7px;
}

#history-index-inner {
  width: 40px;
  height: 40px;
  background: #3ae6cc;
  color: ghostwhite;
  font-weight: bold;
  border-radius: 8%;
  margin: 0 auto;
  display:flex;
  justify-content: center;
  align-items: center;
}

.history-content {
  width: 8.5%;
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

#expired-time {
  font-weight: 500;
  font-size: 14px;
  color: #fff;
  width: 56px;
  padding: 6px 12px;
  border-radius: 10px;
  margin: 0 auto;
}

.el-button {
  padding: 8px 20px;
}

.el-button--primary.is-plain {
    color: #3ae6cc;
    background: #effffd;
    border-color: #3ae6cc;
}

.el-button--primary {
    color: #3ae6cc;
    background-color: #effffd;
    border-color: #3ae6cc;
}

.el-button--primary.is-plain:focus, .el-button--primary.is-plain:hover {
    background: #3ae6cc;
    border-color: #3ae6cc;
    color: #fff;
}

.el-button.is-plain:focus, .el-button.is-plain:hover {
    background: #3ae6cc;
    border-color: #3ae6cc;
    color: #fff;
}
</style>
