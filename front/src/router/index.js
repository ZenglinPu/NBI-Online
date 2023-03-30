// 创建整个应用的路由
// 注意，vue-router应该安装3版本
// npm i vue-router@3
import vueRouter from 'vue-router'
import HistoryData from '@/components/history/HistoryData'
import UserCenter from '@/components/userCenterPage/UserCenter'
import AccountPage from '@/components/account/AccountPage'
import BatchHistoryData from "@/components/history/BatchHistoryData"
import BatchImgData from "@/components/history/batchHistory/BatchImgData";

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
        // {
        //     path:"/imageProcess",
        //     component:SingleImage,
        // },
        {
            path:"/imageProcess/SingleImage",
            component:SingleImage,
        },
        {
            path:"/imageProcess/MultiImage",
            component:MultiImage,
        },
        {
            path:"/HistoryData/SingleImageData",
            component:HistoryData,
        },
        {
            path: "/HistoryData/BatchHistoryData",
            component: BatchHistoryData,
        },
        {
            name:  'BatchImgData',
            path: "/HistoryData/BatchImgData/:BID",
            component: BatchImgData,
            props:true
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
            name:'Login',
            path:"/AccountPage",
            component: AccountPage,
            props: {w: 1},
        },
        {
            name:'Register',
            path:"/AccountPage",
            component: AccountPage,
            props: {w: 2},
        },
        {
            path:"/Info",
            component: InfoShowPage,
        }
    ]
});

export default router;