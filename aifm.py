# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2023-08-12
# @file    : aifm.py
# @function:

import argparse
from cls import ManagerInitializer
import operation

if __name__ == '__main__':
    md = ManagerInitializer()
    # 定义命令行解析器对象
    parser = argparse.ArgumentParser(description=md.description,
                                     prog=md.prog,
                                     epilog=md.epilog)
    # 添加命令行参数
    parser.add_argument('-l', '--list', action='store_true', required=False, help='列出当前进行中的所有基金项目(简略)')
    parser.add_argument('-ll', '--list_detail', action='store_true', required=False, help='列出当前进行中的所有基金项目(详细信息)')
    parser.add_argument('-c', '--clear', action='store_true', required=False, help='清除所有基金项目')
    parser.add_argument('-b', '--build', action='store_true', required=False, help='创建新的基金项目')
    parser.add_argument('-d', '--delete', action='store_true', required=False, help='删除指定基金项目')
    parser.add_argument('-u', '--update', action='store_true', required=False, help='更新指定基金项目的进度状态')
    parser.add_argument('-m', '--model', action='store_true', required=False, help='查看内置基金项目类型属性信息')
    parser.add_argument('-ia', '--add_incubate', action='store_true', required=False, help='添加新的孵化中项目的预期奖励')
    parser.add_argument('-il', '--list_incubate', action='store_true', required=False, help='列出孵化中项目的预期奖励')
    parser.add_argument('-id', '--delete_incubate', action='store_true', required=False, help='删除指定孵化中项目的预期奖励')
    parser.add_argument('-ic', '--clear_incubate', action='store_true', required=False, help='清除所有孵化中项目的预期奖励')
    parser.add_argument('-rl', '--list_award_repo', action='store_true', required=False, help='列出奖励仓库')
    parser.add_argument('-rw', '--withdraw_repo', action='store_true', required=False, help='从奖励仓库中取出指定数量的奖励')
    parser.add_argument('-rd', '--delete_repo', action='store_true', required=False, help='删除指定的奖励仓库')
    parser.add_argument('-rc', '--clear_repo', action='store_true', required=False, help='清除所有奖励仓库')
    parser.add_argument('-cc', '--clear_all', action='store_true', required=False, help='清除所有存档和存储文件(完全初始化)')
    print('\n欢迎使用“成就激励基金”管理器. 使用参数[-h]来查看帮助信息.')
    # 从命令行中解析参数
    args = parser.parse_args()
    # print(f'{args = }')

    if args.clear is True:
        while True:
            op = input('\n确认要清除所有基金项目吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.clear_all_projects()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.list is True:
        operation.list_all_projects()

    if args.list_detail is True:
        operation.list_all_projects_detail()

    if args.build is True:
        project_type_id = eval(input('\n请选择要创建的基金项目类型:\n 1.自定义基金项目\n 2.游戏时长基金项目(示例项目类型)\n'))
        if project_type_id == 2:
            project_name = input('请输入基金项目名称: ')
            operation.build_new_project('游戏时长基金项目', project_name)
        elif project_type_id == 1:
            project_name = input('请输入基金项目名称: ')
            project_info = dict()
            project_info['description'] = input('请输入项目描述: ')
            project_info['award'] = input('请输入最终奖励: ')
            project_info['unit_target'] = input('请输入投入目标的计量单位: ')
            project_info['unit_award'] = input('请输入最终奖励的计量单位: ')
            project_info['value_target'] = float(eval(input('请输入投入目标的数值: ')))
            project_info['value_award'] = float(eval(input('请输入最终奖励的数值: ')))
            project_info['cur_stat'] = float(eval(input('请输入当前状态: ')))
            operation.build_new_project('自定义基金项目', project_name, **project_info)
            operation.list_all_projects()
        else:
            print('非法输入.')

    if args.delete is True:
        operation.list_all_projects()
        del_id = eval(input('\n请输入要删除的项目id: '))
        while True:
            op = input('确认要删除该基金项目吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.delete_project(del_id)
                operation.list_all_projects()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.update is True:
        projects_cnt = operation.list_all_projects()
        if projects_cnt != 0:
            update_id = eval(input('\n请输入要更新的项目id: '))
            value_add = eval(input('请输入项目进度状态的新增数值: '))
            flag_repo_change = operation.update_project_stat(update_id, value_add)
            operation.list_all_projects()
            if flag_repo_change:
                operation.list_award_repo()

    if args.model is True:
        operation.list_all_project_models()

    if args.add_incubate is True:
        award = input('\n请输入新的孵化中项目的预期奖励名称: ')
        description = input('请输入奖励描述: ')
        necessity_level = eval(input('请输入需求性等级. 取值{1,2,3,4,5}(由低至高): '))
        operation.add_incubate_award(award, description, necessity_level)
        operation.list_incubate_award()

    if args.list_incubate is True:
        operation.list_incubate_award()

    if args.delete_incubate is True:
        operation.list_incubate_award()
        del_id = eval(input('\n请输入要删除的预期奖励id: '))
        while True:
            op = input('确认要删除该预期奖励吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.delete_incubate_award(del_id)
                operation.list_incubate_award()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.clear_incubate is True:
        while True:
            op = input('\n确认要清除所有孵化中项目的预期奖励吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.clear_all_incubate_awards()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.list_award_repo is True:
        operation.list_award_repo()

    if args.withdraw_repo is True:
        operation.list_award_repo()
        repo_id = eval(input('\n请输入取出奖励的仓库id: '))
        value_withdraw = eval(input('请输入取出奖励的数值: '))
        flag_success_withdraw = operation.withdraw_award_in_repo(repo_id, value_withdraw)
        if flag_success_withdraw:
            operation.list_award_repo()

    if args.delete_repo is True:
        operation.list_award_repo()
        del_id = eval(input('\n请输入要删除的奖励仓库id: '))
        while True:
            op = input('确认要删除该奖励仓库吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.delete_award_repo(del_id)
                operation.list_award_repo()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.clear_repo is True:
        while True:
            op = input('确认要清空所有奖励仓库吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.clear_all_award_repo()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.clear_all is True:
        while True:
            op = input('确认要清除所有存档和存储文件吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.clear_all_projects()
                operation.clear_all_incubate_awards()
                operation.clear_all_award_repo()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break
