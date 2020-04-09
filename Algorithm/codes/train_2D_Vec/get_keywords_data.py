"""
    获取词频大于1的关键词相关数据
    并将格式转换为前端需要的形式
"""


tag_dict = {}
with open('./data/test_tags.txt', 'r', encoding='utf-8') as f:
    for line in f:
        tag_lst = line.split(',')
        # print(tag_lst)
        if tag_dict.get(tag_lst[0]):
            tag_dict[tag_lst[0]][2] += 1
        else:
            tag_dict[tag_lst[0]] = [tag_lst[1], tag_lst[2].strip(), 1]
res_lst = []
for key, value in tag_dict.items():
    if value[2] > 1:
        lst = [float(value[0]), float(value[1]), value[2], key]
        res_lst.append(lst)
print(res_lst)
