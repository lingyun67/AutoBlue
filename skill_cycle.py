# 技能循环文件，存放所有职业的所有技能循环方案。
from main import ping_A, next_target, skill1, skill2, skill3, skill4, skillbt, skillb1, skillb2


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
