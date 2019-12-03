function showBanner() {
	var toggle = true;
	var time = null;
	var nexImg = 0;
	var bannerHeight = $(".c-banner ul li img").eq(0).css("height");
	var imgLength = $(".c-banner .banner ul li").length;
	$(".c-banner").css("height", bannerHeight);
	jumpBtnClrChange(nexImg);

	$(document).ready(function () {
		time = setInterval(intervalImg, 3000);
	});

	$(".preImg").click(function () {
		clearInterval(time);
		nexImg = nexImg - 1;
		if (nexImg < 0) {
			nexImg = imgLength - 1;
		};
		jumpBtnClrChange(nexImg);
		$(".c-banner .banner ul li").eq(nexImg).css("display", "block");
		$(".c-banner .banner ul li").eq(nexImg).stop().animate({ "opacity": 1 }, 1000);
		$(".c-banner .banner ul li").eq(nexImg + 1).stop().animate({ "opacity": 0 }, 1000, function () {
			$(".c-banner ul li").eq(nexImg + 1).css("display", "none");
		});
		time = setInterval(intervalImg, 3000);
	})

	$(".nexImg").click(function () {
		clearInterval(time);
		intervalImg();
		time = setInterval(intervalImg, 3000);
	})

	function intervalImg() {
		if (nexImg < imgLength - 1) {
			nexImg++;
		} else {
			nexImg = 0;
		}

		$(".c-banner .banner ul li").eq(nexImg).css("display", "block");
		$(".c-banner .banner ul li").eq(nexImg).stop().animate({ "opacity": 1 }, 1000);
		$(".c-banner .banner ul li").eq(nexImg - 1).stop().animate({ "opacity": 0 }, 1000, function () {
			$(".c-banner .banner ul li").eq(nexImg - 1).css("display", "none");
		});
		jumpBtnClrChange(nexImg);
	}

	function jumpBtnClrChange(jumpImg) {
		$(".c-banner .jumpBtn ul li").css("background-color", "white");
		$(".c-banner .jumpBtn ul li[jumpImg=" + jumpImg + "]").css("background-color", "grey");
	}

	$(".c-banner .jumpBtn ul li").each(function () {
		$(this).click(function () {
			clearInterval(time);
			jumpImg = $(this).attr("jumpImg");
			if (jumpImg != nexImg) {
				var after = $(".c-banner .banner ul li").eq(jumpImg);
				var befor = $(".c-banner .banner ul li").eq(nexImg);
				nexImg = jumpImg;
				after.css("display", "block");
				after.stop().animate({ "opacity": 1 }, 1000);
				befor.stop().animate({ "opacity": 0 }, 1000, function () {
					befor.css("display", "none");
				});
			}
			jumpBtnClrChange(jumpImg);
			time = setInterval(intervalImg, 3000);
		});
	});
};