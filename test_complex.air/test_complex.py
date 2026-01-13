# -*- encoding=utf8 -*-
__author__ = "huanabi"

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
from ActionLibrary import GameDriver
from GamePages import MainPage, BattlePage

auto_setup(__file__)
poco = UnityPoco()
driver = GameDriver(poco)
main_page = MainPage(driver)
battle_page = BattlePage(driver)

print(">>>启动复杂场景验证...")

# 验证分数增长
print("\n>>> 正向测试：杀敌得分")
driver.activate_window()

# 记录初始分
score_before = battle_page.get_score()
print(f"初始分数: {score_before}")

# 走位并射击
battle_page.fight_routine(duration=10) 

# 验证分数变化
score_after = battle_page.get_score()
print(f"操作后分数: {score_after}")

if score_after > score_before:
    print(f"杀敌验证通过 (分数 +{score_after - score_before})")
else:
    print("警告: 分数未增加 (可能未击中敌人)")


# 死亡循环验证 
print("\n>>> 逆向测试：死亡与自动重置")
print(">>> 操作：停止操作，等待被击杀...")

# 等待死亡
is_dead = battle_page.wait_for_death(timeout=60)
if not is_dead:
    print("测试失败：角色未正常死亡")
    sys.exit(1)

# 自动重开监测
is_restarted = battle_page.wait_for_auto_restart(timeout=15)

# 最终验证
if is_restarted:
    final_score = battle_page.get_score()
    if final_score == 0:
        print("闭环验证通过：游戏已自动重置，分数归零")
    else:
        print(f"异常：游戏重置了，但分数是 {final_score}")
else:
    print("错误：游戏没有自动重开 ")

print("\n>>> 所有测试结束")
