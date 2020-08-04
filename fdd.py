# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@file: fdd.py
@time: 2020-08-02 16:08
@desc: 法大大电子合同接口类
"""
import json
import datetime
import requests
import hashlib
import base64
import urllib


class Fdd:
    """
    法大大电子合同应用接口类
    """

    def __init__(self):
        """
        核心数据初始化2.0接口版本
        """
        self.url = '法大大提供的url，形式为: http://fadada.com:8800/api/ 最后一个"/"不能丢弃'
        self.app_id = '法大大提供的app_id'
        self.app_secret = '法大大提供的密钥'
        self.v = '2.0'

    @staticmethod
    def __md5(data):
        """
        md5加密方式
        :param data: 字符串
        :return: md5值
        """
        return hashlib.md5(str(data).encode(encoding='UTF-8')).hexdigest().upper()

    @staticmethod
    def __sha1(data):
        """
        sha1加密方式
        :param data: 字符串
        :return: sha1值
        """
        s1 = hashlib.sha1()
        s1.update(data.encode())
        return s1.hexdigest().upper()

    def __sign(self, data):
        """
        单独生成签名
        :param data: 要签名的数据
        :return: 签名好的数据
        """
        if 'sign' in data.keys():
            msg = data['sign']
            del data['sign']
        else:
            msg = ''
            for key, value in sorted(data.items()):
                msg += str(value)
        msg = self.app_secret + msg
        data['app_id'] = self.app_id
        data['timestamp'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        data['v'] = self.v
        sha1_add = ''
        if 'sha1_add' in data.keys():
            sha1_add = data['sha1_add']
            del data['sha1_add']
        md5_add = ''
        if 'md5_add' in data.keys():
            md5_add = data['md5_add']
            del data['md5_add']
        s = self.__sha1(data['app_id'] + self.__md5(md5_add + data['timestamp']) + self.__sha1(msg) + sha1_add)
        data['msg_digest'] = str(base64.b64encode(s.encode("utf-8")), "utf-8")
        return data

    def __send(self, url, data):
        """
        发送
        :param data: 业务数据
        :return: 传递后的数据
        """
        res = requests.post(self.url + url, self.__sign(data))
        print(json.loads(res.text))
        return json.loads(res.text)

    def __get(self, data):
        """
        获得get参数
        :param data: 参数字典
        :return: 签名后的参数字符串
        """
        tmp = []
        for key, value in self.__sign(data).items():
            tmp.append(str(key) + '=' + urllib.parse.quote(str(value)))
        return '&'.join(tmp)

    def account_register(self, open_id, account_type):
        """
        注册法大大用户
        :param open_id: 我们自己用户的openid，字符串类型
        :param account_type: 用户类型,1:个人，2:企业
        :return: 成功了就返回customer_id,失败了就返回false
        """
        url = 'account_register.api'
        data = {
            'open_id': str(open_id),
            'account_type': str(account_type)
        }
        res = self.__send(url, data)
        if res['code'] == 1:
            return res['data']
        else:
            return False

    def get_company_verify_url(self, data):
        """
        获得企业认证地址
        :param data: 根据手册拼接字典
        :return: 成功返回字典，失败返回false
        """
        url = 'get_company_verify_url.api'
        res = self.__send(url, data)
        if res['code'] == 1:
            return {
                'transactionNo': res['transactionNo'],
                'url': str(base64.b64decode(res['url']), "utf-8")
            }
        else:
            return False

    def apply_cert(self, customer_id, verified_serialno):
        """
        实名证书申请
        :param customer_id: 用户id
        :param verified_serialno: 企业实名认证号
        :return: 布尔
        """
        url = 'apply_cert.api'
        data = {
            'customer_id': customer_id,
            'verified_serialno': verified_serialno
        }
        res = self.__send(url, data)
        if res['code'] == 1:
            return True
        else:
            return False

    def custom_signature(self, customer_id, content):
        """
        创建印章
        :param customer_id: 注册后的法大大用户
        :param content: 印章内容
        :return: 印章的base64图片
        """
        url = 'custom_signature.api'
        data = {
            'customer_id': customer_id,
            'content': content
        }
        res = self.__send(url, data)
        if res['code'] == 1:
            return res['data']['signature_img_base64']
        else:
            return False

    def upload_template(self, template_id, doc_url):
        """
        模板上传
        :param template_id: 自定义模板ID
        :param doc_url: 模板下载路径
        :return: 布尔
        """
        url = 'uploadtemplate.api'
        data = {
            'template_id': template_id,
            'doc_url': doc_url,
            'sign': template_id
        }
        res = self.__send(url, data)
        if res['code'] == '1':
            return True
        else:
            return False

    def generate_contract(self, doc_title, template_id, contract_id, parameter_map):
        """
        模板填充
        :param doc_title: 合同标题
        :param template_id: 模板的ID
        :param contract_id:
        :param parameter_map:
        :return:
        """
        url = 'generate_contract.api'
        parameter_map = json.dumps(parameter_map, ensure_ascii=False)
        data = {
            'template_id': template_id,
            'doc_title': doc_title,
            'contract_id': contract_id,
            'parameter_map': parameter_map,
            'sign': template_id + contract_id,
            'sha1_add': parameter_map
        }
        res = self.__send(url, data)
        if res['code'] == '1000':
            return res['download_url']
        else:
            return False

    def person_deposit(self, data):
        """
        个人实名信息存证
        :param data: 个人实名信息存证信息字典（个人实名信息存证接口6.3）
        :return: 存证号
        """
        url = 'person_deposit.api'
        res = self.__send(url, data)
        if res['code'] == 1:
            return res['data']
        else:
            return False

    def ext_sign(self, data):
        """
        手动签署合同
        :param data: 签署合同必要数据
        :return: 跳转的URL
        """
        parse = self.__get(data)
        return self.url + 'extsign.api?' + parse

    def view_contract(self, contract_id):
        """
        查看合同
        :param contract_id: 合同号
        :return: 查看合同的url
        """
        return self.url + 'viewContract.api?' + self.__get({'contract_id': contract_id})

    def download_contract(self, contract_id):
        """
        下载合同
        :param contract_id: 合同号
        :return: 下载合同的url
        """
        return self.url + 'downLoadContract.api.api?' + self.__get({'contract_id': contract_id})

    def contract_filing(self, contract_id):
        """
        合同归档，成功后，合同就固定完成了
        :param contract_id: 合同号
        :return: 布尔
        """
        url = 'contractFiling.api'
        res = self.__send(url, {'contract_id': contract_id})
        if res['code'] == 1:
            return True
        else:
            return False

    def check_sign(self, data):
        """
        检测异步通知信息签名是否正确
        :param data: 异步通知过来的字典
        :return: 布尔
        """
        sign = data
        msg_digest = sign['msg_digest']
        del sign['msg_digest']
        check = self.__sign(sign)
        if msg_digest == check:
            return True
        else:
            return False
