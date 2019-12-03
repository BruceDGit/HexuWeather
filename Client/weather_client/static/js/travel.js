function showWeatherNewsBanner() {
    var toggle = true;
    var time = null;
    var nexImg = 0;
    var bannerHeight = $(".weatherNewsBanner ul li img").eq(0).css("height");
    var imgLength = $(".weatherNewsBanner .banner ul li").length;
    var titleList = ['浙江湖州：南浔古镇游兴浓','国庆期间南宁市民观看最古老的烟花——“打铁花”','34辆地方彩车入驻奥林匹克公园 成为国庆热门打卡地'];
    var bannerTitle = $(".weatherNewsBanner .jumpBtn h6");
    $(".weatherNewsBanner").css("height", bannerHeight);
    jumpBtnClrChange(nexImg);

    $(document).ready(function () {
        time = setInterval(intervalImg, 3000);
    });

    function intervalImg() {
        if (nexImg < imgLength - 1) {
            nexImg++;
        } else {
            nexImg = 0;
        }
        $(".weatherNewsBanner .banner ul li").eq(nexImg).css("display", "block");
        $(".weatherNewsBanner .banner ul li").eq(nexImg).stop().animate({ "opacity": 1 }, 100);
        $(".weatherNewsBanner .banner ul li").eq(nexImg - 1).stop().animate({ "opacity": 0 }, 100, function () {
            $(".weatherNewsBanner .banner ul li").eq(nexImg - 1).css("display", "none");
        });
        jumpBtnClrChange(nexImg);
    }
    function jumpBtnClrChange(jumpImg) {
        $(".weatherNewsBanner .jumpBtn ul li").css("background-color", "#666");
        $(".weatherNewsBanner .jumpBtn ul li[jumpImg=" + jumpImg + "]").css("background-color", "#ff7e00");
        var text = titleList[jumpImg];
        bannerTitle.text(text);
    }

    $(".weatherNewsBanner .jumpBtn ul li").each(function () {
        $(this).click(function () {
            clearInterval(time);
            jumpImg = $(this).attr("jumpImg");
            if (jumpImg != nexImg) {
                var after = $(".weatherNewsBanner .banner ul li").eq(jumpImg);
                var befor = $(".weatherNewsBanner .banner ul li").eq(nexImg);
                nexImg = jumpImg;
                after.css("display", "block");
                after.stop().animate({ "opacity": 1 }, 100);
                befor.stop().animate({ "opacity": 0 }, 100, function () {
                    befor.css("display", "none");
                });
            }
            jumpBtnClrChange(jumpImg);
            time = setInterval(intervalImg, 3000);
        });
    });
};
showWeatherNewsBanner();