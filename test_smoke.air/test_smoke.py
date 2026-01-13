# -*- encoding=utf8 -*-
__author__ = "huanbai"

import sys
import os

current_path = os.path.abspath(__file__)
air_dir = os.path.dirname(current_path)
project_root = os.path.dirname(air_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
from ActionLibrary import GameDriver
from GamePages import MainPage, BattlePage 

auto_setup(__file__)

# 初始化框架
poco = UnityPoco()
driver = GameDriver(poco)

# 初始化页面
main_page = MainPage(driver)
battle_page = BattlePage(driver)


# 进入游戏
print("\n>>> 游戏启动测试")
main_page.start_game()
driver.assert_ui_exists("ScoreText", "检查分数面板出现")

# 核心战斗操作
print("\n>>> 核心战斗循环测试")
battle_page.fight_routine(duration=15) 

# 结算验证
print("\n>>> 验证分数变化")
score_ui = poco("ScoreText")
if score_ui.exists():
    print(f"当前分数 UI 内容: {score_ui.get_text()}")
    
print("\n>>> 测试全流程结束，生成报告")
