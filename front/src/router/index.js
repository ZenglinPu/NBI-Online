// 创建整个应用的路由
// 注意，vue-router应该安装3版本
// npm i vue-router@3
import vueRouter from 'vue-router'
import HistoryData from '@/components/HistoryData'
import UserCenter from '@/components/UserCenter'
import AccountPage from '@/components/AccountPage'

import SingleImage from "@/components/singleImageProcess/SingleImageProcess"
import MultiImage from "@/components/multiImageProcess/MultiImageProcess"

const router = new vueRouter({
    routes:[
        {
            path:"/",
            component:SingleImage,
        },
        {
            path:"/ImageProcess",
            component:SingleImage,
        },
        {
            path:"/ImageProcess/SingleImage",
            component:SingleImage,
        },
        {
            path:"/ImageProcess/MultiImage",
            component:MultiImage,
        },
        {
            path:"/HistoryData",
            component:HistoryData,
        },
        {
            path:"/UserCenter",
            component:UserCenter,
        },
        {
            path:"/AccountPage",
            component:AccountPage,
        },

    ]
});

export default router;