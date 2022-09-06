<template>
  <div style="display: flex;align-items: center;flex-direction: column;overflow: auto;width: 100%;height: 100%;">
    <div id="infoPageTitle">
      <i class="el-icon-info" style="color: #0b007e"></i>
      <p style="margin-left: 10px">NBI-Online说明文档</p>
    </div>
    <div class="infoPageSubTitle">
      <i class="el-icon-discover" style="color: #0b007e"></i>
      <p style="margin-left: 10px">用户权限与图片管理相关说明：</p>
    </div>
    <div class="infoPageContentContainer">
      <div id="uploadTimesInfo" class="infoPageContend_subTitle">
        <p>
          - 源图片上传次数
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;用户仅仅在</span>
          <span style="color: red">完成源图片上传后</span>
          <span>才可进行NBI图片的生成以及修改等操作。</span>
          <span style="color: goldenrod">超级用户</span>
          <span>享有</span>
          <span style="color: red">无限制</span>
          <span>的NBI原始图片上传次数，而</span>
          <span style="color: gray">普通用户</span>
          <span>仅仅有</span>
          <span style="color: red">10</span>
          <span>次的图片上传机会。当普通用户再次成为超级用户，则会重新享受无限制的上传次数，假如再次失去超级用户身份，依然会获得10次上传机会。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div id="howToBeSuperUserInfo" class="infoPageContend_subTitle">
        <p>
          - 如何成为超级用户
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;目前，我们仅仅支持两种获得超级用户身份的方式：</span><br>
          <span>（一）新用户在</span>
          <span>注册时</span>
          <span>会获得</span>
          <span style="color: red">三天</span>
          <span>的</span>
          <span style="color: goldenrod">超级用户</span>
          <span>使用权限;</span><br>
          <span>（二）通过</span>
          <span style="color: red">邀请码</span>
          <span>可以获得</span>
          <span style="color: red">三十天</span>
          <span>的</span>
          <span style="color: goldenrod">超级用户</span>
          <span>使用权限，即在邀请到别的</span>
          <span style="color: red">新用户注册成功</span>
          <span>时，对方通过输入</span>
          <span style="color: red">您自己的邀请码</span>
          <span>可以为您自己增加超级用户权限。注意，一个账号仅能赠送</span>
          <span style="color: red">一次</span>
          <span>，但是可以</span>
          <span style="color: red">多次</span>
          <span>接受赠送，我们希望通过这样的方式鼓励更多的人来使用我们的网站。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div id="userTypeInfo" class="infoPageContend_subTitle">
        <p>
          - 超级用户和普通用户的区别
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span style="color: gray">普通用户</span>
          <span>和</span>
          <span style="color: goldenrod">超级用户</span>
          <span>都可以在上传源图片之后生成NBI图片，但是在</span>
          <span style="color: red">结果图片的下载权限、源图片的上传次数</span>
          <span>以及</span>
          <span style="color: red">图片在后台的管理和保留时间</span>
          <span>上有所不同:</span><br>
          <span>（一）</span>
          <span style="color:gray;">普通用户</span>
          <span style="color: red">无法下载</span>
          <span>生成后的NBI高清晰度原图，若直接在网页上下载则只能得到</span>
          <span style="color: red">压缩后的结果图片</span>
          <span>，</span>
          <span style="color: goldenrod">超级用户</span>
          <span>则可以下载</span>
          <span style="color:red;">无压缩的结果图</span>
          <span>;</span><br>
          <span>（二）</span>
          <span style="color: gray">普通用户</span>
          <span>有</span>
          <span style="color: red">10次</span>
          <span>的上传次数限制，而</span>
          <span style="color: goldenrod">超级用户</span>
          <span>则不限制上传;</span><br>
          <span>（三）如果上传图片不生成，则系统默认保留</span>
          <span style="color: red">24小时</span>
          <span>。如果是生成了结果的图片数据，</span>
          <span style="color: gray">普通用户</span>
          <span>仅在后台保留</span>
          <span style="color: red">30天</span>
          <span style="color: goldenrod">高级用户</span>
          <span>则是</span>
          <span style="color: red">1年</span>
          <span>。在后台保存的期间，用户都可以对这些数据进行</span>
          <span style="color: red">搜索</span>
          <span>、</span>
          <span style="color: red">查看</span>
          <span>、</span>
          <span style="color: red">修改</span>
          <span>、</span>
          <span style="color: red">下载</span>
          <span>等操作;</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer" style="border-bottom: 1px solid gray;width: 93%"></div>

    <div id="nbiInfo" class="infoPageSubTitle">
      <i class="el-icon-discover" style="color: #0b007e"></i>
      <p style="margin-left: 10px">NBI图片及其相关说明：</p>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - NBI成像及其优势
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;NBI全称是</span>
          <span style="color:red;">narrow band imaging</span>
          <span>，中文名</span>
          <span style="color: red">窄带光谱成像</span>
          <span>。被称为内镜医生的“鹰眼视觉”,可降低漏诊率。在NBI检查中，内镜的照明光源切换为窄带蓝光（中心波长415nm）和窄带绿光（中心波长540nm），在屏幕上显示的时候进行了色彩变换。将镜头接收到的蓝光与显示器像素上的蓝、绿发光点对应，将镜头接收到的绿光与显示器像素上的红发光点对应。因此，在检查部位上蓝光反射较多的位置，屏幕上相应地显示为青色；在检查部位上绿光反射较多的位置，屏幕上相应地显示为红色。</span>
          <span>由于黏膜内血液的光学特性对蓝、绿光吸收较强，因此使用难以扩散并能被血液吸收的光波，能够增加黏膜上皮和黏膜下血管的对比度和清晰度。因此，NBI具有相当于粘膜染色的功效，应用时仅需按键切换无需喷洒染色剂，故被称为电子染色内镜。</span>
          <span>NBI图像对观察粘膜表面微结构和微血管重要性已被全世界广泛验证和接受。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - NBI技术结合标本拍摄台的应用
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span style="color: red">标本拍摄台</span>
          <span>通过内镜下切除的离体的黏膜病变组织（如肿瘤），再展开抻平后可更容易暴露全貌（实时内镜下的显示屏很难做到全貌），标本拍摄台可以更好的完成整体标本的高清拍摄（内镜摄像头只有134万像素）存档，去除干扰和反光。</span>
          <br>
          <span>&nbsp;&nbsp;&nbsp;通过结合标本拍摄台与NBI技术，我们 ①可以再次确认手术切除范围，必要时补充切除；②与病理切片的显微结构进行综合比对，提高诊断的准确性和可靠性。③对所切除的病变组织进行图像留存，用于学术交流、教学、科研和印刷出版；</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - NBI-Online的功能
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span>NBI-Online 一个在线合成和管理NBI医用图片的免费工具网站</span>
          <br>
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span>An online NBI Image Generator designed for doctors who don't have much knowledge about image processing.</span>
          <br>
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span>本网站可以接受在标本拍摄台获取的两种波段下的同一标本图片，在线生成NBI图片，同时可以对每一个标本图片进行信息管理和后台存储。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer" style="border-bottom: 1px solid gray;width: 93%"></div>

    <div id="userAgreementInfo" class="infoPageSubTitle">
      <i class="el-icon-discover" style="color: #0b007e"></i>
      <p style="margin-left: 10px">NBI-Online（本网站）用户协议：</p>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - 导语
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;首先，欢迎你使用NBI-Online的服务！</span>
          <span>为了良好的使用NBI-Online服务，你应当阅读并遵守</span>
          <span style="color: red">《NBI-Online用户协议》</span>
          <span>（以下简称“本协议”）。</span>
          <span>请你务必审慎阅读、充分理解各条款内容，并选择接受或不接受。</span>
          <span>除非你已阅读并接受本协议所有条款，否则你无权使用NBI-Online服务。你对NBI-Online服务的登录、查看、使用等行为即视为你已阅读并同意本协议的约束。</span>
          <span>如果你未满18周岁，请在法定监护人的陪同下阅读本协议。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - 协议与服务
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span style="color:red;">协议的范围</span>
          <span>：本协议是你与本网站所有者关于使用NBI-Online服务所订立的协议。</span>
          <br>
          <span>&nbsp;&nbsp;&nbsp;</span>
          <span style="color:red;">关于本服务</span>
          <span>：本网站所包含的服务包括：对上传得到的源图片进行存储、通过得到的源图片生成对应的NBI图片以及一部分的图片处理工作、对用户提交的所有图片数据进行管理等。</span>
          <span>为了保证本网站服务的安全性和功能的一致性，我们有权不经向你特别通知而对软件进行更新，或者对软件的部分功能效果进行改变或限制。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - 用户信息保护
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;保护</span>
          <span style="color: red">用户个人信息</span>
          <span>是我们的基本原则，本网站将会采取合理的措施保护用户的个人信息。除法律法规规定的情形外，未经用户许可不会向第三方公开、透露用户个人信息。我们保证对相关信息采用专业加密存储与传输方式，保障用户个人信息的安全。</span>
          <br>
          <span>&nbsp;&nbsp;&nbsp;关于用户所提交的</span>
          <span style="color: red">标本图片信息</span>
          <span>，本网站保证除法律法规规定的情形外，未经用户许可不会向第三方公开、透露。同时用户有权利在任何时候浏览、修改、删除自己提交的标本图片信息，但出于安全性和身份识别（如号码申诉服务）的考虑，你可能无法修改注册时提供的初始注册信息及其他验证信息。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer">
      <div class="infoPageContend_subTitle">
        <p>
          - 安全责任相关
        </p>
      </div>
      <div class="infoPageContend_info">
        <div style="width: 100%;height: 90%">
          <span>&nbsp;&nbsp;&nbsp;你理解并同意，本网站的服务同大多数网站一样，可能会受多种因素影响，包括但不限于用户原因、网络服务质量、社会环境等；也可能会受各种安全问题的侵扰，包括但不限于他人非法利用用户资料，进行现实中的骚扰；用户下载安装的其他软件或访问的其他网站中可能含有病毒、木马程序或其他恶意程序，威胁你的终端设备信息和数据安全，继而影响本服务的正常使用等。</span>
          <span>维护网站安全与正常使用是我们的共同责任，我们保证将按照行业标准合理审慎地采取必要技术措施保护你的终端设备信息和数据安全，但是你承认和同意本网站并不能就此提供完全保证。</span>
        </div>
      </div>
    </div>
    <div class="infoPageContentContainer" style="border-bottom: 1px solid gray;width: 93%"></div>
<!--    <p>1)uploadTimes</p>-->
<!--    <p>2)userAgreement</p>-->
<!--    <p>3)beSuper</p>-->
<!--    <p>4)userType</p>-->
<!--    <p>5)nbi</p>-->
  </div>
</template>

<script>
export default {
  name: "infoShowPage",
  mounted() {
    // 根据url中的参数跳转到页面的对应位置
    this.initJump();
  },
  methods:{
    initJump(){
      let which = this.$route.query['which'];
      if (which === "uploadTimes"){
        document.getElementById('uploadTimesInfo') .scrollIntoView({ behavior: 'smooth' });
      }
      if (which === "userAgreement"){
        document.getElementById('userAgreementInfo') .scrollIntoView({ behavior: 'smooth' });
      }
      if (which === "userType"){
        document.getElementById('userTypeInfo') .scrollIntoView({ behavior: 'smooth' });
      }
      if (which === "nbi"){
        document.getElementById('nbiInfo') .scrollIntoView({ behavior: 'smooth' });
      }
      if (which === "beSuper"){
        document.getElementById('howToBeSuperUserInfo') .scrollIntoView({ behavior: 'smooth' });
      }
    },
  }
}
</script>

<style scoped>
#infoPageTitle{
  width: 93%;
  height: 80px;
  margin-top: 20px;
  font-family: 幼圆,serif;
  font-size: xx-large;
  font-weight: bold;
  display: flex;
  flex-direction: row;
  align-items: center;
  border-bottom: 1px solid gray;
}
.infoPageContentContainer{
  width: 90%;
  font-family: 幼圆,serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 5px;
  margin-bottom: 15px;
}
.infoPageContend_subTitle{
  width: 90%;
  height: 40px;
  display: flex;
  justify-content: start;
  align-items: start;
  font-weight: bold;
}
.infoPageContend_info{
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  height: auto;
}
.infoPageSubTitle{
  width: 90%;
  height: 45px;
  display: flex;
  flex-direction: row;
  align-items: center;
  font-family: 幼圆,serif;
  font-size: large;
  font-weight: bold;
}
</style>