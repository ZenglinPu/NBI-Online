function mainPageInitProcess(){
    // 初始化滑块数值
    var slider = document.getElementById("brightnessAdjustRange");
    if (slider != null){
        var value = document.getElementById("brightnessValue");
        slider.value = 0;
        value.innerText = 0;
    }

    var cslider = document.getElementById("contrastAdjustRange");
    if (cslider != null){
        var cvalue = document.getElementById("contrastOffsetValue");
        cslider.value = 100;
        cvalue.innerHTML = 100;
    }

    var nslider = document.getElementById("numinosityAdjustRange");
    if (nslider != null){
        var nvalue = document.getElementById("numinosityOffsetValue");
        nslider.value = 100;
        nvalue.innerHTML = 100;
    }

    var sslider = document.getElementById("saturationAdjustRange");
    if (sslider != null){
        var svalue = document.getElementById("saturationOffsetValue");
        sslider.value = 100;
        svalue.innerHTML = 100;
    }
}

// 这里仅仅是选择图片
function uploadBlueImage(){
    var blueBotton = document.getElementById("blueImageBotton");
    blueBotton.click();
}

function blueImageShowChange(){
    var imageShow_blue = document.getElementById("icon_blue");
    imageShow_blue.className = "uploadIcon";

    var blueBotton = document.getElementById("blueImageBotton");
    var blueBotton_show = document.getElementById("blueImageBotton_Show");
    document.getElementById("isUpload").innerHTML = 0;

    // 显示文件名
    blueBotton_show.innerHTML = "选择蓝色光源图片(415nm)<br>"+getFileName(blueBotton.value);

    // 根据后缀名判断是否显示
    var fileType = getFileType(blueBotton.value);
    var imageShow = document.getElementById("icon_blue");
    if (fileType == "jpg" || fileType =="JPG" || fileType=="jpeg"){
        var file = blueBotton.files[0]; // 获取input上传的图片数据;
        var read = new FileReader(); // 创建FileReader对像;
        read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
        read.onload = function() {
            var url = read.result; // 拿到读取结果;
            imageShow.src = url;
        }
        imageShow.className = "uploadImageShow";
    }else{
        imageShow.src = "/static/img/unknownImageTypeIcon.png";
    }
}

function uploadGreenImage() {
    var greenBotton = document.getElementById("greenImageBotton");
    greenBotton.click();
}

function greenImageShowChange(){
    var imageShow_green = document.getElementById("icon_green");
    imageShow_green.className = "uploadIcon";

    var greenButton = document.getElementById("greenImageBotton");
    var greenButton_show = document.getElementById("greenImageBotton_Show");
    document.getElementById("isUpload").innerHTML = 0;

    // 显示文件名
    greenButton_show.innerHTML = "选择绿色光源图片(540nm)<br>"+getFileName(greenButton.value);

    var fileType = getFileType(greenButton.value);
    var imageShow = document.getElementById("icon_green");
    if (fileType == "jpg" || fileType =="JPG" || fileType=="jpeg"){
        var file = greenButton.files[0]; // 获取input上传的图片数据;
        var read = new FileReader(); // 创建FileReader对像;
        read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
        read.onload = function() {
            var url = read.result; // 拿到读取结果;
            imageShow.src = url;
        }
        imageShow.className = "uploadImageShow";
    }else{
        imageShow.src = "/static/img/unknownImageTypeIcon.png";
    }
}

function uploadWhiteImage() {
    var whiteBotton = document.getElementById("whiteImageBotton");
    whiteBotton.click();
}

function whiteImageShowChange(){
    var imageShow_white = document.getElementById("icon_green");
    imageShow_white.className = "uploadIcon";

    var whiteButton = document.getElementById("whiteImageBotton");
    var whiteButton_show = document.getElementById("whiteImageBotton_Show");
    document.getElementById("isUpload").innerHTML = 0;

    // 显示文件名
    whiteButton_show.innerHTML = "选择白色光源图片(非必须)<br>"+getFileName(whiteButton.value);

    var fileType = getFileType(whiteButton.value);
    var imageShow = document.getElementById("icon_white");
    if (fileType == "jpg" || fileType =="JPG" || fileType=="jpeg"){
        var file = whiteButton.files[0]; // 获取input上传的图片数据;
        var read = new FileReader(); // 创建FileReader对像;
        read.readAsDataURL(file); // 调用readAsDataURL方法读取文件;
        read.onload = function() {
            var url = read.result; // 拿到读取结果;
            imageShow.src = url;
        }
        imageShow.className = "uploadImageShow";
    }else{
        imageShow.src = "/static/img/unknownImageTypeIcon.png";
    }
}

function uploadNewImage(){
    // 检查是否已经login
    if (document.getElementById("isLogin").innerHTML != 1){
        alert("请先登录");
        return;
    }

    var blueBotton = document.getElementById("blueImageBotton");
    var greenBotton = document.getElementById("greenImageBotton");
    var uid = getcookie("NBI_UID");
    var token = getToken();

    uploadButton = document.getElementById("uploadBtn");
    uploadButton.setAttribute("disabled","disabled");
    uploadStatus = document.getElementById("uploadStatus");
    uploadStatus.innerText = "上传中...";
    uploadStatus.style.color = "rgb(157, 99, 18)";

    var imageForm = new FormData();
    imageForm.append("image_blue", blueBotton.files[0]);
    imageForm.append("image_green", greenBotton.files[0])
    imageForm.append("user", uid);
    imageForm.append("token", token);

    $.ajax({
		url:'/NBI/Image/upload/',
		type: 'POST',
        cache: false,
        data: imageForm,
        async: true,
        processData: false,
        contentType: false,
		error:function(xhr,type,errorThrown){
			alert("操作失败,请稍后重试");
            uploadStatus.innerText = "等待上传";
            uploadStatus.style.color = "rgb(166, 0, 0)";
            uploadButton.removeAttribute('disabled');
		}
	}).done(function (responseData) {
        if (responseData == 1){
            alert("登录状态错误！请重新登录。");
            uploadStatus.innerText = "等待上传";
            uploadStatus.style.color = "rgb(166, 0, 0)";
        }
        else if (responseData == 2){
            alert("您提交的图片为空，请检查！");
            uploadStatus.innerText = "等待上传";
            uploadStatus.style.color = "rgb(166, 0, 0)";
        }
        else if (responseData == 3){
            alert("图片存储错误，目前仅支持常见格式。");
            uploadStatus.innerText = "等待上传";
            uploadStatus.style.color = "rgb(166, 0, 0)";
        }
        else{
            var imageShow_green = document.getElementById("icon_green");
            imageShow_green.className = "uploadImageShow";
            var imageShow_blue = document.getElementById("icon_blue");
            imageShow_blue.className = "uploadImageShow";

            setTimeout(function(){
                imageShow_green.src = "/static/Data/Green/"+responseData.image_green;
                imageShow_blue.src = "/static/Data/Blue/"+responseData.image_blue;
            },50);

            uploadStatus.innerText = "已上传";
            uploadStatus.style.color = "#3eff24";
            document.getElementById("isUpload").innerHTML = 1;
        }
        uploadButton.removeAttribute('disabled');
    });
}

function brightnessValueChange(){
    var slider = document.getElementById("brightnessAdjustRange");
    var bvalue = document.getElementById("brightnessValue");
    bvalue.innerText = slider.value;
}

function channelValueChange(){
    var slider = document.getElementById("channelAdjustRange");
    var bvalue = document.getElementById("channelOffsetValue");
    bvalue.innerText = slider.value;
}

function contrastValueChange(){
    var slider = document.getElementById("contrastAdjustRange");
    var bvalue = document.getElementById("contrastOffsetValue");
    bvalue.innerText = slider.value;
}

function numinosityValueChange(){
    var slider = document.getElementById("numinosityAdjustRange");
    var bvalue = document.getElementById("numinosityOffsetValue");
    bvalue.innerText = slider.value;
}

function saturationValueChange(){
    var slider = document.getElementById("saturationAdjustRange");
    var bvalue = document.getElementById("saturationOffsetValue");
    bvalue.innerText = slider.value;
}

function getResultImage(){
    if (document.getElementById("isUpload").innerHTML != 1){
        alert("请先完成图片上传");
        return;
    }

    // 检查是否已经login
    if (document.getElementById("isLogin").innerHTML != 1){
        alert("请先登录");
        return;
    }

    var getResultBtn = document.getElementById("getResultImage");
    getResultBtn.innerHTML = "生成中...";
    getResultBtn.setAttribute("disabled","disabled");
    if (!document.getElementById("openFunction").checked){
        // 仅仅调整亮度和通道
        var getResultForm = new FormData();
        
        getResultForm.append("token", getToken());
        getResultForm.append("user", getUID());
        var channelOffsetRange = document.getElementById("channelAdjustRange");
        getResultForm.append("channelOffset", channelOffsetRange.value);
        var brightnessRange = document.getElementById("brightnessAdjustRange");
        getResultForm.append("brightnessAdjust", brightnessRange.value);
        var isAutoChannel = document.getElementById("isAutoChannel").checked;
        var isAutoBrightness = document.getElementById("isAutoBrightness").checked;
        getResultForm.append("isAutoChannel", isAutoChannel);
        getResultForm.append("isAutoBrightness", isAutoBrightness);

        getResultForm.append("mode", "easy")

        $.ajax({
            url:'/NBI/Image/getResult/',
            type: 'POST',
            cache: false,
            data: getResultForm,
            async: true,
            processData: false,
            contentType: false,
            error:function(xhr,type,errorThrown){
                alert("操作失败,请稍后重试");
                return;
            }
        }).done(function (responseData) {
            if (responseData == 1){
                alert("登录状态错误！");
            }
            else if (responseData == 2){
                alert("请求方式错误！");
            }
            else if (responseData == 3){
                alert("图片处理错误");
            }
            else{
                showResultImage(responseData);
            }
            getResultBtn.innerHTML = "生成图片";
            getResultBtn.removeAttribute('disabled');
        });
    }
    else{
        // 包括更多更复杂的图片调整
        var getResultForm = new FormData();
        
        getResultForm.append("token", getToken());
        getResultForm.append("user", getUID());
        var channelOffsetRange = document.getElementById("channelAdjustRange");
        getResultForm.append("channelOffset", channelOffsetRange.value);
        var brightnessRange = document.getElementById("brightnessAdjustRange");
        getResultForm.append("brightnessAdjust", brightnessRange.value);
        var isAutoChannel = document.getElementById("isAutoChannel").checked;
        var isAutoBrightness = document.getElementById("isAutoBrightness").checked;
        getResultForm.append("isAutoChannel", isAutoChannel);
        getResultForm.append("isAutoBrightness", isAutoBrightness);

        // 对比度、明度、饱和度
        var contrastOffsetRange = document.getElementById("contrastAdjustRange");
        getResultForm.append("contrastOffset", contrastOffsetRange.value);
        var numinosityOffsetRange = document.getElementById("numinosityAdjustRange");
        getResultForm.append("numinosityOffset", numinosityOffsetRange.value);
        var saturationOffsetRange = document.getElementById("saturationAdjustRange");
        getResultForm.append("saturationOffset", saturationOffsetRange.value);

        getResultForm.append("mode", "full");
        $.ajax({
            url:'/NBI/Image/getResult/',
            type: 'POST',
            cache: false,
            data: getResultForm,
            async: true,
            processData: false,
            contentType: false,
            error:function(xhr,type,errorThrown){
                alert("操作失败,请稍后重试");
                return;
            }
        }).done(function (responseData) {
            if (responseData == 1){
                alert("登录状态错误！");
            }
            else if (responseData == 2){
                alert("请求方式错误！");
            }
            else if (responseData == 3){
                alert("图片处理错误");
            }
            else{
                showResultImage(responseData);
            }
            getResultBtn.innerHTML = "生成图片";
            getResultBtn.removeAttribute('disabled');
        });
    }
}

function showResultImage(imageData){
    var container = document.getElementById("imgBackPart");
    var defaultText = document.getElementById("outImageDefault");
    if (defaultText != null) {
        defaultText.parentNode.removeChild(defaultText);
    }

    var lastResultImage = document.getElementById("resultImage");
    if (lastResultImage != null){
        lastResultImage.parentNode.removeChild(lastResultImage);
    }
    
    var resultImage = document.createElement("img");
    setTimeout(function(){
        resultImage.id = "resultImage";
        resultImage.src = "/static/Data/Temp/"+imageData.showImage;
    }, 50)

    container.appendChild(resultImage);

    var recordRealResult = document.getElementById("resultImageDownloadUrl");
    recordRealResult.innerHTML = imageData.resultImage;
}


function downloadResult(){
    // 检查是否存在生成图片
    var resultImage = document.getElementById("resultImage");
    if (resultImage == null){
        alert("请先点击生成图片！");
        return -1;
    }

    var isFirst = document.getElementById("firstTimeShowDownloadInfo");
    if (isFirst.innerHTML == "1"){
        isFirst.innerHTML = "0";
        alert("已开始下载，如图片较大会需要一定反应时间，请耐心等待。");
    }

    var recordRealResult = document.getElementById("resultImageDownloadUrl").innerHTML;
    // downloadByBlob("/static/Data/NBI/"+recordRealResult, "resultNBI.jps");
    downloadIamge("/static/Data/NBI/"+recordRealResult, "resultNBI.jpg");
}

function downloadIamge(imgSrc, fileName){
    var alink = document.createElement("a");
    alink.href = imgSrc;
    alink.download = fileName; //fileName保存提示中用作预先填写的文件名
    alink.click();
}

function getFileName(o){
    var pos=o.lastIndexOf("\\");
    return o.substring(pos+1); 
}

function getFileType(o){
    var pos=o.lastIndexOf(".");
    return o.slice(pos+1, o.length);
}

function ChooseLastImage(){
    var getLastForm = new FormData();
    getLastForm.append("user", getUID());
    $.ajax({
        url:'/NBI/Image/chooseLastImage/',
        type: 'POST',
        cache: false,
        data: getLastForm,
        async: true,
        processData: false,
        contentType: false,
        error:function(xhr,type,errorThrown){
            alert("操作失败,请稍后重试");
            return;
        }
    }).done(function (responseData) {
        if (responseData == 1){
            alert("未找到上次提交图片");
            return;
        }
        else{
            alert(2);
        }
    });
}

function addInfoPartChange(){
    var choose = document.getElementById("addInfo_bodyPart").value;
    if (choose == " 其他"){
        var fatherContainer = document.getElementById("addInfo_bodyPart_Container");
        var addInput = document.createElement("div");
        addInput.className = "addInfo";
        addInput.id = "addInfo_bodyPart_other_Container";
        
        var addInput_p = document.createElement("p");
        addInput_p.innerHTML = "";
        addInput_p.className = "addInfo_formLabel";
        addInput.appendChild(addInput_p);

        var addInput_text = document.createElement("input");
        addInput_text.id = "addInfo_bodyPart_other";
        addInput_text.className = "addInfo_formInput";
        addInput_text.setAttribute("AUTOCOMPLETE", "off");
        addInput_text.setAttribute("type", "text");
        addInput_text.setAttribute("placeholder", " 输入其他标本部位名称");
        addInput.appendChild(addInput_text);

        var addInput_p2 = document.createElement("p");
        addInput_p2.innerHTML = "";
        addInput_p2.style.width = "5%";
        addInput.appendChild(addInput_p2);

        fatherContainer.appendChild(addInput);
    }else{
        var c = document.getElementById("addInfo_bodyPart_other_Container");
        if (c != null){
            document.getElementById("addInfo_bodyPart_Container").removeChild(c);
        }
    }
}

function addInfodiagnoseBeforeChange(){
    var chooseList = document.getElementsByName("addInfo_diagnoseBefore_c");
    // 使用字符串数组，用于存放选择好了的数据
    var chooseResult = new Array(chooseList.length);
    for(var i = 0;i < chooseList.length;i++) {
        if (chooseList[i].selected == true) {
            chooseResult[i] = chooseList[i].value;//这个是获取多选框中的值
        }
    }
    var fatherContainer = document.getElementById("addInfo_diagnoseBefore_Container");
    if (chooseResult[5] != undefined){
        if (document.getElementById("addInfo_diagnoseBefore_other_Container")!=null){
            return;
        }
        var addInput = document.createElement("div");
        addInput.className = "addInfo";
        addInput.id = "addInfo_diagnoseBefore_other_Container";
        
        var addInput_p = document.createElement("p");
        addInput_p.innerHTML = "";
        addInput_p.className = "addInfo_formLabel";
        addInput.appendChild(addInput_p);

        var addInput_text = document.createElement("input");
        addInput_text.id = "addInfo_diagnoseBefore_other";
        addInput_text.className = "addInfo_formInput";
        addInput_text.setAttribute("AUTOCOMPLETE", "off");
        addInput_text.setAttribute("type", "text");
        addInput_text.setAttribute("placeholder", " 输入其他早期诊断结论");
        addInput.appendChild(addInput_text);

        fatherContainer.appendChild(addInput);
    }
    else{
        var c = document.getElementById("addInfo_diagnoseBefore_other_Container");
        if (c != null){
            document.getElementById("addInfo_diagnoseBefore_Container").removeChild(c);
        }
    }
}