# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2023-08-13
# @file    : operation.py
# @function:
from datetime import datetime
import os.path
from utils import SAVE_DIR, PROJECTS_PICKLE_FILENAME, INCUBATE_PICKLE_FILENAME, AWARD_REPO_PICKLE_FILENAME
from cls import TypicalGameHourFundProject, SelfDefinedFundProject, IncubateAward, AwardRepository
import pickle
from tabulate import tabulate

projects_filepath = os.path.join(SAVE_DIR, PROJECTS_PICKLE_FILENAME)
award_incubate_filepath = os.path.join(SAVE_DIR, INCUBATE_PICKLE_FILENAME)
award_repo_filepath = os.path.join(SAVE_DIR, AWARD_REPO_PICKLE_FILENAME)


def clear_all_projects():
    """清除所有项目(删除项目存档文件)."""
    global projects_filepath
    os.remove(projects_filepath)
    print('> 已清除所有基金项目.')


def _read_savefile_projects() -> list:
    """读取存档文件, 返回基金项目列表.

    :return: 基金项目列表
    """
    global projects_filepath
    with open(projects_filepath, 'rb') as f:
        projects_list = list()
        try:
            projects_list = pickle.load(f)
        except EOFError:
            print(f'\n错误! 存档文件为空, 请手动删除存档文件{projects_filepath}后再试.')
    return projects_list


def _read_savefile_incubate() -> list:
    """读取存储文件, 返回孵化中项目的预期奖励列表.

    :return: 预期奖励列表
    """
    global award_incubate_filepath
    with open(award_incubate_filepath, 'rb') as f:
        incubate_list = list()
        try:
            incubate_list = pickle.load(f)
        except EOFError:
            print(f'\n错误! 存储文件为空, 请手动删除存储文件{award_incubate_filepath}后再试.')
    return incubate_list


def _read_savefile_repo() -> list:
    """读取存储文件, 返回奖励仓库列表.

    :return: 仓库列表
    """
    global award_repo_filepath
    with open(award_repo_filepath, 'rb') as f:
        repo_list = list()
        try:
            repo_list = pickle.load(f)
        except EOFError:
            print(f'\n错误! 存储文件为空, 请手动删除存储文件{award_repo_filepath}后再试.')
    return repo_list


def list_all_projects() -> int:
    """列出所有基金项目.

    :return: 基金项目列表的长度
    """
    projects_list = _read_savefile_projects()
    if len(projects_list) == 0:
        print('\n暂无基金项目.\n提示: 使用参数[-b]来添加一个新的基金项目.')
        return len(projects_list)
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
        complete_cnt = project_object.complete_cnt
        s1 = f'{value_target}({unit_target}) => {value_award}({unit_award})'
        s2 = f'{cur_stat}/{value_target}'
        table_output.append([project_id + 1, project_name, project_type,
                             s1, s2, complete_cnt])
    headers = ['项目id', '项目名称', '项目类型', '成就达成方式', '当前完成度', '累计完成轮数']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))
    return len(projects_list)


def list_all_projects_detail() -> int:
    """列出所有基金项目(详细信息).

    :return: 基金项目列表的长度
    """
    projects_list = _read_savefile_projects()
    if len(projects_list) == 0:
        print('\n暂无基金项目.\n提示: 使用参数[-b]来添加一个新的基金项目.')
        return len(projects_list)
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
        init_time = project_object.init_time
        last_update = project_object.last_update_time
        table_output.append([project_id + 1, project_name, project_type,
                             s1, s2, complete_cnt, init_time, last_update, description])
    headers = ['项目id', '项目名称', '项目类型', '成就达成方式', '当前完成度', '累计完成轮数', '项目创建时间', '最近修改进度时间', '项目描述']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))
    return len(projects_list)


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
    new_project.init_time = str(datetime.now())

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
        global projects_filepath
        with open(projects_filepath, 'wb') as f:
            pickle.dump(project_list, f)
        print('> 项目已删除!')
    except IndexError:
        print('\n错误! 输入的项目序号不存在.')


def update_project_stat(project_id: int, value_add: float = 0.0) -> bool:
    """更新指定基金项目的进度状态.

    :param project_id: 项目id.
    :param value_add: 状态的新增值.
    :return: 取出操作是否成功
    """
    project_list = _read_savefile_projects()
    try:
        cur_stat = project_list[project_id - 1].cur_stat
        cur_stat += value_add

        # 检查是否达到目标
        value_target = project_list[project_id - 1].value_target
        value_award_add = 0.0
        while cur_stat >= value_target:
            cur_stat -= value_target
            project_list[project_id - 1].complete_cnt += 1
            value_award_add += project_list[project_id - 1].value_award
        project_list[project_id - 1].cur_stat = cur_stat
        time_now = str(datetime.now())
        project_list[project_id - 1].last_update_time = time_now
        award = project_list[project_id - 1].award
        flag_repo_change = update_award_repo(award, value_award_add, project_list[project_id - 1].unit_award, time_now)  # 更新奖励仓库

        global projects_filepath
        with open(projects_filepath, 'wb') as f:
            pickle.dump(project_list, f)
        print('> 项目进度状态已变更.')

        if flag_repo_change is True:
            return True

    except (IndexError, TypeError):
        print('\n错误! 输入的项目序号不存在.')

    return False


def update_award_repo(award: str, value_award_add: float, unit_award: str, time_now: str) -> bool:
    """更新奖励仓库.

    :param award: 奖励名称.
    :param value_award_add: 奖励数值.
    :param unit_award: 奖励的单位.
    :param time_now: 仓库发生变动的时间.
    :return: 取出操作是否成功
    """
    if value_award_add == 0.0:  # 若数值为0, 则不用更新
        return False

    repo_list = _read_savefile_repo()

    if len(repo_list) != 0:
        for repo in repo_list:  # 依次遍历列表中的每个仓库, 查找是否有同类奖励的
            if repo.award == award:
                repo.value_award += value_award_add
                repo.last_change_time = time_now
                break
    else:   # 检查存储文件为空(不存在仓库), 或者不存在同类奖励仓库
        new_repo = _create_award_repo(award, unit_award)
        new_repo.value_award += value_award_add
        new_repo.last_change_time = time_now
        repo_list.append(new_repo)

    global award_repo_filepath
    with open(award_repo_filepath, 'wb') as f:
        pickle.dump(repo_list, f)
        print('> 已更新奖励仓库.')
    return True


def _create_award_repo(award: str, unit_award: str) -> AwardRepository:
    """创建新的奖励仓库.

    :param award: 奖励名称.
    :param unit_award: 奖励的单位.
    """
    new_repo = AwardRepository(award, 0.0, unit_award)
    print('> 已创建新奖励仓库.')
    return new_repo


def list_all_project_models():
    """展示内置基金项目类型属性信息."""
    # TypicalGameHourFundProject Class
    tghfp = TypicalGameHourFundProject('示例项目')
    TypicalGameHourFundProject.show_model_class(tghfp)


def add_incubate_award(award: str, description: str, necessity_level: int):
    """添加新的孵化中项目的预期奖励.

    :param award: 奖励名称.
    :param description: 奖励描述.
    :param necessity_level: 需求性等级. 取值:{1,2,3,4,5}(由低至高)
    """
    ia = IncubateAward(award, description, necessity_level)
    incubate_list = _read_savefile_incubate()
    incubate_list.append(ia)

    global award_incubate_filepath
    with open(award_incubate_filepath, 'wb') as f:
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
    for (incubate_id, incubate_object) in enumerate(incubate_list):
        award = incubate_object.award
        description = incubate_object.description
        necessity_level = incubate_object.necessity_level
        table_output.append([incubate_id + 1, award, description, necessity_level])
    headers = ['奖励id', '奖励名称', '描述', '需求性等级']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))


def delete_incubate_award(award_id: int):
    """删除指定孵化中项目的预期奖励.

    :param award_id: 预期奖励的id
    """
    incubate_list = _read_savefile_incubate()
    try:
        del incubate_list[award_id - 1]
        global award_incubate_filepath
        with open(award_incubate_filepath, 'wb') as f:
            pickle.dump(incubate_list, f)
        print('> 预期奖励已删除!')
    except IndexError:
        print('\n错误! 输入的预期奖励序号不存在.')


def clear_all_incubate_awards():
    """删除所有孵化中项目的预期奖励."""
    global award_incubate_filepath
    os.remove(award_incubate_filepath)
    print('> 已清除所有孵化中项目的预期奖励.')


def list_award_repo():
    """列出所有奖励仓库."""
    repo_list = _read_savefile_repo()
    if len(repo_list) == 0:
        print('\n暂无已获得奖励.')
        return
    print(f'\n目前共有{len(repo_list)}个奖励仓库:')
    table_output = list()
    for (repo_id, repo_object) in enumerate(repo_list):
        award = repo_object.award
        value_award = repo_object.value_award
        unit_award = repo_object.unit_award
        last_change_time = repo_object.last_change_time
        table_output.append([repo_id + 1, award, value_award, unit_award, last_change_time])
    headers = ['奖励id', '奖励名称', '当前仓库存量', '计量单位', '最近变动时间']
    print(tabulate(table_output, headers=headers, stralign='center', tablefmt='grid'))


def withdraw_award_in_repo(repo_id: int, value_withdraw: float) -> bool:
    """从奖励仓库中取出指定数量的奖励.

    :param repo_id: 仓库id.
    :param value_withdraw: 要取出的奖励数量.
    :return: 取出操作是否成功
    """
    repo_list = _read_savefile_repo()
    try:
        if value_withdraw > repo_list[repo_id - 1].value_award:
            print('\n取出奖励失败. 原因: 库存数量不足.')
            return False
        if value_withdraw <= 0.0:
            print('\n取出奖励失败. 原因: 取出数值应大于0.')
            return False

        repo_list[repo_id - 1].value_award -= value_withdraw
        repo_list[repo_id - 1].last_change_time = str(datetime.now())

        global award_repo_filepath
        with open(award_repo_filepath, 'wb') as f:
            pickle.dump(repo_list, f)
            print('> 奖励已取出. 已更新奖励仓库.')
        return True

    except IndexError:
        print('\n错误! 输入的仓库序号不存在.')
    # except TypeError:
        # print('\n错误! 非法输入.')
    return False


def delete_award_repo(repo_id: int):
    """删除指定孵化中项目的预期奖励.

    :param repo_id: 预期奖励的id
    """
    repo_list = _read_savefile_incubate()
    try:
        del repo_list[repo_id - 1]
        global award_repo_filepath
        with open(award_repo_filepath, 'wb') as f:
            pickle.dump(repo_list, f)
        print('> 奖励仓库已删除!')
    except IndexError:
        print('\n错误! 输入的奖励仓库序号不存在.')


def clear_all_award_repo():
    """清除所有奖励仓库(删除奖励仓库存储文件)."""
    global award_repo_filepath
    os.remove(award_repo_filepath)
    print('> 已清除所有奖励仓库.')
