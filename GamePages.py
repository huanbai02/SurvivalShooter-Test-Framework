
from ActionLibrary import GameDriver
import time
from airtest.core.api import snapshot

class MainPage:
    """
    负责处理游戏开始界面（大厅）的逻辑
    """
    def __init__(self, driver: GameDriver):
        self.driver = driver

    def start_game(self):
        print("在主界面寻找开始游戏入口...")
        # 这里复用你的 activate_window 逻辑作为开始
        self.driver.activate_window()
        # 如果有具体的 Start UI，比如 self.driver.click_ui("StartButton")
        time.sleep(5.0) # 等待场景加载

class BattlePage:
    def __init__(self, driver: GameDriver):
        self.driver = driver
        self.poco = driver.poco

    def get_score(self):
        """获取当前分数"""
        score_ui = self.poco("ScoreText") 
        if score_ui.exists():
            text = score_ui.get_text()
            # 这里处理一下，防止获取到 "Score: 100" 这种带文字的
            # 假设 UI 只有数字 "100"
            try:
                return int(text)
            except:
                # 如果解析失败，打印出来看看
                print(f"分数文本解析失败: {text}")
                return -1
        return 0
    
    def fight_routine(self, duration=10):
        """
        执行一套标准的战斗动作
        """
        print(f"开始执行战斗循环，持续 {duration} 秒")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # 动作：打3枪，换个位置，再打3枪
            self.driver.fire(times=3)
            self.driver.move(direction='w', duration=0.5)
            self.driver.fire(times=2)
            self.driver.move(direction='s', duration=0.5)
            
            # 每次动作后简单检查一下血条还在不在
            if not self.driver.assert_ui_exists("HealthSlider", "战斗中检查存活状态"):
                print("角色可能已死亡，停止战斗")
                break

    def wait_for_death(self, timeout=60):
        """等待死亡"""
        print(f"站立挨打中，等待死亡 (超时: {timeout}s)...")
        start = time.time()
        while time.time() - start < timeout:
            # 检测 GameOverText 是否出现
            if self.poco("GameOverText").exists():
                print("检测到 GameOver 界面")
                snapshot(msg="死亡验证")
                return True
            time.sleep(1.0)
        return False

    def wait_for_auto_restart(self, timeout=20):
        """
        等待游戏自动重开
        判断标准：分数归零 且 GameOverText 消失
        """
        print(f"等待关卡自动重置 (超时: {timeout}s)...")
        start = time.time()
        
        while time.time() - start < timeout:
            # 获取当前状态
            current_score = self.get_score()
            is_game_over_visible = self.poco("GameOverText").exists()
                # 判断条件
            if current_score == 0 and not is_game_over_visible:
                print("检测到环境重置：分数归零，UI消失")
                # 额外等待1秒确保场景加载稳定
                time.sleep(1.0)
                return True
            
            time.sleep(1.0) # 每秒轮询一次
            
        print("等待重开超时！")
        return False