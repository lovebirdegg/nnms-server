from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action

from common.custom import CommonPagination, RbacPermission

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse,FileResponse,JsonResponse

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_xops.basic import XopsResponse
from rest_xops.code import *
from django.db.models import Q
from django.apps import apps

from rbac.models import Permission

from django.contrib.contenttypes.models import ContentType
from .serializers import *


# Create your views here.
import time
import hashlib
import requests
import json
import datetime
import os

class ContentTypeView(ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter)
    pagination_class = CommonPagination
    ordering_fields = ('id',)
    search_fields = ('model',)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=True)
    def model_detail(self, request, pk=None):
        content_type = ContentType.objects.get(pk=pk)
        app_name = content_type.app_label
        model_name = content_type.model
        model_obj = apps.get_model(app_name,model_name)
        print(model_obj)
        fields=[]
        print(model_obj._meta.fields)
        for field in model_obj._meta.fields:
            field_dic = {}
            field_dic['name'] = field.name
            field_dic['verbose_name'] = field.verbose_name
            field_dic['type'] = field.get_internal_type()
            field_dic['blank'] = field.blank
            field_dic['editable'] = field.editable
            fields.append(field_dic)
        return XopsResponse(fields)

    def generate_permission(self, model_name, model_verbose_name):
        all_permission_name = model_verbose_name
        all_permission_method = model_name + '_all'

        list_permission_name = model_verbose_name + '列表'
        list_permission_method = model_name + '_list'

        create_permission_name = model_verbose_name + '创建'
        create_permission_method = model_name + '_create'

        edit_permission_name = model_verbose_name + '编辑'
        edit_permission_method = model_name + '_edit'

        del_permission_name = model_verbose_name + '删除'
        del_permission_method = model_name + '_del'

        all_permissions = Permission.objects.filter(method=all_permission_method)

        if(len(all_permissions) == 0):
            all_permission = Permission(name=all_permission_name, method=all_permission_method)
            all_permission.save()

            list_permission = Permission(name = list_permission_name,method=list_permission_method,pid=all_permission)
            list_permission.save()
            create_permission = Permission(name=create_permission_name, method=create_permission_method, pid=all_permission)
            create_permission.save()
            edit_permission = Permission(name=edit_permission_name, method=edit_permission_method, pid=all_permission)
            edit_permission.save()
            del_permission = Permission(name=del_permission_name, method=del_permission_method, pid=all_permission)
            del_permission.save()



    def generate_vue_code(self,fields,app_name,model_name,model_camel_case_name):
            try:
                ##生成列表
                filter_fields = ''
                search_fields = ''
                table_columns = ''
                table_column_tmpl="""\t\t\t<el-table-column label="{verbose_name}" prop="{name}"/>"""
                for field in fields:
                    if(field['show']):
                        table_columns = table_columns + table_column_tmpl.format(verbose_name = field['verbose_name'],name=field['name']) + "\n"
                    if(field['filter']):
                        filter_fields = filter_fields + '\t\t\tconst {name} = this.query.{name}'.format(name=field['name']) + '\n'
                        filter_fields = filter_fields + "\t\t\tif ({name} !== '' && {name} !== null) {{ this.params['{name}'] = {name} }}".format(name=field['name']) + "\n"
                print(table_columns)
                print(filter_fields)
                index_vue_tmpl_file = open('code_tmpl/index.vue').read()
                index_vue_file_str = index_vue_tmpl_file.replace('##table_columns##',table_columns)
                index_vue_file_str = index_vue_file_str.replace('##filter_fields##',filter_fields)
                index_vue_file_str = index_vue_file_str.replace('##model_name##',model_name)
                index_vue_file_to = open('code_tmpl/{app_name}/index.vue'.format(app_name = app_name), 'w+',encoding='UTF-8')
                index_vue_file_to.write(index_vue_file_str)
                index_vue_file_to.close()

                ##生成header
                header_filter_fields = ''
                header_search_fields = ''
                header_filter_input_tmpl = """\t\t<el-input v-model="query.{name}" clearable placeholder="输入{verbose_name}" style="width: 192px;" class="filter-item" @keyup.enter.native="toQuery"/>"""

                ##date_picker 模板
                header_filter_date_picker_tmpl =  """\t\t<el-date-picker v-model="query.{name}" type="datetime" placeholder="选择{verbose_name}" />\n"""

                ##select 模板
                header_filter_select_tmpl = """\t\t<el-select v-model="query.{name}" placeholder="请选择{verbose_name}">\n"""
                header_filter_select_tmpl = header_filter_select_tmpl + """\t\t\t<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>\n"""
                header_filter_select_tmpl = header_filter_select_tmpl + """\t\t</el-select>\n"""


                for field in fields:
                    if(field['search']):
                        header_search_fields = "\t\t<el-input v-model='query.value' clearable placeholder='输入搜索' style='width: 192px;' class='filter-item' @keyup.enter.native='toQuery'/>"
                    if(field['filter']):
                        if(field['formtype'] == 'select'):
                            header_filter_fields = header_filter_fields + header_filter_select_tmpl.format(verbose_name = field['verbose_name'],name=field['name']) + '\n'
                        elif(field['formtype'] == 'datepicker'):
                            header_filter_fields = header_filter_fields + header_filter_date_picker_tmpl.format(
                                verbose_name=field['verbose_name'], name=field['name']) + '\n'
                        else:
                            header_filter_fields = header_filter_fields + header_filter_input_tmpl.format(verbose_name = field['verbose_name'],name=field['name']) + '\n'

                print(header_filter_fields)
                header_vue_tmpl_file = open('code_tmpl/header.vue').read()
                header_vue_file_str = header_vue_tmpl_file.replace('##search_fields##',header_search_fields)
                header_vue_file_str = header_vue_file_str.replace('##filter_fields##',header_filter_fields)
                header_vue_file_to = open('code_tmpl/{app_name}/header.vue'.format(app_name = app_name), 'w+',encoding='UTF-8')
                header_vue_file_to.write(header_vue_file_str)
                header_vue_file_to.close()

                ##生成editor

                edit_fields = ''
                for field in fields:
                    edit_fields = edit_fields + "\t\t\t\t{name}: this.data.{name},".format(name=field['name']) + '\n'
                edit_vue_tmpl_file = open('code_tmpl/edit.vue').read()
                edit_vue_file_str = edit_vue_tmpl_file.replace('##edit_fields##',edit_fields)
                edit_vue_file_to = open('code_tmpl/{app_name}/edit.vue'.format(app_name = app_name), 'w+',encoding='UTF-8')
                edit_vue_file_to.write(edit_vue_file_str)
                edit_vue_file_to.close()

                ##生成form

                form_fields = ''
                form_items = ''
                form_rules = ''

                ##input 模板
                form_input_tmpl = """\t\t\t<el-form-item label="{verbose_name}" prop="{name}">\n"""
                form_input_tmpl = form_input_tmpl + """\t\t\t\t<el-input v-model="form.{name}" style="width: 360px;" />\n"""
                form_input_tmpl = form_input_tmpl + "\t\t\t</el-form-item>"

                ##date_picker 模板
                form_date_picker_tmpl = """\t\t\t<el-form-item label="{verbose_name}" prop="{name}">\n"""
                form_date_picker_tmpl = form_date_picker_tmpl + """\t\t\t\t<el-date-picker v-model="form.{name}" type="date" placeholder="选择日期" />\n"""
                form_date_picker_tmpl = form_date_picker_tmpl + "\t\t\t</el-form-item>"

                ##select 模板
                form_select_tmpl = """\t\t\t<el-form-item label="{verbose_name}" prop="{name}">\n"""
                form_select_tmpl = form_select_tmpl + """\t\t\t\t<el-select v-model=""form.{name}"" placeholder="请选择">\n"""
                form_select_tmpl = form_select_tmpl + """\t\t\t\t\t<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>\n"""
                form_select_tmpl = form_select_tmpl + """\t\t\t\t</el-select>\n"""
                form_select_tmpl = form_select_tmpl + "\t\t\t</el-form-item>"

                ##radio 模板
                form_radio_tmpl = """\t\t\t<el-form-item label="{verbose_name}" prop="{name}">\n"""
                form_radio_tmpl = form_radio_tmpl + """\t\t\t\t<el-radio v-model="form.{name}" label="1">备选项1</el-radio>\n"""
                form_radio_tmpl = form_radio_tmpl + """\t\t\t\t<el-radio v-model="form.{name}" label="2">备选项2</el-radio>\n"""
                form_radio_tmpl = form_radio_tmpl + "\t\t\t</el-form-item>"

                ##checkbox 模板
                form_checkbox_tmpl = """\t\t\t<el-form-item label="{verbose_name}" prop="{name}">\n"""
                form_checkbox_tmpl = form_checkbox_tmpl + """\t\t\t\t<el-checkbox v-model="form.{name}" label="1">备选项1</el-checkbox>\n"""
                form_checkbox_tmpl = form_checkbox_tmpl + """\t\t\t\t<el-checkbox v-model="form.{name}" label="2">备选项1</el-checkbox>\n"""
                form_checkbox_tmpl = form_checkbox_tmpl + "\t\t\t</el-form-item>"

                for field in fields:
                    if (field['show']):
                        form_fields = form_fields + "\t\t\t\t{name}: '',".format(name=field['name']) + '\n'
                        if(field['formtype'] == 'input'):
                            form_items = form_items + form_input_tmpl.format(name=field['name'],
                                                                             verbose_name=field['verbose_name']) + '\n'
                        if (field['formtype'] == 'datepicker'):
                            form_items = form_items + form_date_picker_tmpl.format(name=field['name'],
                                                                             verbose_name=field['verbose_name']) + '\n'
                        if (field['formtype'] == 'select'):
                            form_items = form_items + form_select_tmpl.format(name=field['name'],
                                                                             verbose_name=field['verbose_name']) + '\n'
                        if (field['formtype'] == 'radio'):
                            form_items = form_items + form_radio_tmpl.format(name=field['name'],
                                                                             verbose_name=field['verbose_name']) + '\n'
                        if (field['formtype'] == 'checkbox'):
                            form_items = form_items + form_checkbox_tmpl.format(name=field['name'],
                                                                             verbose_name=field['verbose_name']) + '\n'
                    if(field['blank']):
                        form_rules = form_rules + "\t\t\t\t{name}: [{{ required: true, message: '请输入{verbose_name}', trigger: 'blur' }}],".format(name=field['name'],verbose_name=field['verbose_name'])+ '\n'
                form_vue_tmpl_file = open('code_tmpl/form.vue').read()
                form_vue_file_str = form_vue_tmpl_file.replace('##form_fields##',form_fields)
                form_vue_file_str = form_vue_file_str.replace('##form_items##',form_items)
                form_vue_file_str = form_vue_file_str.replace('##form_rules##',form_rules)
                form_vue_file_str = form_vue_file_str.replace('##model_name##',model_name)
                form_vue_file_to = open('code_tmpl/{app_name}/form.vue'.format(app_name = app_name), 'w+',encoding='UTF-8')
                form_vue_file_to.write(form_vue_file_str)
                form_vue_file_to.close()

                ##生成API.js
                api_js_tmpl_file = open('code_tmpl/api.js').read()
                # api_js_file_str = form_vue_tmpl_file.format(model_camel_case_name = model_camel_case_name,model_name=model_name)
                api_js_file_str = api_js_tmpl_file.replace('##model_camel_case_name##',model_camel_case_name)
                api_js_file_str = api_js_file_str.replace('##model_name##',model_name)
                api_js_file_to = open('code_tmpl/{app_name}/{model_name}.js'.format(app_name = app_name,model_name=model_name), 'w+',encoding='UTF-8')
                api_js_file_to.write(api_js_file_str)
                api_js_file_to.close()

            except (Exception) as e:
                print("Exception:" + str(e))

    @action(methods=['post'], detail=True)
    def code_generate(self, request, pk=None):
        data = {}
        content_type = ContentType.objects.get(pk=pk)

        fields = request.data
        print(fields)
        app_name = content_type.app_label#应用名称
        model_name = content_type.model#模型名称
        model_obj = apps.get_model(app_name, model_name)

        model_label = model_obj._meta.label#模型名称app.Model

        print(model_obj._meta)

        model_verbose_name = model_obj._meta.verbose_name_plural #模型中文名称
        model_camel_case_name = model_label.split('.')[1]#模型名称Model

        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#生成时间

        isExists=os.path.exists('code_tmpl/'+app_name)
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs('code_tmpl/'+app_name)

        try:
            ##生成视图文件
            filter_fields = ''
            search_fields = ''
            for field in fields:
                if(field['filter']):
                    filter_fields = filter_fields +"'"+ field['name'] + "',"
                if(field['search']):
                    search_fields = search_fields +"'"+ field['name'] + "',"
            views_tmpl_file = open('code_tmpl/views.py').read()
            views_file_str = views_tmpl_file.format(
                model_camel_case_name=model_camel_case_name,
                model_name=model_name,
                time=nowTime,
                filter_fields=filter_fields,
                search_fields=search_fields)

            views_file_to = open('code_tmpl/{app_name}/{model_name}_views.py'.format(model_name=model_name,app_name=app_name), 'w+',encoding='UTF-8')
            views_file_to.write(views_file_str)
            views_file_to.close()

            ##生成serialierz文件
            serializers_tmpl_file = open('code_tmpl/serializers.py').read()
            serializers_file_str = serializers_tmpl_file.format(
                model_name=model_camel_case_name,
                time=nowTime)

            serializers_file_to = open('code_tmpl/{app_name}/{model_name}_serializers.py'.format(model_name=model_name,app_name=app_name), 'w+',encoding='UTF-8')
            serializers_file_to.write(serializers_file_str)
            serializers_file_to.close()

            ##生成url文件
            url_tmpl_file = open('code_tmpl/urls.py').read()
            url_file_str = url_tmpl_file.format(
                model_name=model_name,
                model_camel_case_name=model_camel_case_name,
                app_name=app_name,
                time=nowTime)

            url_file_to = open('code_tmpl/{app_name}/urls.py'.format(app_name=app_name), 'w+',encoding='UTF-8')
            url_file_to.write(url_file_str)
            url_file_to.close()

            self.generate_vue_code(fields, app_name, model_name, model_camel_case_name)
            self.generate_permission(model_name, model_verbose_name)
        except (Exception) as e:
            print("Exception:" + str(e))
            return XopsResponse(data=str(e),status=BAD)
        return XopsResponse(data)
