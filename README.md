# AIFM - 成就激励基金管理器

## Introduction

“AIFM(Achievement Inventive Fund Manager, 成就激励基金管理器)”是一个基金项目管理和跟踪工具. 

用户可以创建独特的基金项目. 对每个项目, 用户可以自行决定达成目标后的奖励, 自由设定达成目标所需的工作量和奖励的多少, 并设置相应的计数单位.

例如, 用户可以创建这样的一个基金项目: “我每学习100小时, 就可以为购买游戏储值50元.”

- 达成目标所需的工作量为100, 其单位为小时.
- 奖励的数值为50, 其单位为元.

同时, 用户可以对创建的每个基金项目进行跟踪, 包括查看, 更新以及删除指定的项目.

需要注意的是, AIFM的工作仍依赖于用户自身的自觉性, 其存在意义只是为用户增加成就感并给予鼓励.

## Usage

### CMD Command

```bash
python aifm.py [-h] [-l] [-ll] [-c] [-b] [-d] [-u] [-ia] [-il]
```

### Optional Arguments

```bash
-h, --help            show this help message and exit
-l, --list            列出当前进行中的所有基金项目(简略)
-ll, --list_detail    列出当前进行中的所有基金项目(详细信息)
-c, --clear           清除所有基金项目
-b, --build           创建新的基金项目
-d, --delete          删除指定基金项目
-u, --update          更新指定基金项目的进度状态
-ia, --add_incubate   添加新的孵化中项目的预期奖励
-il, --list_incubate  列出孵化中项目的预期奖励
```

