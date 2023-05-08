'''
Client for interacting with pscheduler
'''

#from urllib import response
#import uuid
from .api_filters import ApiFilters
#import re
from .test import Test
from .task import Task
from .tool import Tool
from ..utils import Utils, build_err_msg, extract_url_uuid

class ApiConnect(object):

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.bind_address = kwargs.get('bind_address', None)
        self.bind_map = kwargs.get('bind_map', {})
        self.lead_address_map = kwargs.get('lead_address_map', {})
        self.filters = kwargs.get('filters', ApiFilters())
        self.error = None

    def get_tasks(self):
        tasks_url = self.url
        tasks_url = tasks_url.strip()
        if not tasks_url.endswith('/'):
            tasks_url += '/'
        tasks_url = tasks_url + 'tasks'
        filters = {'detail': True, "expanded": True}

        if self.filters.task_filters:
            filters['json'] = self.filters.task_filters
        
        response = Utils().send_http_request(
            connection_type = 'GET',
            url = tasks_url,
            timeout = self.filters.timeout,
            get_params = filters,
            ca_certificate_file = self.filters.ca_certificate_file,
            ca_certificate_path = self.filters.ca_certificate_path,
            verify_hostname = self.filters.verify_hostname,
            local_address = self.bind_address,
            bind_map = self.bind_map,
            address_map = self.lead_address_map
        )

        if not response.ok: 
            self.error = build_err_msg(http_resonse=response)
            return
        
        response_json = response.json() 
        if not response_json:
            self.error = "No task objects returned"
            return

        if type(response_json) is not list:
            self.error = "Tasks must be an array. Not {}".format(type(response_json))
            return
        
        tasks = []
        for task_response_json in response_json:
            task_url = ''
            if 'detail' in task_response_json:
                if 'href' in task_response_json['detail']:
                    task_url = task_response_json['detail']['href']
                    has_detail = True
            elif 'href' in task_response_json:
                task_url = task_response_json['href']
            elif not task_url: 
                continue
        
            task_uuid = extract_url_uuid(url=task_url) #Utils
            if not task_uuid:
                self.error = "Unable to extract UUID from url {}".format(task_url)
                continue
            
            if has_detail:
                task = Task(
                    data=task_response_json,
                    url=self.url,  
                    filters=self.filters,
                    uuid=task_uuid,
                    bind_map=self.bind_map,
                    lead_address_map=self.lead_address_map
                )
            else:
                task = self.get_task(task_uuid)
            
            if not task:
                #There was an error
                continue
            
            tasks.append(task)
        
        return tasks
    
    def get_task(self, task_uuid): 
        #build url
        task_url = self.url
        task_url = task_url.strip()
        if not task_url.endswith('/'):
            task_url += '/'
        task_url = task_url + "tasks/" + task_uuid

        #fetch task
        task_response = Utils().send_http_request(
            connection_type='GET',
            url=task_url,
            get_params={'detail':True},
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not task_response.ok:
            self.error = build_err_msg(http_response=task_response)
            return
        
        task_response_json = task_response.json() 
        if not task_response_json:
            self.error = "No task returned from {}".format(task_url)
            return
        
        return Task(
            data=task_response_json,
            url=self.url, 
            filters=self.filters,
            uuid=task_uuid,
            bind_map=self.bind_map,
            lead_address_map=self.lead_address_map
        )
    
    def get_tools(self):

        #build url
        tools_url = self.url
        tools_url = tools_url.strip()
        if not tools_url.endswith('/'):
            tools_url += '/'
        tools_url = tools_url + "tools"

        filters = {}

        response = Utils().send_http_request(
            connection_type='GET',
            url=tools_url,
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not response.ok:
            self.error = build_err_msg(http_respose=response)
            return
        
        response_json = response.json()
        if not response_json:
            self.error = "No tool objects returned"
            return
        
        if type(response_json) is not list:
            self.error = "Tools must be an array. Not {}".format(type(response_json))
            return
        
        tools = []

        for tool_url in response_json:
            tool_name = extract_url_uuid(url=tool_url)
            if not tool_name:
                self.error = "Unable to extract name from url {}".format(tool_url)
                return
            
            tool = self.get_tool(tool_name)

            if not tool:
                #there was an error
                return 
            
            tools.append(tool)
        
        return tools
    
    def get_tool(self, tool_name):

        #build url
        tool_url = self.url
        tool_url = tool_url.strip()
        if not tool_url.endswith('/'):
            tool_url += '/'
        tool_url = tool_url + 'tools/' + tool_name

        #fetch tool
        tool_response = Utils().send_http_request(
            connection_type='GET',
            url=tool_url,
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not tool_response.ok:
            self.error = build_err_msg(http_response=tool_response)
            return
        
        tool_response_json = tool_response.json()
        if not tool_response_json:
            self.error("No tool object returned from {}".format(tool_url))
            return
        
        return Tool(
            data=tool_response_json,
            url=tool_url,
            filters=self.filters,
            uuid=tool_name
        )

    def get_test_urls(self):

        #build url
        tests_url = self.url
        tests_url = tests_url.strip()

        if not tests_url.endswith('/'):
            tests_url += '/'
        tests_url = tests_url + 'tests'

        filters = {}

        response = Utils().send_http_request(
            connection_type='GET',
            url=tests_url,
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not response.ok:
            self.error = build_err_msg(http_response=response)
            return
        
        response_json = response.json()
        if not response_json:
            self.error = "No test objects returned"
            return
        
        if type(response_json) is not list:
            self.error = "Tests must be a list. Not {}".format(type(response_json))
            return
        
        return response_json
    
    def get_tests(self):

        #build url
        tests_url = self.url
        tests_url = tests_url.strip()
        if not tests_url.endswith('/'):
            tests_url += '/'
        tests_url += "tests"

        filters = {}

        response = Utils().send_http_request(
            connection_type='GET',
            url=tests_url,
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not response.ok:
            self.error = build_err_msg(http_response=response)
            return
        
        response_json = response.json()
        if not response_json:
            self.error = 'No test objects returned'
            return
        
        if type(response_json) is not list:
            self.error('Tests must be a list. Not {}'.format(response_json))
            return
        
        tests = []
        for test_url in response_json:
            test_name = extract_url_uuid(url=test_url)
            if not test_name:
                self.error = 'Unable to extract name from url {}'.format(test_url)
                return
            test = self.get_test(test_name)

            if not test:
                #There was an error
                return
            tests.append(test)
        
        return tests
    
    def get_test(self, test_name):
        #build url
        test_url = self.url
        test_url = test_url.strip()
        if not test_url.endswith('/'):
            test_url += '/'
        
        test_url = test_url + "tests/" + test_name

        #fetch test
        test_response = Utils().send_http_request(
            connection_type='GET',
            url=test_url,
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not test_response.ok:
            self.error = build_err_msg(http_response=test_response)
            return
        
        test_response_json = test_response.json()
        if not test_response_json:
            self.error="No test object returned from {}".format(test_url)
        
        return Test(
            data=test_response_json,
            url=test_url,
            filters=self.filters,
            uuid=test_name
            )
    
    def get_hostname(self):

        #build url
        hostname_url = self.url
        hostname_url = hostname_url.strip()
        if not hostname_url.endswith('/'):
            hostname_url += '/'
        
        hostname_url += "hostname"

        filters = {}

        response = Utils().send_http_request(
            connection_type="GET",
            url=hostname_url,
            timeout=self.filters.timeout,
            ca_certificate_file=self.filters.ca_certificate_file,
            ca_certificate_path=self.filters.ca_certificate_path,
            verify_hostname=self.filters.verify_hostname,
            local_address=self.bind_address,
            bind_map=self.bind_map,
            address_map=self.lead_address_map
        )

        if not response.ok:
            self.error = build_err_msg(http_response=response)
            return
        
        response_json = response.json()
        if not response_json:
            self.error= "No hostname returned"
            return
        
        return response_json

