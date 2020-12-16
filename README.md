# Buffcreeps
  buff挂刀爬虫
  
  ## 依赖源
  依赖sqlite3，requests,PyQt5
  
  ## 使用
  安装好依赖后，执行**main.py**即可。
  使用时需要添加自己的Cookie用来生成库,并输入期望的steam余额比例(默认为0.85)来生成倒货的收益数据
  >Cookie获取方式:
  网页端登录buff,点击[饰品市场](https://buff.163.com/market/?game=csgo#tab=selling&page_num=1)页面后,按下F12,选择Network-XHR  
  选择goods开头的包,复制Headers-Request Headers中的Cookie数据
  
  点击更新数据库开始更新过程  
  
  **注意**:
  
  * 为了保证账号安全,请使用小号的Cookie  
  * 为了降低封号概率,爬取数据,更新数据库的时间会很长  
  * 推荐每次只爬取一到两个大类的物品数据,可大幅降低封号概率,目前未在GUI中实现,可以于getDetils.py 178行 getAllDetils函数中,修改循环range的范围来手动达成该效果
           
   ##  已知问题
           
   印花和其他两个分类物品的适配有问题,尽快解决
   在更新时主界面会失去响应
   
           
    
      
  ## 一些话
  兴趣所致，随手写写
  python和qt水平不高，如有问题还望指正。
  期末繁忙，bug修复/功能扩展随缘补充
