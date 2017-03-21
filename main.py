# -*- coding: utf-8 -*-  
# author: chengshuai
import sys
import ConfigParser

def LOG(color,content):
    code = "31;40"
    if color == "warn":
        code = "33;40"
    elif color == "info":
        code = "32;40"
    print "\033[1;%sm%s\033[0m" %(code,content)

class ReadConfFile(object):
    config = None
    def __init__(self, file="./house.conf"):
        self.config = ConfigParser.SafeConfigParser()
        self.config.readfp(open(file))
    def read_option(self, group, name):
        return self.config.get(group, name)
    def get_options(self,group):
        return self.config.options(group)

class Fang(object):
    def __init__(self,soutao,total,old,evaluate_ratio,_2year,_5and1,location,size,rongji):
        self.soutao = soutao
        self.total = total
        self.old = old
        self._2year = _2year
        self._5and1 = _5and1
        self.location = location
        self.size = size
        self.rongji = rongji
        self.evaluate_ratio = evaluate_ratio
        #self.wangqian = self.calculate_wangqian()
        self.wangqian = total*evaluate_ratio

    def _is_putong(self):
        if self.rongji < 1.0:
            return False
        if self.size > 140:
            return False
        else:
            if self.location < 5.0:
                #if self.wangqian > 468*1.2:
                if self.wangqian > 468:
                    return False
            elif self.location > 5.0 and self.location < 6.0:
                #if self.wangqian > 374*1.2:
                if self.wangqian > 374:
                    return False
            elif self.location > 6.0:
                #if self.wangqian > 281*1.2:
                if self.wangqian > 281:
                    return False
        return True

    def qieshui(self):
        price = 0.00
        zengzhishui = self.zengzhishui()
        if self.size > 90:
            price = (self.wangqian-zengzhishui)*0.015
        else:
            price = (self.wangqian-zengzhishui)*0.01
        return price

    def fangdai(self):
        price = 0.00
        if self._is_putong():
            if self.soutao:
                price = self.wangqian*0.65
            else:
                price = self.wangqian*0.4
        else:
            if self.soutao:
                price = self.wangqian*0.60
            else:
                price = self.wangqian*0.2
        return price

    def geshui(self):
        price = 0.00
        if self._5and1:
            price = 0.00
        else:
            price = (self.wangqian-self.old)*0.20
        return price

    def zengzhishui(self):
        price = 0.00
        if self._is_putong():
            price = 0.00
        else:
            if _2year:
                price = ((self.wangqian-self.old)/1.05)*0.056
            else:
                price = (self.wangqian/1.05)*0.056
        return price

    def fuwufei(self):
        price = self.total * 0.027
        return price

    def shoufu(self):
        price = self.total - self.fangdai()
        return price

    def get_soufu_total(self):
        price = self.fuwufei()+self.geshui()+self.zengzhishui()+self.qieshui()+self.shoufu()
        return price
        

    def money(self):
        LOG("error","--------- 核算 ----------")
        LOG("info","折旧比: %.2f" %self.evaluate_ratio)
        if not self._is_putong():
            LOG("info","个人税: %.2f" %self.geshui())
            LOG("info","增值税: %.2f" %self.zengzhishui())
        LOG("info","房契税: %.2f" %self.qieshui())
        LOG("info","服务费: %.2f" %self.fuwufei())
        LOG("info","首付钱: %.2f" %self.shoufu())

        if self._is_putong():
            LOG("warn","普住房: 是")
        else:
            LOG("warn","普住房: 不是")
        LOG("warn","首付钱: %.2f" %(self.get_soufu_total()))
        LOG("warn","贷款钱: %.2f" %self.fangdai())

if __name__ == '__main__':
    conf = ReadConfFile()
    soutao = int(conf.read_option('default','FANG_SOUTAO'))
    total = float(conf.read_option('default','FANG_TOTAL'))
    old = float(conf.read_option('default','FANG_OLD'))
    evaluate_ratio = float(conf.read_option('default','FANG_EVALUATE_RATIO'))
    _2year = int(conf.read_option('default','FANG_2YEAR'))
    _5and1 = int(conf.read_option('default','FANG_5and1'))
    location = float(conf.read_option('default','FANG_LOCATION'))
    size = float(conf.read_option('default','FANG_SIZE'))
    rongji = float(conf.read_option('default','FANG_RONGJI'))
    LOG("error","--------- 信息 ----------")
    if soutao:
        LOG("info","首套房子: 是")
    else:
        LOG("warn","首套房子: 不是")
    LOG("info","房子总价: %.2f" %total)
    LOG("info","房子原价: %.2f" %old)
    LOG("info","房折旧比: %.2f" %evaluate_ratio)
    if _2year:
        LOG("info","满足两年: 是")
    else:
        LOG("warn","满足两年: 不是")
    if _5and1:
        LOG("info","满五唯一: 是")
    else:
        LOG("warn","满五唯一: 不是")
    LOG("info","房子位置: %.2f 环" %location)
    LOG("info","房子大小: %.2f 平方米" %size)
    LOG("info","房子容积: %.2f" %rongji)
    
    fang = Fang(soutao,total,old,evaluate_ratio,_2year,_5and1,location,size,rongji)
    fang.money()

    LOG("error","------ 推荐折旧比 -------")
    soufu_total_mini = 100000000.00
    evaluate_ratio_suggest = 0.60
    evaluate_ratio = 0.60
    while (evaluate_ratio < 0.95):
        fang = Fang(soutao,total,old,evaluate_ratio,_2year,_5and1,location,size,rongji) 
        soufu_total = fang.get_soufu_total()
        if soufu_total <= soufu_total_mini:
            soufu_total_mini = soufu_total
            evaluate_ratio_suggest = evaluate_ratio
        else:
            pass
        evaluate_ratio = evaluate_ratio + 0.01
    LOG("warn","推荐折旧比: %.2f => 首付为：%.2f" %(evaluate_ratio_suggest,soufu_total_mini))
