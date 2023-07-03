import time
import vgamepad as vg
from PIL import ImageGrab
import math
import pyautogui
import logging
import datetime

art = """
______          _     ______                 _       _
|  ___|        | |    | ___ \               | |     (_)
| |_ _   _  ___| | __ | |_/ / __ _ _ __   __| | __ _ _
|  _| | | |/ __| |/ / | ___ \/ _` | '_ \ / _` |/ _` | |
| | | |_| | (__|   <  | |_/ / (_| | | | | (_| | (_| | |
\_|  \__,_|\___|_|\_\ \____/ \__,_|_| |_|\__,_|\__,_|_|
"""



def get_pixel_color(x, y):
    # 获取屏幕坐标点的颜色
    image = ImageGrab.grab()
    rgb = image.getpixel((x, y))
    image.close()
    return rgb


def colors_approx_equal(color1, color2, tolerance):
    # 计算两个颜色之间的欧几里德距离
    distance = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

    # 判断距离是否在容差范围内
    if distance <= tolerance:
        return True
    else:
        return False


def simulate_combat(gamepad, target_x, target_y, target_color, hp_x, hp_y, hp_color, color_tolerance, timeout):
    # 模拟战斗的方法
    logging.info("开始战斗")

    gamepad.right_joystick(x_value=0, y_value=0)
    gamepad.update()

    start_time = time.time()  # 记录开始时间

    # 正在瞄准敌人 and HP血量不低
    while colors_approx_equal(get_pixel_color(target_x, target_y), target_color, color_tolerance) and (not colors_approx_equal(get_pixel_color(hp_x, hp_y), hp_color, color_tolerance - 4)):
        elapsed_time = time.time() - start_time  # 计算已经过去的时间
        if elapsed_time > timeout:  # 如果已经过去的时间超过timeout秒
            find_enemy_bug(gamepad, target_x, target_y, target_color, color_tolerance)  # 强制寻找敌人
            break
        kill(gamepad)


def find_enemy(gamepad, target_x, target_y, target_color, color_tolerance, timeout):
    # 寻找敌方怪物的方法
    logging.info("开始寻找敌怪")

    start_time = time.time()  # 记录开始时间

    # 收刀
    shou_dao(gamepad)

    # 开始视角旋转
    gamepad.right_joystick(x_value=15000, y_value=0)
    gamepad.update()

    while not colors_approx_equal(get_pixel_color(target_x, target_y), target_color, color_tolerance):
        elapsed_time = time.time() - start_time  # 计算已经过去的时间
        if elapsed_time > timeout:  # 如果已经过去的时间超过timeout秒
            reset_viewpoint(gamepad)
            break
        # 尝试锁定
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
        time.sleep(0.5)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
        time.sleep(0.5)


def simulate_combat_bug(gamepad):
    # 模拟战斗的方法
    logging.info("开始bug模式下的战斗")
    gamepad.right_joystick(x_value=0, y_value=0)
    gamepad.update()
    kill(gamepad)


def find_enemy_bug(gamepad, target_x, target_y, target_color, color_tolerance):
    # 寻找敌方怪物的方法
    logging.info("卡死模式下开始寻找敌怪")

    # 收刀
    shou_dao(gamepad)

    reset_viewpoint(gamepad)

    # 开始视角旋转
    gamepad.right_joystick(x_value=12000, y_value=0)
    gamepad.update()

    while 1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
        time.sleep(0.1)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
        time.sleep(0.3)

        simulate_combat_bug(gamepad)  # 尝试清除新的怪物

        gamepad.right_joystick(x_value=12000, y_value=0)
        gamepad.update()

        if not colors_approx_equal(get_pixel_color(target_x, target_y), target_color, color_tolerance):
            break


def regain_health(gamepad, hp_x, hp_y, hp_color, color_tolerance):
    # 恢复生命值
    logging.info("开始恢复生命值")

    gamepad.right_joystick(x_value=0, y_value=0)
    gamepad.update()

    # 只要生命值低就一直循环
    while colors_approx_equal(get_pixel_color(hp_x, hp_y), hp_color, color_tolerance):
        # 低头
        gamepad.right_joystick(x_value=10000, y_value=-30000)
        gamepad.update()
        skill3(gamepad)
        ping_B(gamepad)
        skillb2(gamepad)
        # 取消锁定
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
        time.sleep(0.1)
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        gamepad.update()
        time.sleep(0.2)
    # 重置视角
    reset_viewpoint(gamepad)


# 重置视角
def reset_viewpoint(gamepad):
    gamepad.right_joystick(x_value=0, y_value=32767)
    gamepad.update()
    time.sleep(1.5)
    gamepad.right_joystick(x_value=0, y_value=-20000)
    gamepad.update()
    time.sleep(1.3)
    gamepad.right_joystick(x_value=0, y_value=0)
    gamepad.update()
    time.sleep(0.1)


# 战斗循环相关：
def kill(gamepad):
    # logging.info("开始技能循环")
    ping_A(gamepad)
    skill1(gamepad)
    next_target()
    ping_A(gamepad)
    skill2(gamepad)
    next_target()
    ping_A(gamepad)
    skill4(gamepad)
    next_target()


def next_target():  # 滚轮向下
    # 万代这个傻逼设置太狗屎了，手柄居然不能切换目标？？？
    pyautogui.scroll(-1)


# 平A 手柄按B
def ping_A(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()
    time.sleep(0.1)


# 平B 也就是右键（
def ping_B(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.update()
    time.sleep(0.1)


# 按左肩键+X 1技能
def skill1(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)  # 左肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)  # x
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(0.1)


# 按左肩键+Y 2技能
def skill2(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)  # 左肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)  # Y
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.update()
    time.sleep(0.1)


# 按左肩键+ 3技能
def skill3(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)  # 左肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # A
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.1)


# 按左肩键+B 4技能
def skill4(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)  # 左肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)  # B
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()
    time.sleep(0.1)


# 按右肩键+A 大招
def skillbt(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)  # 右肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)  # A
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.1)


# 按右肩键+X 战斗幻想1
def skillb1(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)  # 右肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)  # X
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(0.1)


# 按右肩键+Y 战斗幻想2
def skillb2(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)  # 右肩
    gamepad.update()
    time.sleep(0.1)
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)  # Y
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.update()
    time.sleep(0.1)


# 收刀
def shou_dao(gamepad):
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(0.1)


def main():
    print(art)

    # 生成带有日期和时间的日志文件名
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"logfile_{current_time}.log"

    # 配置日志记录器
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 创建一个用于将日志输出到文件的处理器
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 创建一个用于将日志输出到控制台的处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 将处理器添加到日志记录器
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    target_color = (247, 1, 0)  # 敌人 当前目标颜色
    hp_color = (51, 51, 51)  # 血条的背景板的颜色
    target_x = 821
    target_y = 61
    hp_x = 831
    hp_y = 1045
    color_tolerance = 10  # 颜色误差容忍范围
    timeout = 30  # 战斗超时时间

    gamepad = vg.VX360Gamepad()

    reset_viewpoint(gamepad)
    reset_viewpoint(gamepad)

    while True:
        if colors_approx_equal(get_pixel_color(hp_x, hp_y), hp_color, color_tolerance - 4):  # 降低容差
            logging.info("匹配到低于目标血量")
            regain_health(gamepad, hp_x, hp_y, hp_color, color_tolerance)
        else:
            if colors_approx_equal(get_pixel_color(target_x, target_y), target_color, color_tolerance):
                logging.info("匹配到相关颜色")
                simulate_combat(gamepad, target_x, target_y, target_color, hp_x, hp_y, hp_color, color_tolerance, timeout)
                logging.info("战斗结束")
            else:
                logging.info("颜色不匹配")
                find_enemy(gamepad, target_x, target_y, target_color, color_tolerance, timeout)
                logging.info("寻找怪物结束")
                time.sleep(0.3)  # 等待一段时间后继续检测

if __name__ == '__main__':
    main()
