1 该目录的命令默认会加入到/usr/local/bin目录(除adb)
  如果用户要改写, 改写后的按后续步骤放置    !!!!!!!!!!!

2 用户根目录建立文件夹bin  (~/bin)

3 修改 ~/.profile,  确认将bin目录加入PATH环境变量中(一般系统默认已经添加)
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

4 将adb命令放置到用户根目录的bin文件夹下

5 更新shell的环境变量
    A 方法一: 重启shell
    B 方法二: source ~/.profile

一些命令的简单介绍
1 adb 可以在ubuntu上使用adb连接板卡
2 zgitpatch  提取commit和前一个版本的完整文件.  喜欢使用BC等比较工具会很喜欢
    zgitpatch  commit   注意该命令必须在git仓库的根目录执行,  即在.git目录同级的位置执行
    
3 zxgrep系列命令  一些针对特定文件查找的命令,  自己可以根据需要添加特定文件后缀的查找
    zxgrep key [path]   在path路径下查找指定文件中的关键字  key   并显示出文件名以及行号    
    zxgrep -w key [patch]   完全匹配查找
