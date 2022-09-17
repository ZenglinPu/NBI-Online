<template>
  <el-form id="infoFormContainer" :model="infoForm" :rules="rules" ref="infoForm" label-width="100px" size="mini">
    <el-form-item label="标本名称" prop="sampleName">
      <el-input v-model="infoForm.sampleName"></el-input>
    </el-form-item>
    <el-form-item label="标本部位" prop="partName">
      <el-select v-model="infoForm.partName" placeholder="请选择标本部位">
        <el-option label="胃" value="胃"></el-option>
        <el-option label="大肠" value="大肠"></el-option>
        <el-option label="小肠" value="小肠"></el-option>
        <el-option label="食管" value="食管"></el-option>
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
    <el-form-item label="浸润深度" prop="infiltration">
      <el-input style="width: 320px" placeholder="仅粘膜下层需文本录入" :disabled="submucosaSelected"
                v-model="infoForm.submucosaDepth"
                class="input-with-select">
        <el-select style="width: 108px" id="infiltrationSelector" v-model="infoForm.infiltration" slot="prepend"
                   placeholder="请选择">
          <el-option label="粘膜上皮层" value="粘膜上皮层"></el-option>
          <el-option label="粘膜固有层" value="粘膜固有层"></el-option>
          <el-option label="粘膜肌层" value="粘膜肌层"></el-option>
          <el-option label="粘膜下层" value="粘膜下层"></el-option>
        </el-select>
        <template slot="append">μm</template>
      </el-input>
    </el-form-item>
    <el-form-item label="分化程度" prop="differentiation">
      <el-checkbox-group v-model="infoForm.differentiation">
        <el-checkbox label="高分化" name="differentiation"></el-checkbox>
        <el-checkbox label="中分化" name="differentiation"></el-checkbox>
        <el-checkbox label="低分化" name="differentiation"></el-checkbox>
        <el-checkbox label="不适用" name="differentiation"></el-checkbox>
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
      <el-button type="primary" @click="submitForm('infoForm')">提交修改</el-button>
      <!-- <el-button @click="resetForm('infoForm')">重置</el-button> -->
    </el-form-item>
  </el-form>
</template>

<script>

export default {
  name: 'HistoryImageInfo',
  props: ['GID'],
  data() {
    return {
      infoForm: {
        sampleName: '',
        partName: '',//部位 胃、大肠小肠、食管
        preDiagnosis: [],//术前诊断
        pathologic: [],//病理诊断
        differentiation: [],///分化程度Integer分化程度多选：‘0’：不适用 ‘1‘：低分化 ‘2’：中分化 ‘3‘：高分化 多选
        infiltration: '',//（单选，粘膜上皮层，粘膜固有层，粘膜肌层，粘膜下层（文本录入，单位μm），固有肌层）
        submucosaDepth: '',//粘膜下层深度
        cuttingEdge: true,//水平切缘（单选，阴性，阳性
        remark: '',//备注
      },
      preDiagnosisOptions: [{
        value: '腺癌', label: '腺癌'
      }, {
        value: '鳞癌', label: '鳞癌'
      }, {
        value: 'HGIN', label: 'HGIN'
      }, {
        value: 'LGIN', label: 'LGIN'
      }, {
        value: '腺瘤', label: '腺瘤'
      }, {
        value: '锯齿状病变', label: '锯齿状病变'
      }, {
        value: '错构瘤', label: '错构瘤'
      }, {
        value: '神经内分泌肿瘤', label: '神经内分泌肿瘤'
      }, {
        value: '间质瘤', label: '间质瘤'
      }
      ],
      pathologicOptions: [{
        value: '腺癌', label: '腺癌'
      }, {
        value: '鳞癌', label: '鳞癌'
      }, {
        value: 'HGIN', label: 'HGIN'
      }, {
        value: 'LGIN', label: 'LGIN'
      }, {
        value: '腺瘤', label: '腺瘤'
      }, {
        value: '锯齿状病变', label: '锯齿状病变'
      }, {
        value: '错构瘤', label: '错构瘤'
      }, {
        value: '神经内分泌肿瘤', label: '神经内分泌肿瘤'
      }, {
        value: '间质瘤', label: '间质瘤'
      }
      ],
      rules: {
        sampleName: [
          {required: true, message: '请输入标本名称', trigger: 'blur'},
          {min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur'}
        ],
        partName: [
          {required: true, message: '请选择标本部位', trigger: 'change'}
        ],
        preDiagnosis: [
          {type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change'}
        ],
        pathologic: [
          {type: 'array', required: true, message: '请至少选择一个诊断', trigger: 'change'}
        ],
        differentiation: [
          {type: 'array', required: true, message: '请至少选择一个分化程度', trigger: 'change'}
        ],
      }
    };
  },
  computed: {
    submucosaSelected() {
      return this.infoForm.infiltration !== "粘膜下层"
    }
  },
  methods: {
    getCookie(objName) {//获取指定名称的cookie的值
      const arrStr = document.cookie.split("; ");
      for (let i = 0; i < arrStr.length; i++) {
        const temp = arrStr[i].split("=");
        if (temp[0] === objName) return temp[1];
      }
      return null;
    },
    getToken() {
      return this.getCookie("NBI_token");
    },
    getUID() {
      return this.getCookie("NBI_UID");
    },
    submitForm(formName) {

      this.$refs[formName].validate((valid) => {
        if (valid) {
          let config = {
            headers: {'Content-Type': 'multipart/form-data'}
          };

          //处理诊断的表单
          let tmp = this.infoForm.preDiagnosis
          let preDiagnosis =''
          tmp.forEach(elem => {
            preDiagnosis = preDiagnosis + elem + ','
          })
          preDiagnosis=preDiagnosis.slice(0,-1)

          tmp = this.infoForm.pathologic
          let pathologic=''
          tmp.forEach(elem => {
            pathologic = pathologic + elem + ','
          })
          pathologic=pathologic.slice(0,-1)
          tmp = this.infoForm.differentiation
          let differentiation=''
          tmp.forEach(elem => {
            differentiation = differentiation + elem + ','
          })
          differentiation=differentiation.slice(0,-1)
          //处理分化程度的表单
          let infiltration = this.infoForm.infiltration
          if (this.infoForm.infiltration === "粘膜下层") {
            infiltration = this.infoForm.infiltration + this.infoForm.submucosaDepth;
          }

          let uploadForm = new FormData();
          uploadForm.append("sampleName", this.infoForm.sampleName)
          uploadForm.append("partName", this.infoForm.partName)
          uploadForm.append("preDiagnosis", preDiagnosis)
          uploadForm.append("pathologic", pathologic)
          uploadForm.append("cuttingEdge", this.infoForm.cuttingEdge)
          uploadForm.append("infiltration", infiltration)
          uploadForm.append("differentiation", differentiation)
          uploadForm.append("remark", this.infoForm.remark)
          // 身份识别数据
          uploadForm.append("uid", this.getUID());
          uploadForm.append("token", this.getToken());
          // 图片_id
          uploadForm.append("_id", this.GID);
          this.$axios.post('HistoryDetail/modifyInfo/', uploadForm, config).then((response) => {
            if (response.data === 1) {
              this.$message({
                message: '登录状态错误！请重新登录。',
                type: 'error'
              });
            } else if (response.data === 2) {
              this.$message({
                message: '未找到对应图片信息',
                type: 'warning'
              });
            } else {
              alert('submit!');
              // console.log(response.data)
            }
          });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },

  },
  mounted() {
    let getItemInfoForm = new FormData();
    // 身份识别数据
    getItemInfoForm.append("uid", this.getUID());
    getItemInfoForm.append("token", this.getToken());
    // 图片_id
    getItemInfoForm.append("gid", this.GID);

    this.$axios.post("/NBI/HistoryDetail/", getItemInfoForm, {
      headers: {'Content-Type': 'multipart/form-data'}
    }).then((response) => {
      if (response.data === 2) {
        this.$message({
          message: '登录状态错误！请重新登录。',
          type: 'error'
        });
      } else if (response.data === 1) {
        this.$message({
          message: '未发现对应图片信息',
          type: 'warning'
        });
      } else {
        // console.log("图片详情后端", response.data)
        this.infoForm.sampleName = response.data.sampleName;
        this.infoForm.partName = response.data.part;
        let preDiagnosis = response.data.preDiagnosis;
        let pathologic = response.data.pathologic;
        let differentiation = response.data.differentiation;
        if (preDiagnosis) {
          preDiagnosis = preDiagnosis.split(',');
          this.infoForm.preDiagnosis = preDiagnosis;
        }
        if (pathologic) {
          pathologic = pathologic.split(',');
          this.infoForm.pathologic = pathologic;
        }
        if (differentiation) {
          differentiation = differentiation.split(',');
          this.infoForm.differentiation = differentiation;
        }
        this.infoForm.cuttingEdge = response.data.cuttingEdge === "true";
        this.infoForm.remark = response.data.remark;

        let tmp =response.data.infiltration
        if(tmp.slice(0,4)==="粘膜下层"){
          this.infoForm.submucosaDepth=tmp.slice(4)
          this.infoForm.infiltration="粘膜下层"
        }else{
          this.infoForm.infiltration=response.data.infiltration
        }
        // console.log("修改后infoForm", this.infoForm);
      }
    })
  },
  updated() {
    if (this.infoForm.infiltration !== "粘膜下层") {
      this.infoForm.submucosaDepth = ''
    }
  }
}
</script>
<style scoped>


.el-tag + .el-tag {
  margin-left: 10px;
}

#infoFormContainer {
  padding-right: 20px;
  padding-right: 5px;
  padding-down: 5px;
}

/*#infiltrationSelector{*/
/*  width: 50px;*/
/*}*/

.el-form >>> .el-form-item--mini.el-form-item {
  margin-bottom: 22px;
}
</style>