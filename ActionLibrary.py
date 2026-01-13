
import time
import pydirectinput
import pyautogui
from airtest.core.api import snapshot

class GameDriver:
    def __init__(self, poco):
        self.poco = poco

    def activate_window(self):
        """
        点击屏幕中心激活窗口
        """
        print("[Driver] 正在激活游戏窗口...")
        # 点击屏幕中心
        w, h = pyautogui.size()
        pyautogui.click(w // 2, h // 2)
        time.sleep(5.0)

    def move(self, direction='w', duration=1.0):
        """
        控制角色移动
        :param direction: 方向键 (w/a/s/d)
        :param duration: 持续时间
        """
        print(f"[Driver] 移动: 按住 {direction} {duration}秒")
        pydirectinput.keyDown(direction)
        time.sleep(duration)
        pydirectinput.keyUp(direction)
    
    def fire(self, times=1):
        """
        原地开火
        """
        print(f"[Driver] 射击 {times} 次")
        for i in range(times):
            # 模拟按下左键
            pydirectinput.mouseDown() 
            
            # 保持按下状态 0.1 秒
            time.sleep(0.1)   
            
            # 松开左键
            pydirectinput.mouseUp()
            
            # 射击间隔
            time.sleep(0.2)

    def assert_ui_exists(self, ui_name, msg="检查UI存在"):
        """
        断言 UI 是否存在
        """
        if self.poco(ui_name).exists():
            print(f"{msg}: 通过")
            return True
        else:
            print(f"{msg}: 失败！")
            snapshot(msg=f"报错截图_{ui_name}")
            return False