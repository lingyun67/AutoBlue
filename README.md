# AutoBlue

一个普普通通的挂机脚本，使用了色块识别、模拟手柄输入、模拟鼠标输入的第三方库

## 开始使用

将本项目下载到本地，然后在项目文件夹运行：

```
pip install -r requirements.txt
```

这将会安装所需要的第三方库

第一次使用之前，你需要进行本机适配。

你需要获取你的客户端的血条的坐标，下载抓抓工具
[https://wwuh.lanzout.com/iAItC115cv2d]
打开抓抓工具之后，随便找一个怪，将鼠标瞄准在它血条的最左边但再往右留几格像素，并且要求瞄准的那颗像素点尽量在血条的垂直中心。此时按下ctrl+alt+1，抓抓工具会显示你获取到的这个位置的坐标。

再用同样方法获取你自己的血条的坐标，此时不是最左边了，大概在你血条80%的位置即可。（v.0.2-Alpha-v2版本及以后若不使用弓箭手可以不设置血条坐标）

打开config.ini，该文件的默认值如下：
```
[General]
# 敌人 当前目标颜色
target_color = 247, 1, 0
# 血条的背景板的颜色
hp_color = 51, 51, 51
x_original_value = 821
y_original_value = 61
hp_x = 831
hp_y = 1045
# 颜色误差容忍范围
color_tolerance = 10
# 战斗超时时间
timeout = 30
# buff导致血条移动像素数
target_window_pianyi_original = 7
```

将你刚刚获取到的坐标，如821,61分别修改到x_original_value与y_original_value中。

默认情况下，第三个3主动技能和第二个战斗幻想和右键作为生命恢复手段，如果不想更改代码请更改游戏内技能位置。

现在可以运行本脚本。

```python
py main.py
```

## 脚本逻辑

- 工作流程是：启动-重置当前视角-旋转搜索目标-锁定目标-进入技能循环-目标死亡-再次搜索目标
- target坐标组所指向的坐标颜色若约等于红色，则判定为当前正在锁定目标，进入战斗循环，反之则进入寻敌循环。
- hp坐标组所指向的坐标颜色若等于玩家血条的背景板的颜色，则强制进入生命恢复循环。
- 因锁定目标可能会发生锁定丢失的情况，现将会在设定的时间经过后强制搜索新的目标
- 旋转搜索时可能因为视角过于诡异导致转了很多圈也搜不到敌人，现将会在设定的时间经过之后重置视角
- 血量过低的时候自动进入血量回复循环（仅限弓箭手）
- 使用vgamepad库进行手柄模拟输入，使用pyautogui库进行鼠标滚轮的输入
- 只要按照16:9的比例缩放窗口，无论窗口放在任意位置，在经过最多30s的时间后都能重新定位血条位置

## 自定义设置

待补充

## 挂机地点推荐

待补充

## 较复杂功能实现

方法get_target_health_bar_coordinates：

如果在1080p的全屏模式下有一个红色的像素在821,61的坐标，这个坐标的xy轴的变量名为x_original_value与y_original_value。

当调用这个get_target_health_bar_coordinates方法的时候会调用现有的get_window_coordinates方法，get_window_coordinates会返回窗口的四个数据：window_left, window_top, window_width, window_height，这四个数据代表窗口左上角的 x 坐标、窗口左上角的 y 坐标、窗口的宽度和窗口的高度。

get_target_health_bar_coordinates方法在获得了这四个数据之后，会用窗口的宽度除以屏幕的宽度，用窗口的高度除以屏幕的高度，这样就得到了缩小的比例。

然后再用红色的像素之前的名为x_original_value与y_original_value的坐标变量乘以该比例，再加到缩小后的窗口的左上角的坐标上，这样就完成了该红色像素点的重新定位。

后续：get_target_health_bar_coordinates方法被拆分为get_scaling_factors方法与calculate_target_coordinates方法，前者用来获取比例，后者用来获取具体坐标


## 更新日志

- v0.1 使用按键精灵进行尝试 识别指定位置(目标血条)的颜色 如果有血条 自动按下平a 自动滚轮向下滚1格来实现切怪，以攻击同屏幕所有小怪
- v0.2 因不能旋转视角遂改用python，使用vgamepad库进行手柄模拟输入，使用pyautogui库进行鼠标滚轮的输入
