# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2023-08-13
# @file    : operation.py
# @function:

import os.path
from utils import SAVE_DIR, PROJECTS_PICKLE_FILENAME, INCUBATE_PICKLE_FILENAME
from cls import TypicalGameHourFundProject, SelfDefinedFundProject, IncubateAward
import pickle
from tabulate import tabulate

projects_filepath = os.path.join(SAVE_DIR, PROJECTS_PICKLE_FILENAME)
incubate_filepath = os.path.join(SAVE_DIR, INCUBATE_PICKLE_FILENAME)


def clear_all_projects():
    """清除所有项目(删除项目存档文件)."""
    global projects_filepath
    os.remove(projects_filepath)
    print('> 已清除所有基金项目.')


def _read_savefile_projects() -> list:
    """读取存档文件, 返回基金项目列表."""
    global projects_filepath
    with open(projects_filepath, 'rb') as f:
        projects_list = []
        try:
            projects_list = pickle.load(f)
        except EOFError:
            print(f'\n错误! 存档文件为空, 请手动删除存档文件{projects_filepath}后再试.')
    return projects_list


def _read_savefile_incubate() -> list:
    """读取存储文件, 返回孵化中项目的预期奖励列表."""
    global incubate_filepath
    with open(incubate_filepath, 'rb') as f:
        incubate_list = []
        try:
            incubate_list = pickle.load(f)
        except EOFError:
            print(f'\n错误! 存储文件为空, 请手动删除存储文件{incubate_filepath}后再试.')
    return incubate_list


def list_all_projects():
    """列出所有基金项目."""
    projects_list = _read_savefile_projects()
    if len(projects_list) == 0:
        print('\n暂无基金项目.\n提示: 使用参数[-b]来添加一个新的基金项目.')
        return
    print(f'\n目前共有{len(projects_list)}个基金项目:')
    table_output = list()
    for (project_id, project_object) in enumerate(projects_list):  # 列出所有项目
        project_type = project_object.project_type
        project_name = project_object.project_name
        unit_target = project_object.unit_target
        unit_award = project_object.unit_award
        value_target = project_object.value_target
        value_award = project_object.value_award
        cur_stat = project_object.cur_stat
        s1 = f'{value_target}({unit_target}) => {value_award}({unit_award})'
        s2 = f'{cur_stat}/{value_target}'
        table_output.append([project_id + 1, project_name, project_type,
                             s1, s2])
    headers = ['项目id', '项目名称', '项目类型', '成就达成方式', '当前完成度']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))


def list_all_projects_detail():
    """列出所有基金项目(详细信息)."""
    projects_list = _read_savefile_projects()
    if len(projects_list) == 0:
        print('\n暂无基金项目.\n提示: 使用参数[-b]来添加一个新的基金项目.')
        return
    print(f'\n目前共有{len(projects_list)}个基金项目:')
    table_output = list()
    for (project_id, project_object) in enumerate(projects_list):  # 列出所有项目
        project_type = project_object.project_type
        project_name = project_object.project_name
        description = project_object.description
        unit_target = project_object.unit_target
        unit_award = project_object.unit_award
        value_target = project_object.value_target
        value_award = project_object.value_award
        cur_stat = project_object.cur_stat
        complete_cnt = project_object.complete_cnt
        s1 = f'{value_target}({unit_target}) => {value_award}({unit_award})'
        s2 = f'{cur_stat}/{value_target}'
        table_output.append([project_id + 1, project_name, project_type,
                             s1, s2, complete_cnt, description])
    headers = ['项目id', '项目名称', '项目类型', '成就达成方式', '当前完成度', '累计完成轮数', '项目描述']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))


def build_new_project(project_type: str, project_name: str, **kwargs):
    """创建新的基金项目.

    :param project_type: 基金项目类型.
    :param project_name: 基金项目名称.
    :param kwargs: 自定义项目类型时, 其他的构造属性.
    """
    if project_type == '游戏时长基金项目':
        new_project = TypicalGameHourFundProject(project_name=project_name)
    else:
        new_project = SelfDefinedFundProject(project_name=project_name,
                                             unit_target=kwargs['unit_target'], unit_award=kwargs['unit_award'],
                                             value_target=kwargs['value_target'], value_award=kwargs['value_award'],
                                             cur_stat=kwargs['cur_stat'])
        new_project.award = kwargs['award']
        new_project.description = kwargs['description']

    projects_list = _read_savefile_projects()
    projects_list.append(new_project)

    global projects_filepath
    with open(projects_filepath, 'wb') as f:
        pickle.dump(projects_list, f)
    print('> 新基金项目创建完毕, 已保存至本地.')


def delete_project(project_id: int):
    """删除指定的基金项目.

    :param project_id: 项目id.
    """
    project_list = _read_savefile_projects()
    try:
        del project_list[project_id - 1]
    except IndexError:
        print('\n错误! 输入的项目序号不存在.')
    global projects_filepath
    with open(projects_filepath, 'wb') as f:
        pickle.dump(project_list, f)
    print('> 项目已删除!')


def update_project_stat(project_id: int, value_add: float = 0.0):
    """更新指定基金项目的进度状态.

    :param project_id: 项目id.
    :param value_add: 状态的新增值.
    """
    project_list = _read_savefile_projects()
    try:
        cur_stat = project_list[project_id - 1].cur_stat
        cur_stat += value_add
        # 检查是否达到目标
        value_target = project_list[project_id - 1].value_target
        while cur_stat >= value_target:
            cur_stat -= value_target
            project_list[project_id - 1].complete_cnt += 1
        project_list[project_id - 1].cur_stat = cur_stat
    except IndexError:
        print('\n错误! 输入的项目序号不存在.')

    global projects_filepath
    with open(projects_filepath, 'wb') as f:
        pickle.dump(project_list, f)
    print('> 项目进度状态已变更.')


def add_incubate_award(award: str, description: str, necessity_level: int):
    """添加新的孵化中项目的预期奖励.

    :param award: 奖励名称.
    :param description: 奖励描述.
    :param necessity_level: 需求性等级. 取值:{1,2,3,4,5}(由低至高)
    :return:
    """
    ia = IncubateAward(award, description, necessity_level)
    incubate_list = _read_savefile_incubate()
    incubate_list.append(ia)

    global incubate_filepath
    with open(incubate_filepath, 'wb') as f:
        pickle.dump(incubate_list, f)
    print('> 预期奖励已录入.')


def list_incubate_award():
    """列出孵化中项目的预期奖励."""
    incubate_list = _read_savefile_incubate()
    if len(incubate_list) == 0:
        print('\n暂无预期奖励.\n提示: 使用参数[-ia]来添加一个新的孵化中项目的预期奖励.')
        return
    print(f'\n目前共有{len(incubate_list)}个预期奖励:')
    table_output = list()
    for (incubate_id, incubate_project) in enumerate(incubate_list):
        award = incubate_project.award
        description = incubate_project.description
        necessity_level = incubate_project.necessity_level
        table_output.append([incubate_id + 1, award, description, necessity_level])
    headers = ['奖励id', '奖励名称', '描述', '需求性等级']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))
