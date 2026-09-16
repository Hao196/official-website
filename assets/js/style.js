$(function(){
    var widths=$(window).width();
    var num=0;
    if(widths>=800){
        $(".nav .list1").css("display","block");
        $(".nav .list2").css("display","none");
        num=4.5;
    }else{
        $(".nav .list1").css("display","none");
        $(".nav .list2").css("display","block");
        num=3
    }
    $('.main_left .list dd').click(function(){
        if($(this).children('ul').css('display')=='none'){
            $(this).children(".dd_tit").addClass('active');
            $(this).children('ul').slideDown(100).children('li');

        }else{
            $(this).children(".dd_tit").removeClass('active');
            $(this).children('ul').slideUp(100);
            $(this).siblings('ul').children('li').children('ul').slideUp(100);

        }
    })
    $(".smenu .list2 .btn").click(function(){
        $(this).parent(".list2").children("ul").slideToggle()
    })

   
                     
    


    var htm=$('#img_ul').html();
    $('#img_ul').append(htm);
    var lenth = $('#img_ul>li').length;
    for(var i=0;i<lenth/2;i++){
        $('<li></li>').appendTo('#qiuye_i');
    }
    //初始化
    function qiuye_resize() {
        liw = document.body.clientWidth || document.documentElement.clientWidth;//获得窗口宽,后面的是兼容ie7
        var liw = $('.banner_box').width();
        var lenth = $('#img_ul li').length;
        $('#img_ul li').width(liw);//动态设置li的宽度
        $('#img_ul').width(liw * lenth);//动态设置ul的宽度
    }
    var i = 0;
    qiuye_resize();
    //改变窗口修正初始化
    window.onresize = function() {
    	if ($(window).width() < 641) {
			j = 3;
		} else {
			j = 5;
		}
		var width_img_div = $('.img_div').width();//定义li的宽度
		$('.img_div ul li').width(width_img_div / j); 
		var length_li = $('.img_div ul li').length;
		var width_li = $('.img_div ul li').outerWidth();
		$('.img_div ul').width(length_li * width_li + length_li); //定义ul的宽度
		$('.img_ul').width(width_li * (j - 1) + $('.img_div ul li .div').width());
        var widths=$(window).width();
        var num
    if(widths>=800){
        $(".nav .list1").css("display","block");
        $(".nav .list2").css("display","none");
        num=4.5;
    }else{
        $(".nav .list1").css("display","none");
        $(".nav .list2").css("display","block");
        num=3
    }
    var wid2=$("#demo").width()
    $("#indemo li").width(wid2/num)
        qiuye_resize();
        qiuye_bo();
        //窗口小于640时隐藏
    }//改变窗口大小的时候会触发这个事件

    var liw = $('.banner_box').width();
    liw = document.body.clientWidth || document.documentElement.clientWidth;//获得窗口宽,后面的是兼容ie7
    //窗口小于640时隐藏左右按钮
    if(liw < 640){
        $('#prevnextt').css('display','none')
    }else{
        $('#prevnextt').css('display','block')
    }

    /*-----------------------轮播主函数-----------------------*/
    function qiuye_bo() {
        if (i >= lenth) {
            $('#img_ul').css('left',(-liw*lenth/2+liw)+'px');
            i = lenth/2;
        }
        else if(i<0){
            $('#img_ul').css('left',(-liw*lenth/2)+'px');
            i=lenth/2-1;
        }
        $('#img_ul').stop().animate({'left': -liw * i},1000);
        $('#qiuye_i li').eq(i<lenth/2?i:i-lenth/2).addClass('on').siblings().removeClass('on');//焦点
        i++;
        //document.title=i;//修改title标签的内容，应该可以去掉
    }
    qiuye_bo();
    var qiuye_interval = setInterval(qiuye_bo, 5000);//设置定时器开始轮播

    //焦点点击事件
    $('#qiuye_i li').click(function() {
        clearInterval(qiuye_interval);
        i = $(this).index();
        qiuye_bo();
        //qiuye_interval = setInterval(qiuye_bo, 5000);
    })
    var wid2=$("#demo").width()
    $("#indemo li").width(wid2/4)
})




// 2019/8/13
$(function(){
    $(".ph_img").click(function(){
        $(".ph_bg").show();
        $(".ph_naver").show();
    });
    $(".ph_bg").click(function(){
        $(this).hide();
        $(".ph_naver").hide();
    });
    $(".ph_foot-link>ul>li").click(function(){
        // $(this).siblings(".ph_link-xl").show().parent("li").siblings().children(".ph_link-xl").hide();
        $(this).find(".ph_link-xl").toggle()
    })
})