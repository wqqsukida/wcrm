# -*- coding: utf-8 -*-
# Author zwhset

TEST_DOMAIN_NAME = 'dylan.org'
TEST_GROUP_NAME  = 'test-python-ldap-group'

from domain import Domain
from dmonitor import DMonitor

class DomainTest(Domain):

    def __init__(self):
        super(DomainTest, self).__init__()
        # try:
        #     self.remove(domain=TEST_DOMAIN_NAME)
        #     self.group_remove(group_id=self.get_test_group_id())
        # except:
        #     pass

    def check_func(self, name, data):
        try:
            ret_code =  int(data['status']['code'])
        except:
            ret_code = None

        if ret_code == 1:
            print name, ': True'
            print data
        else:
            print name, ': False'
            try:
                print data.get('status', {}).get('message', None) or data
            except Exception as e:
                print 'data error: ', data


    def domain_list_test(self):
        self.check_func('domain_list_test', self.list())

    def domain_create_test(self):
        self.check_func('domain_list_create', self.create(domain=TEST_DOMAIN_NAME))

    def domain_remove_test(self):
        self.check_func('domain_remove_test', self.remove(domain=TEST_DOMAIN_NAME))

    def domain_status_test(self):
        print 'create domain: ', TEST_DOMAIN_NAME
        self.create(domain=TEST_DOMAIN_NAME)
        self.check_func('domain_status_test', self.status(domain=TEST_DOMAIN_NAME,
                                                          status='disable'))
    def domain_info_test(self):
        self.check_func('domain_info_test', self.info(domain=TEST_DOMAIN_NAME))

    def domain_log_test(self):
        self.check_func('domain_log_test', self.log(domain=TEST_DOMAIN_NAME))

    def domain_grouplist_test(self):
        self.check_func('domain_grouplist_test', self.group_list())

    def domain_groupcreate_test(self):
        self.check_func('domain_groupcreate_test',
                        self.group_create(group_name=TEST_GROUP_NAME)
                        )

    def domain_groupmodify_test(self):
        new_group_name = 'new' + TEST_GROUP_NAME
        group_id = self.get_test_group_id()

        self.check_func('domain_groupmodify_test',
                        self.group_modify(group_name=new_group_name,
                                          group_id=group_id)
                        )

    def domain_changegroup_test(self):
        group_id = self.get_test_group_id()
        self.check_func('domain_changegroup_test', self.change_group(
            group_id=group_id,
            domain=TEST_DOMAIN_NAME
        ))

    def domain_groupremove_test(self):
        self.check_func('domain_groupremove_test',
                        self.group_remove(self.get_test_group_id()))

    def domain_ismark_test(self):
        self.check_func('domain_ismark_test',
                        self.ismark(domain=TEST_DOMAIN_NAME,
                                    is_mark='yes'))

    def domain_remark_test(self):
        self.check_func('domain_remark_test',
                        self.remark(domain=TEST_DOMAIN_NAME,
                                    remark='This is test remark'))

    def domain_purview_test(self):
        self.check_func('domain_purview_test',
                        self.purview(domain=TEST_DOMAIN_NAME))

    def test_all(self):
        self.domain_list_test()
        self.domain_create_test()
        self.domain_remove_test()
        self.domain_status_test()
        self.domain_info_test()
        self.domain_log_test()
        self.domain_grouplist_test()
        # 分组测不了，这是个人版
        # self.domain_groupcreate_test()
        # self.domain_groupmodify_test()
        # self.domain_changegroup_test()
        # self.domain_groupremove_test()
        self.domain_ismark_test()
        self.domain_remark_test()
        self.domain_purview_test()

    def get_test_group_id(self):
        _ret = self.group_list()
        try:
            group_id = None
            groups = _ret['groups']
            for group in groups:
                if group.get('group_name', None) == TEST_GROUP_NAME:
                    group_id = group.get('group_id')
                    print 'get group id: ', group_id
                    return group_id
            if not group_id:
                raise ValueError, 'DndPod APi error, not get group_id'
        except Exception as e:
            raise ValueError, 'DndPod APi error, not get group_id' + str(e)


class DMonitorTest(DMonitor):

    def __init__(self):
        super(DMonitorTest, self).__init__()

    def list_subdomain_test(self):
        pass

    def list_sub_value_test(self):
        pass

    def list_test(self):
        pass

    def create_test(self):
        pass

    def modify_test(self):
        pass

    def remove_test(self):
        pass

    def info_test(self):
        pass

    def set_status_test(self):
        pass

    def get_history_test(self):
        pass

    def user_desc_test(self):
        pass

    def get_downs_test(self):
        pass

    def all_test(self):
        pass



if __name__ == '__main__':
    dt = DomainTest()
    dt.domain_list_test()