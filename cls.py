# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2023-08-12
# @file    : cls.py
# @function:

import os.path
import pickle

from utils import SAVE_DIR, PROJECTS_PICKLE_FILENAME, INCUBATE_PICKLE_FILENAME, AWARD_REPO_PICKLE_FILENAME


class ManagerInitializer:
    prog = 'aifm.py'  # 程序名
    # usage = ''  # 程序使用方式
    description = """
    “AIFM(Achievement Inventive Fund Manager, 成就激励基金管理器)”是一个基金项目管理和跟踪工具.\n
    用户可以创建独特的基金项目. 对每个项目, 用户可以自行决定达成目标后的奖励, 自由设定达成目标所需的工作量和奖励的多少, 并设置相应的计数单位.\n
    例如, 用户可以创建这样的一个基金项目: “我每学习100小时, 就可以为购买游戏储值50元.”\n在这个项目中, 
    达成目标所需的工作量为100, 其单位为小时; 奖励的数值为50, 其单位为元.\n
    同时, 用户可以对创建的每个基金项目进行跟踪, 包括查看, 更新以及删除指定的项目.\n
    需要注意的是, AIFM的工作仍依赖于用户自身的自觉性, 其存在意义只是为用户增加成就感并给予鼓励."""
    epilog = f'本地存档保存在{SAVE_DIR}目录下的{PROJECTS_PICKLE_FILENAME}文件中.'  # 程序额外说明

    def __init__(self):
        self._check_savefile()

    def _check_savefile(self):
        projects_filepath = os.path.join(SAVE_DIR, PROJECTS_PICKLE_FILENAME)
        award_incubate_filepath = os.path.join(SAVE_DIR, INCUBATE_PICKLE_FILENAME)
        award_repo_filepath = os.path.join(SAVE_DIR, AWARD_REPO_PICKLE_FILENAME)
        if not os.path.exists(projects_filepath):  # 未找到存档文件, 则创建新的空白存档文件
            with open(projects_filepath, 'wb') as f:
                pickle.dump(list(), f)
            print(f'> 已创建空白项目存档文件: {projects_filepath}')
        if not os.path.exists(award_incubate_filepath):
            with open(award_incubate_filepath, 'wb') as f:
                pickle.dump(list(), f)
            print(f'> 已创建空白预期奖励存储文件: {award_incubate_filepath}')
        if not os.path.exists(award_repo_filepath):
            with open(award_repo_filepath, 'wb') as f:
                pickle.dump(list(), f)
            print(f'> 已创建空白奖励仓库存储文件: {award_repo_filepath}')


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
                 value_target: float, value_award: float,
                 cur_stat: float = 0.0):
        """基金项目初始化.

        :param project_name: 基金项目名称.
        :param unit_target: 计量单位(投入目标).
        :param unit_award: 计量单位(获取奖励).
        :param value_target: 数值(投入目标).
        :param value_award: 数值(获取奖励).
        :param cur_stat: 当前状态. 即项目创建时已经累积的单位.
        """
        super().__init__()
        self.project_name = project_name
        self.unit_target = unit_target
        self.unit_award = unit_award
        self.value_target = value_target
        self.value_award = value_award
        self.cur_stat = cur_stat
        self.complete_cnt = 0  # 项目累计完成轮数
        self.last_update_time = '无'  # 上次更新项目进度的时间


class TypicalGameHourFundProject(FundProject):
    """游戏时长基金项目(示例项目类型)"""
    project_type = '游戏时长基金项目'
    award = '游戏时长'
    description = '我每学习达到指定时长, 就能获得一定的游戏时间.'

    def __init__(self, project_name: str,
                 unit_target: str = '小时', unit_award: str = '小时',
                 value_target: float = 10.0, value_award: float = 1.0,
                 cur_stat: float = 0.0):
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
        self.complete_cnt = 0
        self.last_update_time = '无'

    def show_model_class(self):
        print(f'\n游戏时长基金项目(示例项目类型)({self.__class__})属性信息如下: ')
        print(f'{self.project_type=}\n{self.project_name=}\n{self.award=}\n{self.description=}\n'
              f'{self.value_target=}\n{self.unit_target=}\n{self.value_award=}\n{self.unit_award=}\n'
              f'{self.cur_stat=}\n{self.complete_cnt=}\n{self.last_update_time=}\n')


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
        # TODO: add more attributes


class AwardRepository:
    """奖励存储库"""
    def __init__(self, award: str, value_award: float, unit_award: str):
        """初始化一种奖励的存储库.

        :param award: 奖励名称.
        :param value_award: 奖励在当前仓库存存量.
        :param unit_award: 奖励的单位.
        """
        self.award = award
        self.value_award = value_award
        self.unit_award = unit_award
        self.last_change_time = ''  # 最近变动时间
