# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2023-08-12
# @file    : cls.py
# @function:

import os.path
import pickle

from utils import SAVE_DIR, PROJECTS_PICKLE_FILENAME, INCUBATE_PICKLE_FILENAME


class ManagerInitializer:
    prog = 'aifm.py'  # 程序名
    # usage = ''  # 程序使用方式
    description = '“AIFM(Achievement Inventive Fund ' \
                  'Manager, 成就激励基金管理器)”是一个基金项目管理和跟踪工具. ' \
                  '用户通过记录并达成一定目标和成就, 以触发自己设定的奖励.'  # 程序帮助文档
    epilog = f'本地存档保存在{SAVE_DIR}目录下的{PROJECTS_PICKLE_FILENAME}文件中.'  # 程序额外说明

    def __init__(self):
        self._check_savefile()

    def _check_savefile(self):
        projects_filepath = os.path.join(SAVE_DIR, PROJECTS_PICKLE_FILENAME)
        incubate_filepath = os.path.join(SAVE_DIR, INCUBATE_PICKLE_FILENAME)
        if not os.path.exists(projects_filepath):  # 未找到存档文件, 则创建新的空白存档文件
            with open(projects_filepath, 'wb') as f:
                pickle.dump(list(), f)
            print(f'> 已创建空白项目存档文件: {projects_filepath}')
        if not os.path.exists(incubate_filepath):
            with open(incubate_filepath, 'wb') as f:
                pickle.dump(list(), f)
            print(f'> 已创建空白奖励存储文件: {incubate_filepath}')


class FundProject:
    """基金项目[基类]"""
    project_type = '基金项目'
    award = ''
    description = ''

    def __init__(self):
        # TODO: 周期项目  self.is_period
        # TODO: 循环项目  self.is_cycle
        pass


class SelfDefinedFundProject(FundProject):
    """自定义基金项目"""
    project_type = '自定义基金项目'
    award = '自定义奖励'
    description = '项目描述.'

    def __init__(self, project_name: str,
                 unit_target: str, unit_award: str,
                 value_target: int, value_award: int,
                 cur_stat: int = 0):
        """基金项目初始化.

        :param project_name: 基金项目名称.
        :param unit_target: 计量单位(投入目标).
        :param unit_award: 计量单位(获取奖励).
        :param value_target: 数值(投入目标).
        :param value_award: 数值(获取奖励).
        :param cur_stat: 当前状态. 即项目创建时已经累积的时长.
        """
        super().__init__()
        self.project_name = project_name
        self.unit_target = unit_target
        self.unit_award = unit_award
        self.value_target = value_target
        self.value_award = value_award
        self.cur_stat = cur_stat


class TypicalGameHourFundProject(FundProject):
    """游戏时长基金项目(示例项目类型)"""
    project_type = '游戏时长基金项目(示例项目类型)'
    award = '游戏时长'
    description = '我每学习达到指定时长, 就能获得一定的游戏时间.'

    def __init__(self, project_name: str,
                 unit_target: str = '小时', unit_award: str = '小时',
                 value_target: int = 10, value_award: int = 1,
                 cur_stat: int = 0):
        """初始化"游戏时长基金项目"(示例项目类型).

        :param project_name: 基金项目名称.
        :param unit_target: 计量单位(投入目标时长). 推荐取值: {天, 小时, 分钟}
        :param unit_award: 计量单位(获取奖励时长). 推荐取值: {天, 小时, 分钟}
        :param value_target: 数值(投入目标时长).
        :param value_award: 数值(获取奖励时长).
        :param cur_stat: 当前状态. 即项目创建时已经累积的时长.
        """
        super().__init__()
        self.project_name = project_name
        self.unit_target = unit_target
        self.unit_award = unit_award
        self.value_target = value_target
        self.value_award = value_award
        self.cur_stat = cur_stat


class IncubateAward:
    """孵化中项目的预期奖励."""
    def __init__(self, award: str, description: str, necessity_level: int = 3):
        """初始化奖励.

        :param award: 奖励名称.
        :param description: 奖励描述.
        :param necessity_level: 需求性等级. 取值:{1,2,3,4,5}(由低至高)
        """
        self.award = award
        self.description = description
        self.necessity_level = necessity_level
