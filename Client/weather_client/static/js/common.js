// 获取用户定位信息，并将结果保存到本地存储
function getLocation(params_dict) {
    // params_dict: {myfunc:fun_name, params: params}
    var get_url = "http://192.144.143.60:18000/api/v1/user_ip"
    $.ajax({
        // 请求方式
        type: "get",
        // url
        url: get_url,

        //***************  test code begin ***************
        // success: function (result) {
        //     // 查询ip之前，todo 迁移至sucess下
        //     var result_ip = {
        //         'code': 200,
        //         'user_ip': '192.255.255.255'
        //     }
        //     var query_set = result_ip.user_ip
        //     query_url = 'http://192.144.143.60:18000/api/v1/location/' + query_set
        //     $.ajax({
        //         type: "get",
        //         url: query_url,
        //         success: function (result) {
        //             // 发送之前
        //             result_location = {
        //                 'code': 200,
        //                 'location': '天津,天津,和平'
        //             }
        //             // $location_list = result_location.location.split(',');
        //             localStorage.setItem('location', result_location.location);
        //             params_dict.myfunc(params_dict.params)
        //         }
        //     })
        // },
        //***************  test code end ***************

        success: function (result) {
            if (200 == result.code) {
                // 成功获取响应内容
                // var result = {
                // 	'code': 200,
                // 	'user_ip': '192.255.255.255'
                // }
                var query_set = result.user_ip
                query_url = 'http://192.144.143.60:18000/api/v1/location/' + query_set
                // 根据IP获取用户定位
                $.ajax({
                    type: "get",
                    url: query_url,
                    success: function (result_location) {
                        if (200 == result_location.code) {
                            // 成功获取响应内容
                            // result_location = {
                            // 	'code': 200,
                            // 	'location': '天津,天津,和平'
                            // }
                            // $location_list = result_location.location.split(',');
                            localStorage.setItem('location', result_location.location);
                            params_dict.myfunc(params_dict.params)
                        }
                    }
                })
            } else {
                alert(result.error)
            }
        }
    })
}

// 渲染周边天气数据
function write_surrounding_weather() {
    var $location = localStorage.getItem("location");
    $.ajax({
        type: "get",
        url: "http://192.144.143.60:18000/api/v1/weather/" + $location + "?surrounding_weather=1",
        success: function (result) {
            // result = {
            //     'code': 200,
            //     data: {
            //         'location': ['和平区', '河东区', '河西区', '河北区'],
            //         'weather': ['多云', '多云', '多云', '多云'],
            //         'temperature': ['5/13', '5/13', '5/13', '5/13']
            //     }
            // }
            if (200 == result.code) {
                var surrounding_weather_tag = $("#surrounding_weather")
                var ul_html = ''
                ul_html += '<li class="headerLine"><span class="view">地区</span><span>天气</span><span>气温</span></li>'
                var len = result.data.location.length
                for (var i = 0; i < len; i++) {
                    if (i == 0) {
                        ul_html += '<li class="firstLine"><span class="view">'
                        ul_html += result.data.location[i] + '</span><span>'
                        ul_html += result.data.weather[i] + '</span><span>'
                        ul_html += result.data.temperature[i].replace('/', ' ~ ') + '℃</span></li>'
                    } else {
                        ul_html += '<li><span class="view">'
                        ul_html += result.data.location[i] + '</span><span>'
                        ul_html += result.data.weather[i] + '</span><span>'
                        ul_html += result.data.temperature[i].replace('/', ' ~ ') + '℃</span></li>'
                    }
                }
                surrounding_weather_tag.html(ul_html)
            } else {
                alert(result.error)
            }
        }
    })
}

// 渲染周边景点数据
function write_surrounding_tour() {
    var $location = localStorage.getItem("location");
    $.ajax({
        type: "get",
        url: "http://192.144.143.60:18000/api/v1/tour/" + $location + "?surrounding_weather=1",
        success: function (result) {
            // result = {
            //     'code': 200,
            //     data: {
            //         'location': ['天塔', '天津之眼', '水上公园', '盘山', '五大道'],
            //         'weather': ['多云', '多云', '多云', '多云', '多云'],
            //         'temperature': ['5/13', '5/13', '5/13', '5/13', '5/13']
            //     }
            // }
            if (200 == result.code) {
                var surrounding_tour_tag = $("#surrounding_tour")
                var ul_html = ''
                ul_html += '<li class="headerLine"><span class="view">地区</span><span>天气</span><span>气温</span></li>'
                var len = result.data.location.length
                for (var i = 0; i < len; i++) {
                    if (i == 0) {
                        ul_html += '<li class="firstLine"><span class="view">'
                        ul_html += result.data.location[i] + '</span><span>'
                        ul_html += result.data.weather[i] + '</span><span>'
                        ul_html += result.data.temperature[i].replace('/', ' ~ ') + '℃</span></li>'
                    } else {
                        ul_html += '<li><span class="view">'
                        ul_html += result.data.location[i] + '</span><span>'
                        ul_html += result.data.weather[i] + '</span><span>'
                        ul_html += result.data.temperature[i].replace('/', ' ~ ') + '℃</span></li>'
                    }
                }
                surrounding_tour_tag.html(ul_html)
            } else {
                alert(result.error)
            }
        }
    })
}

// 切换新闻详情页
function swap_infopage(new_id) {
    window.location = '/news_info?new_id=' + new_id
    console.log(window.location)
}