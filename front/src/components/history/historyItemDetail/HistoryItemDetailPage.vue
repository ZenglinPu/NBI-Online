<template>
    <div id="historyItemDetailContainer">
      <div id="detailTitleContainer">
        <div @click="backToHistory()" class="backBtn">
          <i class="el-icon-back"></i>
          <p>返回</p>
        </div>
        <div style="height: 100%;width: 30%;font-family: 幼圆,serif;font-size: large;font-weight: bolder;display: flex;justify-content: start;align-items: center;color: #2a2a2a">
          <p>&emsp;&emsp;标本名称:&emsp;{{titleInfo.sampleName}}</p>
        </div>
        <div style="height: 100%;width: 20%;font-family: 幼圆,serif;font-size: small;font-weight: lighter;display: flex;flex-direction: column;justify-content: start;align-items: end;color: #00002c">
          <div style="width:100%;height:50%;text-align: left;">
            <p>&emsp;&emsp;上传时间:&emsp;{{titleInfo.uploadTime}}</p>
          </div>
          <div style="width:100%;height:50%;text-align: left;">
            <p>&emsp;&emsp;过期时间:&emsp;{{titleInfo.expiresTime}}</p>
          </div>
        </div>
        <div style="height: 100%;width: 40%;display: flex;justify-content: end;align-items: center;">
          <el-button style="width: 30%;height: 45%;display: flex;justify-content: center;align-items: center" type="warning" icon="el-icon-download" @click="downloadResult()">下 载 结 果</el-button>
          <el-button style="width: 30%;height: 45%;display: flex;justify-content: center;align-items: center" type="danger" icon="el-icon-delete" @click="deleteDetail()">删 除</el-button>
        </div>
      </div>
      <div id="detailInfoContainer">
        <div id="imageShowPart">
          <div style="height: 74%;width: 100%;display: flex;justify-content: center;align-items: center;border: 1px solid darkblue; background-color: #6a6f77">
            <el-image class="bigNBIImage" v-show="imageShowInfo.NBIImageName!=='None'" :src="imageShowInfo.NBIImageName" :preview-src-list="imageShowInfo.srcList"></el-image>
          </div>
          <div style="height: 25%;margin-top: 1%;width: 100%;display: flex;justify-content: space-between;align-items: center;">
            <div style="height: 96%;width: 32%;display: flex;justify-content: center;align-items: center;border: 1px solid darkblue; background-color: #6a6f77">
              <el-image class="bigNBIImage" v-show="imageShowInfo.src_blue!=='None'" :src="imageShowInfo.src_blue"></el-image>
            </div>
            <div style="height: 96%;width: 32%;display: flex;justify-content: center;align-items: center;border: 1px solid darkblue; background-color: #6a6f77">
              <el-image class="bigNBIImage" v-show="imageShowInfo.src_green!=='None'" :src="imageShowInfo.src_green"></el-image>
            </div>
            <div style="height: 96%;width: 32%;display: flex;justify-content: center;align-items: center;border: 1px solid darkblue; background-color: #6a6f77">
              <p v-show="imageShowInfo.src_white==='/static/Data/White/null'" style="color: whitesmoke">未上传白色图片</p>
              <el-image class="bigNBIImage" v-show="imageShowInfo.src_white!=='/static/Data/White/null'" :src="imageShowInfo.src_white"></el-image>
            </div>
          </div>
        </div>
        <div id="imageAdjustPart">
          <div id="img_addInfoContainer">
            <el-form :model="infoForm" :rules="rules" ref="infoForm" label-width="80px" size="mini">
                <el-form-item label="标本名称" prop="sampleName">
                    <el-input v-model="infoForm.sampleName"></el-input>
                </el-form-item>
                <el-form-item label="标本部位" prop="partName">
                    <el-select v-model="infoForm.partName" placeholder="请选择标本部位">
                        <el-option label="胃" value="胃"></el-option>
                        <el-option label="大肠" value="大肠"></el-option>
                        <el-option label="小肠" value="小肠"></el-option>
                        <el-option label="食管" value="食管"></el-option>
                        <el-option label="其它" value="其它"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="术前诊断" prop="preDiagnosis">
                    <el-select v-model="infoForm.preDiagnosis" multiple filterable allow-create default-first-option
                        placeholder="请选择术前诊断">
                        <el-option v-for="item in preDiagnosisOptions" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="病理诊断" prop="pathologic">
                    <el-select v-model="infoForm.pathologic" multiple filterable allow-create default-first-option
                        placeholder="请选择诊断">
                        <el-option v-for="item in pathologicOptions" :key="item.value" :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="分化程度" prop="differentiation">
                    <el-checkbox-group v-model="infoForm.differentiation">
                        <el-checkbox label="0" name="differentiation"></el-checkbox>
                        <el-checkbox label="1" name="differentiation"></el-checkbox>
                        <el-checkbox label="2" name="differentiation"></el-checkbox>
                        <el-checkbox label="3" name="differentiation"></el-checkbox>
                        <el-checkbox label="4" name="differentiation"></el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
                <el-form-item label="水平切缘" prop="cuttingEdge">
                    <el-switch v-model="infoForm.cuttingEdge"></el-switch>
                </el-form-item>
                <el-form-item label="备注" prop="remark">
                    <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入备注"
                        v-model="infoForm.remark"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('infoForm')">立即创建</el-button>
                    <!-- <el-button @click="resetForm('infoForm')">重置</el-button> -->
                </el-form-item>
            </el-form>
        </div>
        </div>
      </div>
    </div>
</template>

<script>

export default {
  name: "HistoryItemDetailPage",
  props: ['GID'],
  data(){
    return{
      titleInfo:{
        sampleName: "",
        uploadTime: "",
        expiresTime: "",
      },
      imageShowInfo:{
        NBIImageName: "",
        src_blue: "",
        src_green: "",
        src_white: "",
        srcList:[],
      },
      infoForm: {
        sampleName: '',
        partName: '',//部位 胃、大肠小肠、食管
        preDiagnosis: [],//术前诊断

        pathologic: [],//病理诊断

        differentiation: [],///分化程度Integer分化程度多选：‘0’：不适用 ‘1‘：低分化 ‘2’：中分化 ‘3‘：高分化 多选
        //infiltration: '',（单选，粘膜上皮层，粘膜固有层，粘膜肌层，粘膜下层（文本录入，单位μm），固有肌层）
        cuttingEdge: true,//水平切缘（单选，阴性，阳性
        remark: '备注xxxx',//备注
      },
      preDiagnosisOptions: [{
          value: '早癌', label: '早癌'
      }, {
          value: '炎症', label: '炎症'
      }, {
          value: '腺癌', label: '腺癌'
      },
      {
          value: '胃癌', label: '胃癌'
      }],
      pathologicOptions: [{
          value: '早癌', label: '早癌'
      }, {
          value: '炎症', label: '炎症'
      }, {
          value: '腺癌', label: '腺癌'
      }, {
          value: '胃癌', label: '胃癌'
      }
      ],
      rules: {
          sampleName: [
              { required: true, message: '请输入标本名称', trigger: 'blur' },
              { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
          ],
          partName: [
              { required: true, message: '请选择标本部位', trigger: 'change' }
          ],
          preDiagnosis: [
              { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' }
          ],
          pathologic: [
              { type: 'array', required: true, message: '请至少选择一个诊断', trigger: 'change' }
          ],
          differentiation: [
              { type: 'array', required: true, message: '请至少选择一个分化程度', trigger: 'change' }
          ],
      }
    }
  },
  mounted(){
    this.initDownloadImageInfo();
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
    initDownloadImageInfo(){
       let getItemInfoForm = new FormData();
      // 身份识别数据
      getItemInfoForm.append("uid", this.getUID());
      getItemInfoForm.append("token", this.getToken());
      // 图片_id
      getItemInfoForm.append("gid", this.GID);
      this.$axios.post("/NBI/HistoryDetail/",getItemInfoForm, {
         headers: {'Content-Type': 'multipart/form-data'}
      }).then((response) => {
        if (response.data === 1){
          this.$message({
            showClose: true,
            message: '登录状态错误！请重新登录。',
            type: 'error'
          });
        }
        else{
          // console.log(response.data);
          this.titleInfo.sampleName = response.data.sampleName===""?'未命名':response.data.sampleName;
          this.titleInfo.expiresTime = response.data.expiresTime;
          this.titleInfo.uploadTime = response.data.uploadTime;

          this.imageShowInfo.NBIImageName = "/static/Data/NBI/"+response.data.imageNBIName;
          this.imageShowInfo.srcList.push("/static/Data/NBI/"+response.data.imageNBIName);
          this.imageShowInfo.src_blue = "/static/Data/Blue/"+response.data.imageBlueName;
          this.imageShowInfo.src_green = "/static/Data/Green/"+response.data.imageGreenName;
          this.imageShowInfo.src_white = "/static/Data/White/"+response.data.imageWhiteName;
        }
      });
    },
    backToHistory(){
      window.history.back();
    },
    downloadResult() {
      return undefined;
    },
    deleteDetail() {
      this.$confirm('确认删除？（操作不可逆）')
      .then(() => {
        let deleteImageForm = new FormData();
        // 身份识别数据
        deleteImageForm.append("uid", this.getUID());
        deleteImageForm.append("token", this.getToken());
        //当前页面
        deleteImageForm.append("gid", this.GID);
        this.$axios.post("/NBI/History/deleteImage/", deleteImageForm, {
         headers: {'Content-Type': 'multipart/form-data'}
        }).then((response) => {
          if (response.data === 1){
            this.$message({
              showClose: true,
              message: '登录状态错误！请重新登录。',
              type: 'error'
            });
          }
          else if (response.data === 3){
            this.$message({
              showClose: true,
              message: '删除失败，处理错误！',
              type: 'error'
            });
          }
          else{
            this.$message({
              showClose: true,
              message: '图片已删除',
              type: 'success'
            });
            window.history.back();
            // this.$bus.$emit("reloadHistoryData");
          }
        });
      })
      .catch(() => {
      });
    },
  },
}
</script>

<style scoped>
#historyItemDetailContainer {
  width: 100%;
  height: 100%;
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
#detailTitleContainer{
  width: 100%;
  height: 12%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-items: center;
  border-bottom: 2px solid #777777;
}
#detailInfoContainer{
  width: 96%;
  height: 88%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
#imageShowPart{
  width: 45%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
#imageAdjustPart{
  width: 55%;
  height: 100%;
  border-left: #5d5d5d solid 1px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.bigNBIImage{
  height: 100%;
  object-fit: contain;
}
.backBtn{
  width: 5%;
  display: flex;
  justify-content: end;
  align-items: center;
  color: #2e46ff;
  transition: 0.3s ease;
  cursor: pointer;
}
.backBtn:hover{
  color: #000c73;
}
</style>