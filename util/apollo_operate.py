#!/usr/bin/python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))
# from util.getlogger import GetLogger
from util.getconfig import GetYamlConfig

import requests
from typing import Union, Dict

# 获取日志器与配置信息
# apollo_logger = GetLogger().get_logger('basiclogger')
apollo_config = GetYamlConfig().get_config('Apollo')

__all__ = ['ApolloClient']

class ApolloClient(object):
    """ Apollo 客户端实例，使用 requests 模块进行模拟

    Attributes:
        product_info(login_product): 产品信息，区分不同 apollo 后台
        headers: 请求头, options 参数
    """
    return_msg = {'code': 'failed', 'msg': ''}
    def __init__(self, login_product: str('J9|A18')='A18', headers=None):
        self.product_info = apollo_config[login_product]
        self.login_page = self.product_info["login_url"]
        self.login_data = {
            "username": self.product_info["username"],
            "password": self.product_info["password"],
            "login-submit": "登录"
        }
        self.headers = headers

        self.__session = requests.session()
        self.__s = self.__session.post(url=self.login_page, data=self.login_data, headers=self.headers)

    def get_values(
            self,
            app_id: str,
            env: str('DEV|FAT|UAT|PRO'),
            method='GET'
    ) -> Union[None, Dict]:
        """ 获取所有配置值

        Args:
            app_id: 应用 id 信息，唯一值
            env: 配置环境
            method: 默认为 GET， 不允许更改

        Returns:
            A dict or None
            example: {}
        """
        url = f"{self.product_info['portal_url']}apps/{app_id}/envs/{env}/clusters/default/namespaces"
        try:
            get_values_result = self.__session.get(url=url)
            if  get_values_result.status_code==200:
                self.return_msg['code'] = 'successful'
                self.return_msg['msg'] = f"获取配置成功，响应内容：{get_values_result.json()}"
                return self.return_msg
            else:
                raise "响应结果为非200状态码"
        except Exception as err:
            self.return_msg['msg'] = f"获取配置失败，错误信息：{err.__str__()}"
            return self.return_msg
        finally:
            self.__session.close()

    def set_value(
            self,
            app_id: str,
            env: str('DEV|FAT|UAT|PRO'),
            data: Dict[str, str],
            namespace: str = 'application',
            method='POST',
            headers={'Content-Type': 'application/json'}
    ) -> Union[None, Dict]:
        """ 添加配置

        Args:
            app_id: 应用 id 信息，唯一值
            env: 配置环境
            data: 添加的配置值，字典类型
            namespace: apollo namespace 信息
            method: 默认为 POST， 不允许更改

        Returns:
            A dict or None
            example: {}
        """
        url = f"{self.product_info['portal_url']}apps/{app_id}/envs/{env}/clusters/default/namespaces/{namespace}/item"

        try:
            set_value_result = self.__session.post(url=url, json=data, headers=headers)
            if set_value_result.status_code == 200:
                self.return_msg['code'] = 'successful'
                self.return_msg['msg'] = f"添加配置成功，响应内容：{set_value_result.json()}"
                return self.return_msg
            else:
                self.return_msg['msg'] = f"请求响应结果错误，响应内容：{set_value_result.content}"
                return self.return_msg
        except Exception as err:
            self.return_msg['msg'] = f"添加配置失败，错误信息：{err}"
            return self.return_msg
        finally:
            self.__session.close()

    def add_authorized(
            self,
            app_id: str = None,
            env: str('DEV|FAT|UAT|PRO') = None,
            user: str=None,
            permission: str('ModifyNamespace|ReleaseNamespace')=None,
            namespace: str = 'application',
            headers={'Content-Type': 'text/plain'}
    ) -> None:
        url = f"{self.product_info['portal_url']}apps/{app_id}/envs/{env}/namespaces/{namespace}/roles/{permission}"
        try:
            auth_result = self.__session.post(url=url, data=user, headers=headers)
            if auth_result.status_code == 200:
                self.return_msg['code'] = 'successful'
                self.return_msg['msg'] = f"用户：{user} 授权到：{app_id} {namespace} {permission} 成功"
                return self.return_msg
            else:
                self.return_msg['msg'] = f"用户：{user} 授权到：{app_id} {namespace} {permission}失败，错误信息：{auth_result.text}"
                return self.return_msg
        except Exception as err:
            self.return_msg['msg'] = f"请求响应结果错误，错误信息：{err.__str__()}"
            return self.return_msg
        finally:
            self.__session.close()

if __name__ == '__main__':
    pass
