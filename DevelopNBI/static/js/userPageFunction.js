// 初始化
function userPageInit(){
	// 更改页面
    changeByType(1);

	// 根据cookie自动填充
	rememberAc();
}

function rememberAc(){
	pwd = getcookie("NBI_pwd");
	if (pwd != null){
		uid = getcookie("NBI_UID");
		var loginUID = document.getElementById("UserLogin_form_ac");
		var loginPWD = document.getElementById("UserLogin_form_pw");
		var checkBox = document.getElementById("rememAC");
		loginUID.value = uid;
		loginPWD.value = pwd;
		checkBox.checked = true;
	}
}

function changeByType(type){
	var btn1 = document.getElementById("user_loginBtn");
	var btn2 = document.getElementById("user_registerBtn");
	if (type == 2){
		//显示注册页
		btn2.style.background = "#4169E1";
		btn2.style.color = 'white';
        btn1.style.background = "#F8F8FF";
        btn1.style.color = "black";
	}
	else if(type == 1){
		//显示登陆页
		btn1.style.background = "#4169E1";
		btn1.style.color = 'white';
        btn2.style.background = "#F8F8FF";
        btn2.style.color = "black";
	}
}

function switchPage(witch){
    var silder = document.getElementById("mainContainer_switch_slider");
    var container = document.getElementById("mainContainerInner");
    if (witch == 1){
        silder.style.marginLeft = "0%";
        container.style.height = "54%"
    }
    else{
        silder.style.marginLeft = "-100%";
        container.style.height = "60%"
    }
    changeByType(witch);
}

function checkEmail(email){
	var myReg=/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
	if(myReg.test(email)){
		return true;
	}
	return false;
}

function showReliable(){
	var pw = document.getElementById("register_pw");
	var s = document.getElementById("showLs");
	var ls = 0;

    ls = getPwLs(pw.value);
    s.style.display = 'flex';
    if (pw.value.length == 0){
        s.style.display = 'none';
    }

    var s_1ist = [document.getElementById("showLs_block1"),document.getElementById("showLs_block2"),document.getElementById("showLs_block3")];
    for (var t=0;t<s_1ist.length;t++){
        s_1ist[t].style.opacity = '0';
    }
    for (var t=0;t<ls;t++){
        s_1ist[t].style.opacity = '1';
    }
}

// 注册密码复杂度
function getPwLs(s){ 
	var ls = 0;     
	if(s.match(/([a-z])+/)){     
		ls++;     
	}     	
	if(s.match(/([0-9])+/)){     
		ls++;       
	}     	
	if(s.match(/([A-Z])+/)){     
		ls++;     
	}     
	if(s.match(/[^a-zA-Z0-9]+/)){     
		ls++;     
	}     
	if (ls > 1){
		ls -= 1;
	}
	return ls
}

function sendEmailCode(){
	var email = document.getElementById("email");
	var btn = document.getElementById("getValidcodeBtn");
	if (!checkEmail(email.value)){
		email.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入符合规范的电子邮箱");
		return;
	}
	// 让发送按钮失效
	btn.value = '发送中...';
	btn.setAttribute("disabled","disabled");
	$.ajax({
		url:'/NBI/User/register/sendemail',
		data:{
			"email" : email.value,
		},
		type:'post',//HTTP请求类型
		timeout:10000,//超时时间设置为10秒；
		async: true,//同步的方式
		success:function(responseData){
			alert(responseData);
			startTiming(btn,60);
		},
		error:function(xhr,type,errorThrown){
			alert("操作失败,请稍后重试");
		}
	});
}

function startTiming(which, time){
	var timer_num = time;

    timeClock=setInterval(function(){
        timer_num--;
        which.value = timer_num + 's';
        
        if (timer_num == 0) {
            clearInterval(timeClock);
            which.value = '再次发送';
            which.removeAttribute('disabled');
        } 
    },1000)
}

function registerCheck(){
	var email = document.getElementById("register_email");
	if (!checkEmail(email.value)){
		email.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入符合规范的电子邮箱");
		return;
	}
	// var validecode2 = document.getElementById("validcode2");
	// TODO 验证码功能暂时没有做
	// if (validecode2.value.length <6){
	// 	validecode2.style.borderBottom = "#FF2200 solid 2px";
	// 	alert("请输入邮件中的验证码");
	// 	return;
	// }
	var pwd = document.getElementById("register_pw");
	var pwd_check = document.getElementById("pw_check");
	if (pwd.value != pwd_check.value){
		pwd.style.borderBottom = "#FF2200 solid 2px";
		pwd_check.style.borderBottom = "#FF2200 solid 2px";
		pwd.value = "";
		pwd_check.value = "";
		alert("两次密码输入不一致");
		return;
	}

	if (pwd.value == ''){
		pwd.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入注册密码");
		return;
	}

	var formData = new FormData();
	formData.append("email", email.value);
	formData.append("pw", pwd.value);
	$.ajax({
		url:'/NBI/User/register/',
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
        if (responseData == 0){
            alert("注册失败，该邮箱地址已被注册！");
			email.value = "";
			pwd.value = "";
			pwd_check.value = "";
        }
        else if (responseData == 1){
            alert("注册成功！请登录。");
			setTimeout(function(){
				switchPage(1);
			}, 5000);
        }
    });
}

function loginCheck(){
	var uid = document.getElementById("UserLogin_form_ac");
	if (uid.value==""){
		uid.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入注册邮箱！")
		return;
	}
	var pwd = document.getElementById("UserLogin_form_pw");
	if (pwd.value == ""){
		pwd.style.borderBottom = "#FF2200 solid 2px";
		alert("请输入密码");
		return;
	}
	// 检查能否成功登录，如果成功，根据是否保存更新cookie，并且记录token和uid
	var formData = new FormData();
	formData.append("uid", uid.value);
	formData.append("pwd", pwd.value);
	checkResult = false
	$.ajax({
		url:'/NBI/User/checkLogin/',
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
        if (responseData == 1){
			uid.style.borderBottom = "#FF2200 solid 2px";
			alert("该邮箱未注册！");
			return;
		}
		else if (responseData == 2){
			pwd.style.borderBottom = "#FF2200 solid 2px";
			alert("密码错误！");
			return
		}
		else{
			// 登录成功
			setcookie("NBI_token",responseData.token, 2, "/NBI");
			setcookie("NBI_UID", responseData.uid, 72, "/NBI");
			showAccountStatus(responseData.uname);
			if (document.getElementById("rememAC").checked){
				//记录pwd
				setcookie("NBI_pwd", pwd.value, 72, "/NBI");
			}
			alert("登录成功！");
			setTimeout(function(){
				jumpToMainPage();
			}, 4000);
		}
    });
}