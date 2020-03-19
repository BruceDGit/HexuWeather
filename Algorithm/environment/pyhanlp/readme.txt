step 1, 需要安装HanLP模块, 命令如下:

pip3 install pyhanlp

step 2, 安装完成之后, 需要将下面两个文件放到pyhanlp包的static文件夹下:

	data-for-1.7.zip
	hanlp-1.7.6.jar
    一般路径为 anaconda/lib/python3.6/site-packages/pyhanlp/static

step 3, 做完以上两步, 需要尝试调用一下pyhanlp模块看能否正常运行【有可能需要安装依赖环境jdk，相关指令参考 jdk8 install commands.txt】