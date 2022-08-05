// 创建整个应用的路由
// 注意，vue-router应该安装3版本
// npm i vue-router@3
import vueRouter from 'vue-router'
import HistoryData from '@/pages/HistoryData'
import ImageProcess from '@/pages/ImageProcess'
import UserCenter from '@/pages/UserCenter'
import AccountPage from '@/pages/AccountPage'

import SingleImage from "@/pages/SingleImageProcess"
import MultiImage from "@/pages/MultiImageProcess"

const router = new vueRouter({
    routes:[
        {
            path:"/",
            component:ImageProcess,
        },
        {
            path:"/ImageProcess",
            component:ImageProcess,
            children:[
                {
                    path:"",
                    component: SingleImage,
                },
                {
                    path:"SingleImage",
                    component: SingleImage,
                },
                {
                    path:"MultiImage",
                    component: MultiImage,
                },
            ]
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