# coding=utf-8
import ConfigParser

MyConfigParser = ConfigParser.ConfigParser()
MyConfigParser.read("/var/www/ShopKeeper/conf.ini")


## TODO
# MyConfigParser.read(绝对路径)

def scanConfig():
    ret = []
    for section in MyConfigParser.sections():
        for option in MyConfigParser.options(section):
            dic = {'value': MyConfigParser.get(section, option),
                   'option': option,
                   'sectionAoption': "&".join([section, option]),}
            ret.append(dic)
    return ret


def alertConfig(dic):
    for i in dic.items():
        sAo = i[0].split("&")
        print sAo
        section = sAo[0]
        option = sAo[1]
        value = i[1]
        MyConfigParser.set(section, option, value)

    MyConfigParser.write(open("/var/www/ShopKeeper/conf.ini", "w"))

    pass
