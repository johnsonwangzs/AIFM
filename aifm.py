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
    parser.add_argument('-l', '--list', action='store_true', required=False, help='列出当前进行中的所有基金项目')
    parser.add_argument('-c', '--clear', action='store_true', required=False, help='清除所有基金项目')
    parser.add_argument('-b', '--build', action='store_true', required=False, help='创建新的基金项目')
    parser.add_argument('-ia', '--add_incubate', action='store_true', required=False, help='添加新的孵化中项目的预期奖励')
    parser.add_argument('-il', '--list_incubate', action='store_true', required=False, help='列出孵化中项目的预期奖励')
    parser.add_argument('-d', '--delete', action='store_true', required=False, help='删除指定基金项目')
    print('\n欢迎使用“成就激励基金”管理器. 使用参数[-h]来查看帮助信息.')
    # 从命令行中解析参数
    args = parser.parse_args()
    print(f'{args = }')

    if args.clear is True:
        while True:
            op = input('\n确认要清除所有基金项目吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.clear_all_projects()
                print('> 已清除所有基金项目.')
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.list is True:
        operation.list_all_projects()

    if args.build is True:
        project_type_id = eval(input('\n请选择要创建的基金项目类型:\n 1.自定义基金项目\n 2.游戏时长基金项目(示例项目类型)\n'))
        if project_type_id == 2:
            project_name = input('请输入基金项目名称: ')
            operation.build_new_project('游戏时长基金项目(示例项目类型)', project_name)
            print('> 新基金项目创建完毕, 已保存至本地.')
        elif project_type_id == 1:
            project_name = input('请输入基金项目名称: ')
            project_info = dict()
            project_info['description'] = input('请输入项目描述: ')
            project_info['award'] = input('请输入最终奖励: ')
            project_info['unit_target'] = input('请输入投入目标的计量单位: ')
            project_info['unit_award'] = input('请输入最终奖励的计量单位: ')
            project_info['value_target'] = input('请输入投入目标的数值: ')
            project_info['value_award'] = input('请输入最终奖励的数值: ')
            project_info['cur_stat'] = eval(input('请输入当前状态: '))
            operation.build_new_project('自定义基金项目', project_name, **project_info)
            print('> 新基金项目创建完毕, 已保存至本地.')
        else:
            print('非法输入.')

    if args.delete is True:
        operation.list_all_projects()
        del_id = eval(input('\n请输入要删除的项目id: '))
        while True:
            op = input('确认要删除该基金项目吗? [Y/N]: ')
            if (op == 'Y') or (op == 'y'):
                operation.delete_project(del_id)
                print('> 项目已删除!')
                operation.list_all_projects()
                break
            elif (op == 'N') or (op == 'n'):
                print('无操作.')
                break

    if args.add_incubate is True:
        award = input('\n请输入新的孵化中项目的预期奖励名称: ')
        description = input('请输入奖励描述: ')
        necessity_level = eval(input('请输入需求性等级. 取值{1,2,3,4,5}(由低至高): '))
        operation.add_incubate_award(award, description, necessity_level)
        print('> 预期奖励已录入.')

    if args.list_incubate is True:
        operation.list_incubate_award()
