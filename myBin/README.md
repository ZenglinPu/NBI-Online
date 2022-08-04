NBI-Online 一个在线合成和管理NBI医用图片的免费工具网站

# 安装注意事项
需要使用node.js及其npm工具进行必要工具包的安装
前端采用vue.js实现，后端采用Django实现

在安装好django,node.js等必要组件后，在frontend文件夹下运行
npm i vue-router@3
npm i element-ui -S
npm install axios

# 系统搭建

## 一、系统前后端搭建

### 1、项目需求

- 支持上传一组图片：两张图片（属于同一类的不同的两种图层用户之后的合成）并将合成的图片存储到本地
- 支持对图片的亮度调节并进行保存
- 对已上传图片的关联
- 扩展：对批量上传图片的支持