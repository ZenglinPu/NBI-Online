<template>
  <div id="singleImage_adjust-container">
    <div class="controlPanelPart" v-show="consoleMode===0">
        <div style="height: 100%;width: 18%;font-size: small;font-family: 幼圆,serif;">
            <div id="openFunctionContainer">
                <p style="padding-left: 3%;padding-right: 5px;">开启图片调整功能</p>
                <input type="checkbox" ref="isAdjustImage">
            </div>
        </div>
        <div id="moreFunctionControlRange">
            <div class="adjustContainer">
                <div style="width: 20%;display: flex;justify-content: center;align-items: center;">
                    <p style="font-family: 幼圆,serif ">&emsp;&emsp;对比度</p>
                    <el-popover
                      placement="top-start"
                      width="100"
                      title="对比度"
                      trigger="hover"
                      content="拉大高低亮度像素的距离，提高图片明暗对比程度。">
                      <el-button style="margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                    </el-popover>
                </div>
                <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
                    <div style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
                        <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低对比度</p>
                        <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高对比度</p>
                    </div>
                    <div style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
                        <input @change="showInfo()" type="range" id="contrastAdjustRange" min="0" max="200" v-model="contrastOffset">
                        <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;overflow: hidden;">{{contrastOffset}}</p>
                        <el-button icon="el-icon-refresh-right" circle @click="contrastOffset=100"></el-button>
                    </div>
                </div>
            </div>
            <div class="adjustContainer">
                <div style="width: 20%; height: 100%;display: flex;justify-content: center;align-items: center;">
                    <p style="font-family: 幼圆,serif">&emsp;&emsp;&emsp;明度</p>
                    <el-popover
                      placement="top-start"
                      width="100"
                      title="明度"
                      trigger="hover"
                      content="按SVD分解像素，高明度提高图片整体暗部。">
                      <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                    </el-popover>
                </div>
                <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
                    <div style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
                        <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低明度</p>
                        <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高明度</p>
                    </div>
                    <div style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
                        <input @change="showInfo()" type="range" id="numinosityAdjustRange" min="0" max="100" v-model="luminosityOffset">
                        <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;overflow: hidden;">{{luminosityOffset}}</p>
                        <el-button icon="el-icon-refresh-right" circle @click="luminosityOffset=100"></el-button>
                    </div>
                </div>
            </div>
            <div class="adjustContainer">
                <div style="width: 20%; height: 100%;display: flex;justify-content: center;align-items: center;">
                    <p style="font-family: 幼圆,serif">&emsp;&emsp;饱和度</p>
                    <el-popover
                      placement="top-start"
                      width="100"
                      title="饱和度"
                      trigger="hover"
                      content="按SVD分解像素，高饱和度色彩更加鲜艳。">
                      <el-button style="cursor: help;margin-left: 20px;margin-right: 10px;" size="small" slot="reference" icon="el-icon-link" circle></el-button>
                    </el-popover>
                </div>
                <div style="width:75%; height: 100%;display: flex;flex-direction: column;justify-content: center;">
                    <div style="font-family: 幼圆,serif;font-size: small;width:80%; height: 30%;display: flex;flex-direction: row;justify-content: center;align-items: center">
                        <p style="width: 50%;display: flex;justify-content: left;color: rgb(0, 0, 0);">低饱和度</p>
                        <p style="width: 50%;display: flex;justify-content: right;color: rgb(0, 0, 0);">高饱和度</p>
                    </div>
                    <div style="width:100%; height: 40%;display: flex;flex-direction: row;justify-content: center;align-items: center">
                        <input @change="showInfo()" type="range" id="saturationAdjustRange" min="0" max="200" v-model="saturationOffset">
                        <p style="font-family: STHeiti,serif;margin-left: 12px; color: #264b5d; width: 50px;height: 100%;overflow: hidden;" id="saturationOffsetValue">{{saturationOffset}}</p>
                        <el-button icon="el-icon-refresh-right" circle @click="saturationOffset=100"></el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="controlPanelPart" v-show="consoleMode===1">
      <div class="progress-bar-container">
        <article>
          <!-- <input type="radio" name="switch-pos" id="pos-0" checked>
          <input type="radio" name="switch-pos" id="pos-1">
          <input type="radio" name="switch-pos" id="pos-2">
          <input type="radio" name="switch-pos" id="pos-3"> -->
          <div class="chart">
              <div class="bar bar-30 white">
                  <div class="face top">
                      <div class="growing-bar" ref="GB1"></div>
                  </div>
                  <div class="face side-0">
                      <div class="growing-bar" ref="GB2"></div>
                  </div>
                  <div class="face floor">
                      <div class="growing-bar" ref="GB3"></div>
                  </div>
                  <div class="face side-a"></div>
                  <div class="face side-b"></div>
                  <div class="face side-1">
                      <div class="growing-bar" ref="GB4"></div>
                  </div>
              </div>
          </div>
          <!-- <nav class="actions">
              <label for="pos-0">1/4</label>
              <label for="pos-1">2/4</label>
              <label for="pos-2">3/4</label>
              <label for="pos-3">Full</label>
          </nav> -->
        </article>
      </div> 
      <div class="progress-status-container">
        <div class="progress-status-inner">
            <el-steps direction="vertical" :active="active" process-status="finish" finish-status="success">
                <el-step ref="el_step_channel" :title="this.showChannelOffset" icon="el-icon-setting"></el-step>
                <el-step title="生成图片" icon="el-icon-picture-outline-round"></el-step>
                <el-step title="自动调优" icon="el-icon-magic-stick"></el-step>
                <el-step ref="el_step_brightness" :title="this.showBrightnessOffset" icon="el-icon-setting"></el-step>
                <el-step title="更新数据" icon="el-icon-document-copy"></el-step>
            </el-steps>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "singleImageProcess_imageAdjust",
  data(){
    return {
      contrastOffset: 100,
      luminosityOffset: 100,
      saturationOffset: 100,
      consoleMode: 0,
      brightnessOffset: 0,
      channelOffset: 0,
      active: -1,
      progress: 0,
      progressNormalTopWave: "repeating-linear-gradient(120deg,transparent,rgba(64, 158, 255, .4) 46px,rgba(64, 158, 255, .4) 46px,transparent 92px)",
      progressSuccessTopWave: "repeating-linear-gradient(120deg,transparent,rgba(0, 190, 255, .5) 46px,rgba(0, 190, 255, .5) 46px,transparent 92px)",
    }
  },
  computed:{
    showChannelOffset(){
        return '调整通道：偏移为'+this.channelOffset
    },
    showBrightnessOffset(){
        return '调整亮度：偏移为'+this.brightnessOffset
    }
  },
  mounted() {
    this.$bus.$on("sendAdjustImageInfo",()=>{
      const toSend = {
        "isOpen": this.$refs.isAdjustImage.checked,
        "contrastOffset": this.contrastOffset,
        "luminosityOffset": this.luminosityOffset,
        "saturationOffset": this.saturationOffset,
      };
      //发送数据到send
      this.$bus.$emit("getAdjustImageInfo", toSend);
    })
    this.$bus.$on("changeConsoleMode",(data)=>{
      this.consoleMode = data;
    })
    this.$bus.$on("brightnessNumber",(data)=>{
      this.brightnessOffset = data;
    //   this.$refs.el_step_brightness.title = this.showBrightnessOffset
    //   console.log(data)
    })
    this.$bus.$on("channelNumber",(data)=>{
      this.channelOffset = data;
    //   this.$refs.el_step_channel.title = this.showChannelOffset
    })
    this.$bus.$on("showAutoProgress",(data)=>{
        console.log(this.progress);
        console.log(data);
      if(data.status !== 4 && data.status !== 5 && data.status !== 6) {
        this.active = data.status-1;
        if (data.progress > 0) {
            this.progress += Number(data.progress);
            console.log(this.progress);
        }
        if (this.progress > 98) {
            this.progress = 98
        }
        this.$refs.GB1.style.width=this.$refs.GB2.style.width=this.$refs.GB3.style.width=this.$refs.GB4.style.width=String(this.progress)+"%";
      }
      else if(data.status === 4){
        this.active = 5;
        this.progress = 100;
        this.$refs.GB1.style.width=this.$refs.GB2.style.width=this.$refs.GB3.style.width=this.$refs.GB4.style.width="100%";
        this.$refs.GB1.style.backgroundColor=this.$refs.GB2.style.backgroundColor=this.$refs.GB3.style.backgroundColor=this.$refs.GB4.style.backgroundColor="rgba(0, 190, 255, .6)";
        this.$refs.GB1.style.backgroundImage=this.progressSuccessTopWave;
      }
      else if(data.status === 5){
        this.active = -1;
        this.progress = 0;
        this.$refs.GB1.style.width=this.$refs.GB2.style.width=this.$refs.GB3.style.width=this.$refs.GB4.style.width="0%";
        this.$refs.GB1.style.backgroundColor=this.$refs.GB2.style.backgroundColor=this.$refs.GB3.style.backgroundColor=this.$refs.GB4.style.backgroundColor="rgba(64, 158, 255, .6)";
        this.$refs.GB1.style.backgroundImage=this.progressNormalTopWave;
      }
      else {
        this.$refs.GB1.style.backgroundColor=this.$refs.GB2.style.backgroundColor=this.$refs.GB3.style.backgroundColor=this.$refs.GB4.style.backgroundColor="rgba(255, 49, 49, .6)";
      }
    })
  },
  beforeDestroy() {
    this.$bus.$off("sendAdjustImageInfo");
    this.$bus.$off("changeConsoleMode");
    this.$bus.$off("brightnessNumber");
    this.$bus.$off("channelNumber");
    this.$bus.$off("showAutoProgress");
  },
  methods:{
    showInfo(){
      if (!this.$refs.isAdjustImage.checked){
        this.$message({
          showClose: true,
          message: '仅有在勾选开启图片调整功能后该改动才能生效。',
          type: 'warning'
        });
      }
    },
  }
}
</script>

<style scoped>
#singleImage_adjust-container{
  width: 100%;
  height: 100%;
}
input[type="checkbox"] {
  height: 18px;
  width: 18px;
  border: 2px rgb(0, 94, 255);
  cursor: pointer;
}
#moreFunctionControlRange{
    width: 85%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: start;
}

#contrastAdjustRange{
    background-color: rgb(0, 0, 66);
    border-radius: 10px;
    width: 100%;
    -webkit-appearance: none;
    height:4px;
    margin-top: 20px;
}

#numinosityAdjustRange{
    background-color: rgb(0, 0, 66);
    border-radius: 10px;
    width: 100%;
    -webkit-appearance: none;
    height:4px;
    margin-top: 20px;
}

#saturationAdjustRange{
    background-color: rgb(0, 0, 66);
    border-radius: 10px;
    width: 100%;
    -webkit-appearance: none;
    height:4px;
    margin-top: 20px;
}
#openFunctionContainer{
    width: 100%;
    height: 100%;
    display: flex;
    border-right: 1px gray solid;
    justify-content: center;
    align-items: center;
    font-family: Arial, Helvetica, sans-serif;
}
.controlPanelPart{
    width: 100%;
    height: 100%;
    padding-top: 5px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: row;
}
.adjustContainer{
  width: 100%;
  height: 60px;
  display: flex;
  flex-direction: row;
  border-top: #bdbdbd 1px solid;
  border-bottom: #bdbdbd 1px solid;
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
}

.progress-bar-container h1
{
    font-size: 2.5em;
    margin: 2em 0 .5em;
}
.progress-bar-container h2
{
    margin-bottom: 3em;
}
.progress-bar-container em,.progress-bar-container strong
{
    font-weight: 700;
}
.progress-bar-container input
{
    display: none;
}
.progress-bar-container article 
{
    align-self: center;
    width: 20em;
    margin-bottom: 2em;
}
.progress-bar-container article p,
.progress-bar-container article:last-of-type
{
    margin-bottom: 0;
}
.progress-bar-container
{
    width: 646px;
    height: 100%;
    z-index: 1;
    display: flex;
    overflow: hidden;
    flex-direction: column;
    /* justify-content: center; */
    border-right: 1px solid #DCDFE6;
    background: linear-gradient(180deg,rgba(245,245,252,0.5),#f5f5fc 45%);
    /* background: linear-gradient(180deg,rgba(255,255,255,0),#3e3ed2 5%); */
}
.progress-bar-container .chart
{
    font-size: 1em;

    perspective: 1000px;
    perspective-origin: 50% 50%;
    backface-visibility: visible;
}
.progress-bar-container .bar
{
    font-size: 1em;
    position: relative;
    height: 10em;
    transition: all .1s ease-in-out;
    transform: rotateX(60deg) rotateY(0deg);
    transform-style: preserve-3d;
}
.progress-bar-container .bar .face
{
    font-size: 2em;
    position: relative;
    width: 100%;
    height: 2em;
    background-color: rgba(254,254,254,.3);
}
.progress-bar-container .bar .face.side-a,
.progress-bar-container .bar .face.side-b
{
    width: 2em;
}
.progress-bar-container .bar .side-a
{
    transform: rotateX(90deg) rotateY(-90deg) translateX(2em) translateY(1em) translateZ(1em);
}
.progress-bar-container .bar .side-b
{
    transform: rotateX(90deg) rotateY(-90deg) translateX(4em) translateY(1em) translateZ(-1em);
    position: absolute;
    right: 0;
}
.progress-bar-container .bar .side-0
{
    transform: rotateX(90deg) rotateY(0) translateX(0) translateY(1em) translateZ(-1em);
}
.progress-bar-container .bar .side-1
{
    transform: rotateX(90deg) rotateY(0) translateX(0) translateY(1em) translateZ(3em);
}
.progress-bar-container .bar .top
{
    transform: rotateX(0deg) rotateY(0) translateX(0em) translateY(4em) translateZ(2em);
}
.progress-bar-container .bar .floor
{
    box-shadow: 0 .1em 0.6em rgba(0,0,0,.2), .6em -0.5em 3em rgba(0,0,0,.3), 1em -1em 8em #fefefe;
}

.progress-bar-container .growing-bar
{
    transition: all .1s ease-in-out;
    width: 100%;
    height: 2em;
}

.bar.white .side-a
{
    background-color: rgba(64, 158, 255, .6);
}
.bar.white .growing-bar
{
    background-color: rgba(64, 158, 255, .6);
    /* rgba(0, 190, 255, .6) */
    /* rgba(255, 49, 49, .6) */
}
.bar.white .top .growing-bar {
    background-image: repeating-linear-gradient(
      120deg,
      transparent,
      rgba(64, 158, 255, .4) 46px,
      rgba(64, 158, 255, .4) 46px,
      transparent 92px
    );
    background-size: 320px 64px;
    animation: slide 6s linear infinite;
}
@keyframes slide {
  from {
    background-position-x: 0;
  }
  to {
    background-position-x: 320px;
  }
}
.bar.white .side-0 .growing-bar
{
    box-shadow: -0.5em -1.5em 4em #409eff;
}
.bar.white .floor .growing-bar
{
    box-shadow: 0em 0em 2em #409eff;
}

/* @mixin drawSkin($color, $name)
{
    .bar.#{$name}
    {
        .side-a,
        // &.bar-100 .side-b,
        .growing-bar
        {
            background-color: rgba($color, .6);
        }
        .side-0 .growing-bar
        {
            box-shadow: -0.5em -1.5em 4em $color;
        }
        .floor .growing-bar
        {
            box-shadow: 0em 0em 2em $color;
        }
    }
} */

.chart .bar.white .face
{
    /* background-color: rgba(254, 254, 254, .2); */
}

/* @mixin drawFaces($color, $name)
{
    .chart .bar.#{$name} .face
    {
        background-color: rgba($color, .2);
    }
} */

.bar-30 .growing-bar
{
    width: 0%;
}

.progress-bar-container .chart.grid
{
    display: flex;
    flex-direction: row;
}
.progress-bar-container .chart.grid .exercise 
{
    flex: 0 0 100%;
    display: flex;
}
.progress-bar-container .chart.grid .exercise .bar
{
    flex: 1;
    margin: 0 .5em;
}
.progress-bar-container .chart.grid .exercise .bar:nth-child(2)
{
    z-index: 8;
    flex: 1 0 40%;
}
.progress-bar-container .chart.grid .exercise .bar:first-child
{
    z-index: 10;
    margin-left: 0;
}
.progress-bar-container .chart.grid .exercise .bar:last-child
{
    margin-right: 0;
}

.progress-bar-container .actions
{
    display: flex;
    justify-content: center;
    margin-bottom: 0;
    padding-bottom: 2em;
    border-bottom: 1px dotted rgba(68, 68, 68, .4);
}
/* .progress-bar-container label
{
    box-sizing: border-box;
    padding: 1em;
    margin: 0 .2em;
    cursor: pointer;
    transition: all .15s ease-in-out;
    color: #0a4069;
    border: 1px solid rgba(254, 254, 254, .6);
    border-radius: 0;

    flex: 1;
}
.progress-bar-container label:first-child {
    margin-left: 0;
    border-radius: .2em 0 0 .2em;
}
.progress-bar-container label:last-child {
    margin-right: 0;
    border-radius: 0 .2em .2em 0;
}

input[id='pos-0']:checked ~ .actions label[for='pos-0'],
input[id='pos-1']:checked ~ .actions label[for='pos-1'],
input[id='pos-2']:checked ~ .actions label[for='pos-2'],
input[id='pos-3']:checked ~ .actions label[for='pos-3']
{
    color: #76c900;
    border: 1px solid darken(#0a4069, 15);
    background-color: #0a4069;
}
input[id='pos-0']:checked ~ .chart .growing-bar
{
    width: 25%;
}
input[id='pos-1']:checked ~ .chart .growing-bar
{
    width: 50%;
}
input[id='pos-2']:checked ~ .chart .growing-bar
{
    width: 75%;
}
input[id='pos-3']:checked ~ .chart .growing-bar
{
    width: 100%;
} */

.progress-status-container {
    flex-grow: 1; 
    height: 100%;
    z-index: 1;
    display: flex;
    overflow: hidden;
    flex-direction: column;
    justify-content: center;
    /* background: linear-gradient(180deg,rgba(255,255,255,0),#f5f5fc 5%); */
}
.progress-status-inner {
    width: 100%;
    height: 100%;
    padding: 10px 20px;
}
.el-step >>> .el-step__title {
    font-size: 13px;
}
.el-step >>> .el-step__head {
    margin-right: 6px;
=======
>>>>>>> parent of aea515e2 (🐞 fix(Front): 统一全局CSS样式，与修复gitignore)
=======
>>>>>>> parent of aea515e2 (🐞 fix(Front): 统一全局CSS样式，与修复gitignore)
=======
>>>>>>> parent of aea515e2 (🐞 fix(Front): 统一全局CSS样式，与修复gitignore)
=======
>>>>>>> parent of aea515e2 (🐞 fix(Front): 统一全局CSS样式，与修复gitignore)
}
</style>
