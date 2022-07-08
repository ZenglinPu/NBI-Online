var loc = "http://49.232.229.126:7000";

//主页面
function jumpToMainPage(){
    window.location.replace(loc+"/NBI/mainPage/");
}

//批处理页面
function jumpToBatchProcess(){

}

//用户管理界面
function jumpToLogin(){
    window.location.replace(loc+"/NBI/User/loginPage");
}

function jumpToUserCenter(){
    alert(1);
}

// cookie
function getcookie(objname){//获取指定名称的cookie的值
    var arrstr = document.cookie.split("; ");
    for(var i = 0;i < arrstr.length;i ++){
        var temp = arrstr[i].split("=");
        if(temp[0] == objname) return temp[1];
    }
    return null;
}

function setcookie(name, value, hours, path) {
    var expires = new Date();
    expires.setTime(expires.getTime() + hours * 3600000);
    path = path == "" ? "" : ";path=" + path;
    _expires = (typeof hours) == "string" ? "" : ";expires=" + expires.toUTCString();
    document.cookie = name + "=" + value + _expires + path;
}

// 根据本地token和uid信息检查登录状态
function accountStatusCheck(){
    var isLogin = document.getElementById("isLogin");
    // 本地无token，未登录
    token = getcookie("NBI_token");
    if (token == null){
        noLoginStatus();
        isLogin.innerHTML = 0;
    }

    // 本地有token，与uid一起上传
    uid = getcookie("NBI_UID");
    var formData = new FormData();
	formData.append("uid", uid);
	formData.append("token", token);
    $.ajax({
		url:'/NBI/User/checkByToken/',
		type: 'POST',
        cache: false,
        data: formData,
        async: true,
        processData: false,
        contentType: false,
		error:function(xhr,type,errorThrown){
			alert("操作失败,请稍后重试");
		}
	}).done(function (responseData) {
        var checkResult = responseData.check;
        // console.log(checkResult);
        var newToken = responseData.token;
        var uname = responseData.uname;
        if (checkResult == 0){
            noLoginStatus();
            isLogin.innerHTML = 0;
        }
        else if(checkResult == 1){
            noLoginStatus();
            alert("登录已过期，请重新登录");
            isLogin.innerHTML = 0;
            clearCookie("NBI_token");
        }
        else if(checkResult == 2){
            setcookie("NBI_token",newToken, 2, "/NBI");
            showAccountStatus(uname);
            isLogin.innerHTML = 1;
        }
    });
}

// 更新顶部登录状态显示
function showAccountStatus(uname){
    var aci = document.getElementById("accountInfo");
    aci.innerHTML = uname;
    var acs = document.getElementById("accountStatus");
    acs.innerHTML = "欢迎使用NBI—Online";
}

function noLoginStatus(){
    var aci = document.getElementById("accountInfo");
    aci.innerHTML = "未登录";
    var acs = document.getElementById("accountStatus");
    acs.innerHTML = "登录 / 注册";
}

function clearCookie(name) {  
    setcookie(name, "", -1, "/NBI");
}  

function getToken(){
    return getcookie("NBI_token");
}

function getUID(){
    return getcookie("NBI_UID");
}