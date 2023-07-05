"""
技能循环文件，存放所有职业的所有技能循环方案。

可使用的方法有：ping_A, ping_B, next_target, skill1, skill2, skill3, skill4, skillbt, skillb1, skillb2
含义分别为：平A, 右键, 切换到下一个目标, 技能1, 技能2, 技能3, 技能4, 大招, 战斗幻想1, 战斗幻想2

切换到下一个目标方法需要这样写：next_target(next_target_enabled)
其余所有方法需要这样写：ping_A(gamepad)
也就是括号内需要有参数，切换目标方法的参数是判断该功能是否开启的
普通攻击及技能方法内的参数是gamepad手柄信号模拟对象
"""
from main import ping_A, ping_B, next_target, skill1, skill2, skill3, skill4, skillbt, skillb1, skillb2


# 弓箭手循环方案
def method1(gamepad, next_target_enabled):
    # logging.info("开始技能循环")
    ping_A(gamepad)
    skill1(gamepad)
    next_target(next_target_enabled)
    ping_A(gamepad)
    skill2(gamepad)
    next_target(next_target_enabled)
    ping_A(gamepad)
    skill4(gamepad)
    next_target(next_target_enabled)


def method2(gamepad, next_target_enabled):
    # logging.info("开始技能循环")
    ping_A(gamepad)
    skill1(gamepad)
    next_target(next_target_enabled)
    ping_A(gamepad)
    skill2(gamepad)
    next_target(next_target_enabled)
    ping_A(gamepad)
    skill4(gamepad)
    next_target(next_target_enabled)
