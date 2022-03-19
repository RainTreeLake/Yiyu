import os

def Settings(file_name):
    """导入设置"""
    settings = []
    with open(file_name, encoding="utf-8") as file:
        for setting in file:
            #导入utf-8编码的文本 并将每行文字作为列表的一个元素
            settings.append(setting.rstrip())

    #print(settings)
    return(settings)

def NewFolder(folder_path):
    """若不存在已有文件夹则新建文件夹"""
    if not os.path.exists(folder_path): 
        os.makedirs(folder_path)

def yiyu(i,path,settings,base,eggs):
    """自定义的忆雨递归算法"""
    if i == len(settings):

        answers = path.split("/")
        text = ""

        for egg in eggs:
            #定义一个布尔值判断是否应用彩蛋
            if_egg = False
            #print(egg['egg_conditions'],answers[1:])

            if len(egg['egg_conditions']) >= len(answers)-1:
                #如果彩蛋条件数量大于等于选择数量 则只要选择项都在彩蛋条件中就符合
                n = 0
                for answer in answers[1:]:
                    if answer in egg['egg_conditions']:
                        n += 1
                if n == len(answers)-1:
                    if_egg = True

            else:
                #如果彩蛋条件数量小于选择数量 则彩蛋条件都在选择项中就符合
                n = 0
                for condition in egg['egg_conditions']:
                    if condition in answers[1:]:
                        n += 1
                if n == len(egg['egg_conditions']):
                    if_egg = True

            if if_egg:
                text = egg['egg_text']

        if text == "":
            #用具体结果替换模板中的%
            data = base.split("%")

            m = 0
            while m < len(answers)-1:
                #模板与结果交替插入
                text += data[m]
                text += answers[m+1]

                m += 1
            #模板|结果|模板···模板|结果|模板 模板列表长度比结果长 因此最后添上多出的部分
            text += data[-1]

        with open(path+'/测试结果.txt','w',encoding='utf-8') as file:
            file.write(text)

        return
    #如果i和列表长度相同就结束
    question = settings[i].split(" ")[0]
    choices = settings[i].split(" ")
    del(choices[0])
    #获取到当前的问题以及选项
    with open(path + "/" + question + '.txt','w') as file:
        pass
    for choice in choices:
        new_path = path + "/" + choice
        NewFolder(new_path)
        new_i = i + 1
        #增加i的值和路径 递归套娃
        yiyu(new_i,new_path,settings,base,eggs)

def main(settings_file,base_file,egg_files):
    """主程序"""
    #导入模板
    with open(base_file,encoding="utf-8") as file:
        base = file.read()

    #导入彩蛋
    eggs = []
    for egg_file in egg_files:
        #遍历存放彩蛋的文本文件
        with open(egg_file,encoding="utf-8") as file:
            #第一行存放彩蛋的触发条件 用空格间隔 用|与之后的彩蛋内容分割
            data = file.read().split("|")
        egg_conditions = data[0].rstrip().split(" ")
        egg_text = data[1]
        #eggs是包含所有彩蛋的列表 其中每一个元素都是一个字典 包含条件和内容两个键与值
        eggs.append({'egg_conditions':egg_conditions,'egg_text':egg_text})

    #导入问题答案的设置
    settings = Settings(settings_file)
    path = settings[0]
    NewFolder(path)
    i = 1
    yiyu(i,path,settings,base,eggs)

main("Settings.txt","Base.txt",["Egg1.txt"])

