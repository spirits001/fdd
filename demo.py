# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@file: demo.py
@time: 2020-08-04 23:42
@desc: 法大大电子合同使用样例
"""
import json
from fdd import Fdd

fdd = Fdd()


def account_register():
    # 用户注册 企业为0 个人为1
    res = fdd.account_register('hofeng', '1')
    return res


def person_deposit():
    # 实名信息哈希存证
    data = {
        'customer_id': 'xxxxxxxxxxxx',
        'preservation_name': 'xxxx',
        'preservation_data_provider': 'xxxx',
        'name': '姓名',
        'idcard': '身份证号码',
        'verified_type': '2',
        'mobile': '手机号',
        'mobile_essential_factor': json.dumps({'transaction_id': 'xxxxx'}),  # 要转换为json字符串
        'cert_flag': '1',  # 自动创建证书
    }
    res = fdd.person_deposit(data)
    return res


def custom_signature():
    # 创建用户印章
    res = fdd.custom_signature('customer_id', '印章名称')
    return res


def upload_template():
    # 上传合同模板
    res = fdd.upload_template('模板名称', '模板地址')
    return res


def generate_contract():
    # 用变量生成合同文件
    # 变量字典，键值对
    data = {
        "xxxx": 'xxxx'
    }
    res = fdd.generate_contract('合同名称', '模板编号', '合同编号', data)
    return res


def ext_sign():
    # 手工发起合同签署（甲方和乙方分别发起）
    data = {
        'contract_id': '合同编号',
        'transaction_id': '模板编号',
        'customer_id': '用户ID',
        'doc_title': '合同名称',
        'sign_keyword': '盖章位置',
        'sign': '用户ID',
        'md5_add': '模板编号',
        'customer_mobile': '手机号',
    }
    res = fdd.ext_sign(data)
    return res
