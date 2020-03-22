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

// 渲染今日资讯数据
function write_24h_news() {
    var $location = localStorage.getItem("location");
    $.ajax({
        type: "get",
        url: "http://192.144.143.60:18000/api/v1/news/today/" + $location,
        success: function (result) {
            // result = {
            //                     code: 200,
            //                     data: {
            //                                 	n_id: [ 4110, 4109 ],
            //                                 	title: [
            //                                 		"台湾地区新增27例新冠肺炎确诊病例 累计135例",
            //                                 		"广东省委书记李希、省长马兴瑞，晚上接站(图)"
            //                                 	],
            //                                 	date: [ "2020-03-20 16:19:00", "2020-03-20 16:29:00" ]
            //                     	}
            //                 }
            if (200 == result.code) {
                var today_news_tag = $("#today_news")
                var id_list = result.data
                var ul_html = ''
                var len = result.data.n_id.length
                for (var i = 0; i < len; i++) {
                    ul_html += '<li> <a href="javascript:void(0);" onclick="swap_infopage('
                    ul_html += result.data.n_id[i]
                    ul_html += ')">'
                    ul_html += result.data.title[i]
                    ul_html += '&nbsp;&nbsp;&nbsp;&nbsp;'
                    ul_html += result.data.date[i].substr(0, 10)
                    ul_html += '</a></li>'
                }
                today_news_tag.html(ul_html)
            } else {
                alert(result.error)
            }
        }
    })
}