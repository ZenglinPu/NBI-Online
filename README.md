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
- **TODO**：对用户个人信息进行管理，包括完善和补充个人信息
- **TODO**：将用户分为高级用户和初级用户，不同等级的用户将拥有不同的操作权限，用户可以通过一系列的方式成为高级用户
- **TODO**：对一组图片进行附加信息的管理，同时用户可以查看历史提交数据并进行管理

#### 2、功能模块

- 单组图片上传以及处理模块：支持用户上传一组图片，快速反应生成一张NBI图片
- **TODO**：批处理模块，用户通过一定的规则批量上传图片数据
- 用户注册登录模块：通过邮箱验证注册，以及登录（！目前邮件验证并未开启，可以随便注册）
- **TODO**：用户个人信息管理模块：负责用户完善和补充个人信息，以及管理高级用户和初级用户（管理包括高级用户如何获取，当前身份等等）
- **TODO**：历史提交数据查看和管理模块，对于历史提交过的数据进行增删改查

### 2. 系统实现

#### 1、项目结构
  - NBI-Online：项目文件夹
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
        - Data：图片实际的存放位置，数据库中仅仅记录图片名称
          - Blue：蓝色波段图片
          - Green：绿色波段图片
          - NBI：最终生成的NBI图片（无压缩）
          - Temp：供前端展示的高压缩图片
          - White：白色光源下的标本图片，**TODO**尝试使用这个图片来自动矫正通道强度
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
| rank           | Integer | 用户等级（1=普通；2=超级）                                                  |
| expiresTime    | Time    | 高级用户过期时间戳                                                        |
| workPlace      | String  | 用户工作单位（初始为空）                                                   |
| department     | String  | 用户工作部门（初始为空）                                                   |
| competent      | String  | 用户职称（初始为空）                                                       |
| inviteCode     | String  | 邀请码                                                                  |
| SUM_generate   | Integer | 记录用户生成的总NBI张数                                                    |
| TIMES_generate | Integer | 可生成NBI图片数，-1表示不限量                                               |
