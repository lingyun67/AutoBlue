import win32gui
import win32api


def get_window_coordinates(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    window_rect = win32gui.GetWindowRect(hwnd)
    window_left = window_rect[0]
    window_top = window_rect[1]
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]
    return window_left, window_top, window_width, window_height


# 缩放比例获取函数
def get_scaling_factors(window_title):
    # 获取窗口坐标
    window_left, window_top, window_width, window_height = get_window_coordinates(window_title)

    # 计算窗口的缩放比例
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    scale_x = window_width / screen_width
    scale_y = window_height / screen_height

    return scale_x, scale_y


# 坐标获取函数
def calculate_target_coordinates(window_title, x_original_value, y_original_value):
    # 获取缩放比例
    scale_x, scale_y = get_scaling_factors(window_title)

    # 获取窗口坐标
    window_left, window_top, window_width, window_height = get_window_coordinates(window_title)

    # 计算目标血条的坐标
    target_x = window_left + int(x_original_value * scale_x)
    target_y = window_top + int(y_original_value * scale_y)

    print("target_x:", target_x, "target_y:", target_y)

    return target_x, target_y


def apply_window_scale(target_window_pianyi, target_x, scale_y):
    target_window_pianyi_out = target_window_pianyi * scale_y
    return target_window_pianyi_out

