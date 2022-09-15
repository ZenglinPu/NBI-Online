# NBI-Online
An online NBI Image Generator designed for doctors who don't have much knowledge about image processing.

NBI-Online 一个在线合成和管理NBI医用图片的免费工具网站

## 安装注意事项
需要使用node.js及其npm工具进行必要工具包的安装
前端采用vue.js实现，后端采用Django实现

在安装好django,node.js等必要组件后，在frontend文件夹下运行

npm i vue-router@3

npm i element-ui -S

npm install axios

！注意：pymongo一定不要默认安装最新版本，安装pip install pymongo==3.11.3

## 系统搭建

### 一、系统分析

#### 1、项目需求

- 支持上传一组图片：共三张图片（属于同一类的不同的两种图层用户之后的合成）并将合成的图片存储到本地
- 支持对图片的亮度调节并进行保存
- 对已上传图片的关联
- **TODO**：对批量上传图片的支持
- 对用户个人信息进行管理，包括完善和补充个人信息
- 将用户分为高级用户和初级用户，不同等级的用户将拥有不同的操作权限，用户可以通过一系列的方式成为高级用户
- **TODO**：对一组图片进行附加信息的管理，同时用户可以查看历史提交数据并进行管理

#### 2、功能模块

- 单组图片上传以及处理模块：支持用户上传一组图片，快速反应生成一张NBI图片
- **TODO**：批处理模块，用户通过一定的规则批量上传图片数据
- 用户注册登录模块：通过邮箱验证注册，以及登录（！目前邮件验证并未开启，可以随便注册）
- 用户个人信息管理模块：负责用户完善和补充个人信息，以及管理高级用户和初级用户（管理包括高级用户如何获取，当前身份等等）
- 历史提交数据查看和管理模块，对于历史提交过的数据进行增删改查

### 2. 系统实现

#### 1、项目结构
  - NBI-Online：项目文件夹
    - conf：外部配置参数文件夹，配置参数以yaml格式存储
    - front：前端文件夹，基于Vue实现
      - dist：自动生成文件，在完全开启后端服务器上部署时，需使用npm run build生成
      - public：html文件
      - src：主要开发的资源文件
        - assets：前端静态资源
        - components：前端组件
        - pages：前端分页组件
        - router：Vue路由文件
    - myBin各种自定义的shell文件夹
    - NBIOnline：后端文件夹，基于Django实现
      - NBIOnline
        - dataManagement：本项目使用mongodb管理数据信息，数据管理相关脚本
        - ImageProcess：NBI图片处理相关脚本
        - UserManagement：用户管理相关脚本
      - static：后端静态资源文件
        - img：前端图片静态资源
        - Data：图片实际的存放位置，数据库中仅仅记录图片名称
          - Blue：蓝色波段图片
          - Green：绿色波段图片
          - NBI：最终生成的NBI图片（无压缩）
          - Temp：供前端展示的高压缩图片
          - White：白色光源下的标本图片，**TODO**尝试使用这个图片来自动矫正通道强度
          - Batch：刚刚解压缩的图片临时存放地，经过检查后图片不会存放在这里 **TODO**尝试在检查的时候将图片自动识别成组
        - js
     
#### 2、数据库表
**用户表**

用户信息表: UserInfo

| 字段名          | 类型   | 含义                                                                     |
| -------------- | ------- | -------------------------------------------------------------------------|
| UID            | String  | email地址                                                                |
| pwd            | String  | md5加密后的密码                                                           |
| registerTime   | Time    | 注册时间                                                                  |
| name           | String  | 用户昵称（初始为随机）                                                     |
| expiresTime    | Time    | 高级用户过期时间戳                                                        |
| workPlace      | String  | 用户工作单位（初始为空）                                                   |
| department     | String  | 用户工作部门（初始为空）                                                   |
| competent      | String  | 用户职称（初始为空）                                                       |
| inviteCode     | String  | 邀请码                                                                  |
| isSend         | Boolean | 是否已经赠送过邀请码？true表示已经赠送（每人赠送一次，可多次接受）                  |
| SUM_generate   | Integer | 记录用户生成的总NBI张数                                                    |
| TIMES_generate | Integer | 可生成NBI图片数，超级用户为不限，也为10，但是上传时不会减少，普通用户为10           |

**Token表**

用户token表：TokenInfo

| 字段名         | 类型    | 含义                 |
| -------------- | ------- | --------------------|
| UID            | String  | email地址           |
| expiresTime    | Time    | token过期时间        |
| token          | String  | token值             |
| lastLoginTime  | Time    | 上一次登录的时间     |

**图片信息表**

图片生成信息表：PhotoInfo

| 字段名         | 类型    | 含义                 |
| -------------- | ------- | -------------------------------------------------------------------------|
| UID            | String  | 图片提交者的UID                                                           |
| Image_Green    | String  | 绿光图片名                                                                |
| Image_White    | String  | 白光图片名(可以为空)                                                       |
| Image_Blue     | String  | 蓝光图片名                                                                |
| Image_Result   | String  | NBI合成图片名                                                             |
| Image_Compress | String  | NBI合成后的压缩图片名(这个供前端展示)                                         |
| uploadTime     | Time    | 源图片上传时间                                                            |
| lastChangeTime | Time    | 上一次的修改时间                                                           |
| expireTime     | Time    | 图片数据自动删除的时间，None则表示永久保存                                  |
| isAutoBrightness| Boolean| 最后一次生成时是否自动调节亮度                                              |
| isGenerated    | Boolean | 是否点击了生成按钮，没有的则默认保留24小时                                    |
| contrast       | Integer | 最后一次生成时的对比度                                                     |
| light          | Integer | 最后一次生成时的亮度                                                       |
| saturation     | Integer | 最后一次生成时的饱和度                                                     |
| channelOffset  | Integer | 最后一次生成时的通道调整值                                                 |
| isBatch        | Boolean | 是否是批处理提交的图片，如果是批处理的图片则不在单张的History里面展示              |

**图片附加信息表**

图片附加信息表：PhotoAdditionInfo

| 字段名          | 类型     | 含义                 |
| -------------- | ------- | -------------------------------------------------------------------------|
| GID            | String  | 图片的_id                                                                 |
| sampleName     | String  | 标本名                                                                    |
| part           | String  | 标本部位名                                                                |
| preDiagnosis   | String  | 预诊断结论，可多选，|分割                                                  |
| remark         | String  | 标本备注信息，随意输入                                                     |
| pathologic     | String  | 病理诊断结论，可多选，|分割                                                |
| differentiation| Integer | 分化程度多选：‘0’：不适用 ‘1‘：低分化 ‘2’：中分化 ‘3‘：高分化 多选，|分割    |
| infiltration   | Integer | 浸润深度：单选 0：粘膜上皮层，1:粘膜固有层，2:粘膜肌层3:粘膜下层（文本录入，单位μm），4:固有肌层|
| cuttingEdge    | Boolean | 水平切缘 1-阳性；2-阴性                                                    |

**批处理批次信息表**

批处理批次信息表：BatchProcess

| 字段名         | 类型    | 含义                 |
| -------------- | ------- | ------------------------------------------------------------------------|
| UID            | String  | 图片提交者的UID                                                           |
| batchName      | String  | 批次的名称                                                                |
| srcFolderName  | String  | 存放原始图片数据的文件夹名称，其组成为{batchName}_{uid}{rand}                  |
| uploadTime     | Time    | 这一批次的上传完成的时间                                                    |
| checkTime      | Time    | 这一批次的解压缩、检查完成（通过或不通过）的时间                                 |
| finishTime     | Time    | 这一批次的处理完成（处理错误）时间                                            |
| expireTime     | Time    | 这一批次的过期时间                                                         |
| imgList        | String  | 这一批次所有图片的_id，字符串形式，中间用','分割，其中每条数据是元组的形式           |
| batchSize      | Integer | 这一批次的图片组数                                                         |
| processedNum   | Integer | 这一批次已经处理的图片组数                                                   |
| status         | Integer | 这一批次的处理状态，1-上传中；2-检查中；3-检查失败；4-检查成功；5-处理中；6-处理完成  |
