<template>
    <div id="imgPart">
        <div id="img_addInfoContainer">
            <el-form :model="infoForm" :rules="rules" ref="infoForm" label-width="80px" size="mini">
                <el-form-item label="上传图片" prop="uploadImg">
                    <el-image style="width: 80px; height: 80px" :src="infoForm.url" :preview-src-list="infoForm.srcList"
                        :fit="contain">
                    </el-image>
                </el-form-item>
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

</template>

<script>

export default {
    name: 'HistoryImageInfo',
    props: ['GID'],
    data() {
        return {
            infoForm: {
                url: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
                srcList: [
                    "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
                    "https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg",
                    'https://fuss10.elemecdn.com/3/28/bbf893f792f03a54408b3b7a7ebf0jpeg.jpeg',
                ],
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
        };
    },
    methods: {
        submitForm(formName) {
            let config = {
                headers: { 'Content-Type': 'multipart/form-data' }
            };


            let tmp = this.infoForm.preDiagnosis
            let preDiagnosis = ''
            tmp.forEach(elem => {
                preDiagnosis = preDiagnosis + elem + '|'
            })
            tmp = this.infoForm.pathologic
            let pathologic = ''
            tmp.forEach(elem => {
                pathologic = pathologic + elem + '|'
            })
            console.log(pathologic, preDiagnosis)

            let uploadForm = new FormData();
            uploadForm.append("sampleName", this.infoForm.sampleName)
            uploadForm.append("partName", this.infoForm.partName)
            uploadForm.append("preDiagnosis", preDiagnosis)
            uploadForm.append("pathologic", pathologic)
            //uploadForm.append("cuttingEdge", this.infoForm.cuttingEdge)
            // console.log(uploadForm)
            // console.log(this.infoForm)

            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.$axios.post('HistoryDetail', uploadForm, config).then((response) => {
                        if (response.data === 2) {
                            this.$message({
                                message: '登录状态错误！请重新登录。',
                                type: 'error'
                            });
                        }
                        else if (response.data === 1) {
                            this.$message({
                                message: '未找到对应图片信息',
                                type: 'warning'
                            });
                        }
                        else {
                            alert('submit!');
                            console.log(response.data)
                        }
                    });
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        }
    },
    mounted() {
        //console.log('this',this.GID)
        this.$axios.get('HistoryDetail', {
            params: {
                GID: this.GID
            }
        }).then((response) => {
            if (response.data === 2) {
                this.$message({
                    message: '登录状态错误！请重新登录。',
                    type: 'error'
                });
            }
            else if (response.data === 1) {
                this.$message({
                    message: '未发现对应图片信息',
                    type: 'warning'
                });
            }
            else {
                this.infoForm.sampleName = response.data.sampleName;
                this.infoForm.partName = response.data.partName;
                this.infoForm.preDiagnosis = response.data.preDiagnosis.split('|');
                this.infoForm.pathologic = response.data.pathologic.split('|');
                this.infoForm.cuttingEdge = response.data.cuttingEdge - '1';
                this.infoForm.differentiation = response.data.differentiation.split('|');
                this.infoForm.remark = response.data.remark;
            }
        })
    },
}
</script>
<style scoped>
#img_addInfoContainer {
    display: flex;
    flex-direction: row;
    margin-top: 5px;
    width: 100%;
    height: 638px;
    justify-content: center;
    align-items: center;
}

.el-tag+.el-tag {
    margin-left: 10px;
}

.button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
}

.input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
}

/* #imgShowContainer {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 95px;
    justify-content: center;
    align-items: center;
} */
</style>