// 创建整个应用的路由
// 注意，vue-router应该安装3版本
// npm i vue-router@3
import vueRouter from 'vue-router'
import HistoryData from '@/components/history/HistoryData'
import BatchHistoryData from "@/components/history/BatchHistoryData";
import UserCenter from '@/components/userCenterPage/UserCenter'
import AccountPage from '@/components/account/AccountPage'

import HistoryItemDetailPage from '@/components/history/historyItemDetail/HistoryItemDetailPage'

import SingleImage from "@/components/singleImageProcess/SingleImageProcess"
import MultiImage from "@/components/multiImageProcess/MultiImageProcess"

import InfoShowPage from "@/components/infoPage/infoShowPage"

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
            path:"/HistoryData/BatchHistoryData",
            component:BatchHistoryData,
        },
        {
            name: 'HistoryItemDetailPage',
            path: "/HistoryItemDetailPage/:GID",
            component: HistoryItemDetailPage,
            props:true
        },
        {
            path:"/UserCenter",
            component:UserCenter,
        },
        {
            path:"/AccountPage",
            component:AccountPage,
        },
        {
            path:"/Info",
            component: InfoShowPage,
        }
    ]
});

export default router;