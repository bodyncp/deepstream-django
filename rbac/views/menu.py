#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import OrderedDict
from django.shortcuts import render, redirect, HttpResponse
from django.forms import formset_factory
from django.conf import settings
from django.utils.module_loading import import_string

from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, MultiAddPermissionForm, \
    MultiEditPermissionForm
from rbac.service.urls import memory_reverse
from rbac.service.routes import get_all_url_dict
from stark.utils.pagination import Pagination


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """

    menus = models.Menu.objects.all()
    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menu_exists = models.Menu.objects.filter(id=menu_id).exists()
    if not menu_exists:
        menu_id = None
    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []

    user_name = None
    user_name_dict = request.session.get("show_permission")
    if user_name_dict:
        user_name = user_name_dict.get("user_name")

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menus': second_menus,
            'permissions': permissions,
            'menu_id': menu_id,
            'second_menu_id': second_menu_id,
            "users": user_name,
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        }
    )


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()

        user_name = None
        user_name_dict = request.session.get("show_permission")
        if user_name_dict:
            user_name = user_name_dict.get("user_name")

        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": user_name,
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def menu_edit(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)

        user_name = None
        user_name_dict = request.session.get("show_permission")
        if user_name_dict:
            user_name = user_name_dict.get("user_name")

        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": user_name,
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def menu_del(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(
            request,
            'rbac/delete.html',
            {
                'cancel': url,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认值）
    :return:
    """

    menu_object = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def second_menu_edit(request, pk):
    """
    编辑二级菜单
    :param request:
    :param pk: 当前要编辑的二级菜单
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)
        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def second_menu_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(
            request,
            'rbac/delete.html',
            {
                'cancel': url,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限
    :param request:
    :param second_menu_id:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse('二级菜单不存在，请重新选择！')
        form.instance.pid = second_menu_object
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk: 当前要编辑的权限ID
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')
    page_type = request.GET.get('page')
    start_page = 0
    end_page = 0

    if not page_type:
        start_page = 0
        end_page = 20

    if page_type and int(page_type) == 1:
        start_page = 0
        end_page = 20
    elif page_type:
        start_page = (int(page_type) - 1) * 20
        end_page = int(page_type) * 20

    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    generate_formset = None
    update_formset = None
    if request.method == 'POST' and post_type == 'generate':
        # pass # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                models.Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        # pass  # 批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset

        else:
            update_formset = formset

    # 1. 获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    """
    {
        'rbac:role_list':{'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        'rbac:role_add':{'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
        ....
    }
    """
    router_name_set = set(all_url_dict.keys())

    # 2. 获取数据库中所有的URL
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])
    """
    {
        'rbac:role_list': {'id':1,'title':'角色列表',name:'rbac:role_list',url.....},
        'rbac:role_add': {'id':1,'title':'添加角色',name:'rbac:role_add',url.....},
        ...
    }
    """

    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 3. 应该添加、删除、修改的权限有哪些？
    # 3.1 计算出应该增加的name
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # 3.2 计算出应该删除的name
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name
    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        data_len = [row_dict for name, row_dict in permission_dict.items() if name in update_name_list]
        request.session['data_count'] = len(data_len)

        update_formset = update_formset_class(
                initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list][
                        start_page:end_page])

    query_params = request.GET.copy()

    pager = Pagination(
        current_page=page_type,
        all_count=request.session['data_count'],
        base_url=request.path_info,
        query_params=query_params,
        per_page=20
    )

    data_list = update_formset

    user_name = None
    user_name_dict = request.session.get("show_permission")
    if user_name_dict:
        user_name = user_name_dict.get("user_name")

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'generate_formset': generate_formset,
            'delete_row_list': delete_row_list,
            'update_formset': data_list,
            'pager': pager,
            "users": user_name,
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        }
    )


def multi_permissions_del(request, pk):
    """
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    """
    url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """

    user_id = request.GET.get('uid')
    # 业务中的用户表 "app01.models.UserInfo""
    user_model_class = import_string(settings.RBAC_USER_MODLE_CLASS)

    user_object = user_model_class.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色，然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}

    # 获取当前用户用户用户的所有权限

    # 如果选中的角色，优先显示选中角色所拥有的权限
    # 如果没有选择角色，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}

    elif user_object:  # 未选择角色，但选择了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    all_user_list = user_model_class.objects.all()

    all_role_list = models.Role.objects.all()

    menu_permission_list = []

    # 所有的菜单（一级菜单）
    all_menu_list = models.Menu.objects.values('id', 'title')
    """
    [
        {id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,'children':[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1 },]},
        {id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2 },{id:5,title:x1, menu_id:2 },]},
        {id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3 },]},
    ]
    """
    all_menu_dict = {}
    """
       {
           1:{id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1,children:[] },]},
           2:{id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2,children:[] },{id:5,title:x1, menu_id:2,children:[] },]},
           3:{id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3,children:[] },]},
       }
       """
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item

    # 所有二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    """
    [
        {id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        {id:2,title:x1, menu_id:1,children:[] },
        {id:3,title:x1, menu_id:2,children:[] },
        {id:4,title:x1, menu_id:3,children:[] },
        {id:5,title:x1, menu_id:2,children:[] },
    ]
    """
    all_second_menu_dict = {}
    """
        {
            1:{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
            2:{id:2,title:x1, menu_id:1,children:[] },
            3:{id:3,title:x1, menu_id:2,children:[] },
            4:{id:4,title:x1, menu_id:3,children:[] },
            5:{id:5,title:x1, menu_id:2,children:[] },
        }
        """
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row

        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 所有三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    """
    [
        {id:11,title:x2,pid:1},
        {id:12,title:x2,pid:1},
        {id:13,title:x2,pid:2},
        {id:14,title:x2,pid:3},
        {id:15,title:x2,pid:4},
        {id:16,title:x2,pid:5},
    ]
    """
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {
                    'id':11, 
                    title:'账单列表',
                    children:[
                        {'id':12,title:'添加账单'}
                    ]
                },
                {'id':11, title:'客户列表'},
            ]
        },
        
    ]
    """

    user_name = None
    user_name_dict = request.session.get("show_permission")
    if user_name_dict:
        user_name = user_name_dict.get("user_name")

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
            "users": user_name,
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        }
    )
