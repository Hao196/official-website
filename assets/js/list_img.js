$(document).ready(function() {
	var j = 5; //可视区的数量
	if ($(window).width() < 641) {
		j = 3;
	}
	
	var width_img_div = $('.img_div').width(); 
	//定义li的宽度
	$('.img_div ul li').width(width_img_div / j);  
	var length_li = $('.img_div ul li').length;
	var width_li = $('.img_div ul li').outerWidth();
	$('.img_div ul').width(length_li * width_li + length_li); //定义ul的宽度
	$('.img_ul').width(width_li * (j - 1) + $('.img_div ul li .div').width());
	//轮播主体 
	var i=0;
	function clickScroll() {
		
		if (i > length_li - j) {
			i = 0;
		}
		var width_li = $('.img_div ul li').outerWidth();
		$('.img_div ul').animate({left: -i * width_li}, 1000)
		i++;
	}
	clickScroll();
	var qiuye_interval = setInterval(clickScroll, 3000);

	
	$('.list_img').hover(function() {
			clearInterval(qiuye_interval);
		}, function() {
			qiuye_interval = setInterval(clickScroll, 3000);
	})
	
	//按钮切换
	$('.prev').click(function() {
		if (i <= 1) {
			i = length_li - j + 2;
		}
		i -= 2;
		clearInterval(qiuye_interval);
		clickScroll();
	})
	
	$('.next').click(function() {
		clearInterval(qiuye_interval);
		clickScroll();
		
	})

})