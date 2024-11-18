// 整个网页都加载完毕之后在执行
// 在整个页面加载完成之后才会去执行
$(function (){
    $("#captcha-btn").click(function (event){
        // 阻止默认事件
        event.preventDefault();
    //     获取邮箱输入框
        var email = $("input[name='email']").val();
        // alert(email);
        $.ajax({
            url:"captcha/email?email="+email,
            method:"GET",
            success:function (result){
                var code = result['code'];
                if(code == 200){
                    alert("邮箱验证码发送整个")
                }else {
                    alert(result['message'])
                }

            },
            fail:function (error){
                console.log(error);
            }
        })


    });
});