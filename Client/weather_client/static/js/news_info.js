
// 新闻详情
function write_new_info() {
    var $new_id = window.location.search.split('=')[1]
    $.ajax({
        type: "get",
        url: "http://192.144.143.60:18000/api/v1/news/detail?new_id=" + $new_id,
        
        success: function (result) {
            // result = {
            //     code: 200,
            //     data: {
            //         title: "中牧股份回应兰州兽研所布病事件：生产车间已停产",
            //         categoryld: "产经",
            //         time: "2019年12月27日 08:50",
            //         source: "新京报",
            //         author: "Null",
            //         tag: "中牧卷入兰州兽研所布病事件专题",
            //         context: "　　新京报快讯 据中牧实业股份有限公司12月27日发布消息，2019年12月26日晚22时许...",
            //         imgurl: "Null"
            //     }
            // }
            if (200 == result.code) {
                // console.log(result.data.context)
                var today_news_tag = $("#box")
                var article_content = result.data.context.replace(/\s+/g, '<br>&nbsp;&nbsp;&nbsp;&nbsp;')
                var imgurls = result.data.imgurl.split(',')
                var img_num = imgurls.length
                var ul_html = ''
                ul_html += '<h1 align="center">' + result.data.title + '</h1>'
                ul_html +=  '<div class="top-bar-wrap" id="top-bar-wrap">'
                ul_html +=  '<div class="date-source">'
                ul_html +=  '<span class="date">' + result.data.time + '</span>'
                ul_html +=  '<a href="javascript:void(0);" class="source">' + result.data.source + '</a>'
                ul_html +=  '</div></div>'
                
                ul_html +=  '<div class="article" id="artibody">'
                ul_html +=  '<p class="article-content">' + article_content + '</p>'
                ul_html +=  '</div>'
                ul_html +=  '<div class="article-bottom" id="article-bottom">'
                ul_html +=  '<div class="keywords">'
                ul_html +=  '<label >文章关键词：</label>'
                ul_html +=  '<a href="javascript:void(0);">' + result.data.tag + '</a>'
                ul_html +=  '</div></div>'
                ul_html +=  '<div class="new_imgs_box">'
                for(i=0; i < img_num; i++) {
                	ul_html +=  '<img id="new_imgs" ' + imgurls[i] + ' alt=""/>'
                }
                ul_html +=  '</div>'
                today_news_tag.html(ul_html)
            } else {
                alert(result.error)
            }
        }
    })
}

// 相关新闻
function write_new_recommendations() {
    var $new_id = window.location.search.split('=')[1]
    $.ajax({
        type: "get",
        url: "http://192.144.143.60:18000/api/v1/news/recommendation?new_id=" + $new_id,
        
        success: function (result) {
            // result = {
            //     code: 200,
            //     data: {
            //         n_id: [
            //             3864,
            //             3843,
            //             3540,
            //             3394,
            //             3142,
            //             2923,
            //             2486,
            //             2501,
            //             2240,
            //             2177
            //         ],
            //         title: [
            //             "疾控专家曾光：尚无明确证据表明气温会影响病毒",
            //             "治愈者为何复阳疫情何时结束 钟南山有几个新表态",
            //             "专家复盘：“不明原因肺炎”上报失灵的背后",
            //             "中国-世卫组织联合考察专家组发布权威结论",
            //             "钟南山：18日将发布中药治疗新冠肺炎最新结果",
            //             "国家卫健委专家曾光：武汉再挺一下 就打翻身仗了",
            //             "曾光谈疫情防控：有地方没及时控制好第一代病例",
            //             "流行病学专家：返程途中怎样防护 疫情拐点何时到？",
            //             "武汉早期对疫情重视程度可能不够？专家回应",
            //             "此前通报没提到武汉有医护人员感染?武汉市长回应"
            //         ]
            //     }
            // }
            if (200 == result.code) {
                var news_recommend_tag = $("#news_recommend")
                var news_num = result.data.n_id.length
                var ul_html = ''
                
                for (i=0; i<news_num; i++) {
                    title = result.data.title[i]
                    var title_preview = title.substr(0, 14) 
                    if (title.length > 14){
                        title_preview += '...'
                    }
                    ul_html += '<li><a href="javascript:void(0);" onclick="swap_infopage('
                    ul_html += result.data.n_id[i]
                    ul_html += ')" title="'
                    ul_html += result.data.title[i]
                    ul_html += '">'
                    ul_html += title_preview
                    ul_html += '</a></li>'
                }
                news_recommend_tag.html(ul_html)
            } else {
                alert(result.error)
            }
        }
    })
}