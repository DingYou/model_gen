# coding=utf-8

import pymysql
import underline_formatter as formatter
import os
from CONSTANTS import *
import sys
import platform
import json
import getpass
import datetime


class Field(object):
    def __init__(self, name, field_type, comment):
        self.name = name
        self.field_type = field_type
        self.comment = comment


if __name__ == '__main__':
    # 获取当前系统,根据系统确定路径分隔符
    current_system = platform.system()
    print('当前系统:', current_system)
    current_path = sys.path[0]
    print("当前路径:", current_path)
    separate = os.sep
    current_user = getpass.getuser()
    current_date = datetime.date.today()


    # 读取配置文件
    def read_config(conf_file_path):
        print('读取配置文件: %s' % conf_file_path)
        _conf = open(conf_file_path, encoding=DEFAULT_ENCODING)
        _conf_str = _conf.read()
        _result = json.loads(_conf_str, encoding=DEFAULT_ENCODING)
        return _result


    conf_json = read_config(current_path + separate + TABLE_CONFIG_FILE)
    # 找到java文件所在的目录
    path_split = current_path.split(separate)
    path_split.pop()
    base_application_path = separate.join(str(i) for i in path_split)
    base_java_path = base_application_path + separate + conf_json[BASE_JAVA_FOLDER_KEY]
    base_mapper_path = base_application_path + separate + conf_json[BASE_MAPPER_FOLDER_KEY]

    table_conf = conf_json[TABLE_KEY]
    # 连接数据库
    print('连接数据库...')
    connect = pymysql.Connect(
        host=table_conf['host'],
        port=table_conf['port'],
        user=table_conf['user'],
        passwd=table_conf['password'],
        db=table_conf['db'],
        charset='utf8'
    )

    # 连接数据库,获取建表sql
    try:
        _cursor = connect.cursor()
        _cursor.execute(SHOW_CREATE_TABLE_SQL_TEMP % table_conf[TABLE_NAME_KEY])
        _result = list(_cursor.fetchall())
        createSql = _result[0][1]
    finally:
        connect.close()

    # 从配置文件中读取baseModel中的字段
    base_model_fields = conf_json[BASE_MODEL_FIELDS_KEY]
    # 获取表名和表中的各字段以及字段类型和字段注释
    sql_lines = createSql.splitlines()
    table_sql = sql_lines[0]
    table_name = table_sql.split(GRAVE_ACCENT)[1]
    print("当前表名:", table_name)
    class_name = formatter.underline_to_camel(table_name)
    sql_lines.pop(0)
    type_conf = read_config(current_path + separate + TYPE_CONFIG_FILE)
    field_list = []
    type_list = []
    table_comment = ''
    for line in sql_lines:
        line = line.lstrip(SPACE)
        if line.startswith(GRAVE_ACCENT):
            _words = line.split(SPACE)
            _field_name = _words[0].strip(GRAVE_ACCENT)
            _field_name = formatter.underline_to_lower_camel(_field_name)
            if _field_name in base_model_fields:
                continue
            _field_type = _words[1].split(LEFT_PARENTHESES, 1)[0]
            _field_type = type_conf[_field_type]
            if _field_type not in type_list:
                type_list.append(_field_type)
            # 获取字段注释
            _comment = ''
            if SQL_COMMENT in line:
                _comment = line.split(SQL_COMMENT)[1].strip(SPACE)
                if _comment.endswith(COMMA):
                    _comment = _comment[1:len(_comment) - 2]
                else:
                    _comment = _comment[1:len(_comment) - 1]
            _current_field = Field(_field_name, _field_type, _comment)
            field_list.append(_current_field)
        elif line.startswith(RIGHT_PARENTHESES):
            if SQL_COMMENT in line:
                _comment = line.split(SQL_COMMENT)[1].strip(SPACE)
                table_comment = _comment[2:len(_comment) - 1]

    # 各基类全类名
    base_class_conf = conf_json[BASE_CLASS_KEY]
    # 包路径
    package_conf = conf_json[PACKAGE_KEY]
    package_path = package_conf[BASE_PACKAGE_KEY]
    # 类注释
    class_comment = (CLASS_COMMENT_TEMP % (table_name, table_comment, current_user, current_date))

    # 组装model类
    print('生成Model...')
    model_package = package_path + MODEL_PACKAGE_SUFFIX
    model_package_path = PACKAGE + SPACE + model_package
    model_class = model_package_path + SEMICOLON + NEW_LINE * 2
    # 导包
    base_model = base_class_conf[BASE_MODEL_KEY]
    model_class += IMPORT + SPACE + base_model + SEMICOLON + NEW_LINE
    for field_type in type_list:
        _full_type = type_conf[JAVA_FULL_PATH_KEY][field_type]
        if EMPTY != _full_type:
            model_class += IMPORT + SPACE + _full_type + SEMICOLON + NEW_LINE
    model_class += NEW_LINE
    # 注释
    model_class += class_comment
    # 正文
    model_class_body = ''
    # 字段
    for field in field_list:
        _field_comment = WORD_COMMENT_TEMP % field.comment
        model_class_body += _field_comment
        model_class_body += TAB + PRIVATE + SPACE + field.field_type + SPACE
        model_class_body += field.name + SEMICOLON + NEW_LINE
    #  get set 方法
    for field in field_list:
        model_class_body += NEW_LINE
        _name = field.name[0].upper() + field.name[1:]
        model_class_body += GET_TEMP % (field.field_type, _name, field.name)
        model_class_body += NEW_LINE
        model_class_body += SET_TEMP % (class_name, _name, field.field_type, field.name, field.name, field.name)
    model_class += MODEL_CLASS_TEMP % (class_name, base_model.split(POINT).pop(), class_name,
                                       model_class_body)
    model_file_path = base_java_path + separate + model_package.replace(POINT, separate)
    if not os.path.exists(model_file_path):
        os.makedirs(model_file_path)
    model_file_path += separate + class_name + JAVA_CLASS_SUFFIX
    print('Model文件路径: ', model_file_path)
    with open(model_file_path, 'w', encoding='utf-8') as model_file:
        model_file.write(model_class)

    # 生成DAO
    print('生成DAO...')
    base_dao = base_class_conf[BASE_DAO_KEY]
    dao_class_name = class_name + DAO_NAME_SUFFIX
    dao_package = package_path + DAO_PACKAGE_SUFFIX
    dao_package_path = PACKAGE + SPACE + dao_package
    dao_class = dao_package_path + SEMICOLON + NEW_LINE * 2
    # 导包
    dao_class += IMPORT + SPACE + base_dao + SEMICOLON + NEW_LINE
    dao_class += IMPORT + SPACE + model_package + POINT + class_name + SEMICOLON + NEW_LINE * 2
    dao_class += DAO_CLASS_TEMP % (
        table_name, table_comment, current_user, current_date, dao_class_name, base_dao.split(POINT).pop(), class_name)
    dao_file_path = base_java_path + separate + dao_package.replace(POINT, separate)
    if not os.path.exists(dao_file_path):
        os.makedirs(dao_file_path)
    dao_file_path += separate + dao_class_name + JAVA_CLASS_SUFFIX
    print('Dao文件路径:', dao_file_path)
    with open(dao_file_path, 'w', encoding='utf-8') as dao_file:
        dao_file.write(dao_class)

    # 生成Dao.xml
    print('生成xml...')
    xml_body = MAPPER_TEMP % (dao_package + POINT + dao_class_name)
    application_package = package_conf[APPLICATION_PACKAGE_KEY]
    app_package_len = len(application_package)
    mapper_relative_path = package_path[app_package_len:]
    mapper_relative_path = mapper_relative_path.replace(POINT, separate)
    mapper_file_path = base_mapper_path + mapper_relative_path
    if not os.path.exists(mapper_file_path):
        os.makedirs(mapper_file_path)
    xml_name = dao_class_name
    mapper_file_path += separate + xml_name + XML_FILE_SUFFIX
    with open(mapper_file_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_body)
    print('xml文件路径:', mapper_file_path)

    # 生成manager接口
    print('生成Manager...')
    base_manager = base_class_conf[BASE_DB_MANAGER_KEY]
    manager_class_name = class_name + MANAGER_NAME_SUFFIX
    manager_package = package_path + MANAGER_PACKAGE_SUFFIX
    manager_package_path = PACKAGE + SPACE + manager_package
    manager_class = manager_package_path + SEMICOLON + NEW_LINE * 2
    # 导包
    manager_class += IMPORT + SPACE + base_manager + SEMICOLON + NEW_LINE
    manager_class += IMPORT + SPACE + model_package + POINT + class_name + SEMICOLON + NEW_LINE * 2
    manager_class += MANAGER_CLASS_TEMP % (table_name, table_comment, current_user, current_date, manager_class_name,
                                           base_manager.split(POINT).pop(), class_name)
    manager_file_path = base_java_path + separate + manager_package.replace(POINT, separate)
    if not os.path.exists(manager_file_path):
        os.makedirs(manager_file_path)
    manager_file_path += separate + manager_class_name + JAVA_CLASS_SUFFIX
    print('Manager文件路径:', manager_file_path)
    with open(manager_file_path, 'w', encoding='utf-8') as manager_file:
        manager_file.write(manager_class)

    # 生成manager实现类
    print('生成Manager实现类...')
    base_manager_impl = base_class_conf[BASE_DB_MANAGER_IMPL_KEY]
    manager_impl_class_name = class_name + MANAGER_NAME_SUFFIX + IMPL_SUFFIX
    manager_impl_package = package_path + MANAGER_PACKAGE_SUFFIX + IMPL_PACKAGE_SUFFIX
    manager_impl_package_path = PACKAGE + SPACE + manager_impl_package
    manager_impl_class = manager_impl_package_path + SEMICOLON + NEW_LINE * 2
    # 导包
    manager_impl_class += IMPORT + SPACE + base_manager_impl + SEMICOLON + NEW_LINE
    manager_impl_class += IMPORT + SPACE + dao_package + POINT + dao_class_name + SEMICOLON + NEW_LINE
    manager_impl_class += IMPORT + SPACE + manager_package + POINT + manager_class_name + SEMICOLON + NEW_LINE
    manager_impl_class += IMPORT + SPACE + model_package + POINT + class_name + SEMICOLON + NEW_LINE
    manager_impl_class += MANAGER_IMPL_CLASS_TEMP % (table_name, table_comment, current_user, current_date,
                                                     manager_impl_class_name,
                                                     base_manager_impl.split(POINT).pop(),
                                                     dao_class_name, class_name, manager_class_name)
    manager_impl_file_path = base_java_path + separate + manager_impl_package.replace(POINT, separate)
    if not os.path.exists(manager_impl_file_path):
        os.makedirs(manager_impl_file_path)
    manager_impl_file_path += separate + manager_impl_class_name + JAVA_CLASS_SUFFIX
    print('Manager实现类文件路径:', manager_impl_file_path)
    with open(manager_impl_file_path, 'w', encoding='utf-8') as manager_impl_file:
        manager_impl_file.write(manager_impl_class)

    # 生成service接口
    print('生成Service...')
    base_service = base_class_conf[BASE_DB_SERVICE_KEY]
    service_class_name = class_name + SERVICE_NAME_SUFFIX
    service_package = package_path + SERVICE_PACKAGE_SUFFIX
    service_package_path = PACKAGE + SPACE + service_package
    service_class = service_package_path + SEMICOLON + NEW_LINE * 2
    # 导包
    service_class += IMPORT + SPACE + base_service + SEMICOLON + NEW_LINE
    service_class += IMPORT + SPACE + manager_package + POINT + manager_class_name + SEMICOLON + NEW_LINE
    service_class += IMPORT + SPACE + model_package + POINT + class_name + SEMICOLON + NEW_LINE * 2
    service_class += SERVICE_CLASS_TEMP % (
        table_name, table_comment, current_user, current_date, service_class_name, base_service.split(POINT).pop(), manager_class_name,
        class_name)
    service_file_path = base_java_path + separate + service_package.replace(POINT, separate)
    if not os.path.exists(service_file_path):
        os.makedirs(service_file_path)
    service_file_path += separate + service_class_name + JAVA_CLASS_SUFFIX
    print('Service文件路径:', manager_file_path)
    with open(service_file_path, 'w', encoding='utf-8') as service_file:
        service_file.write(service_class)

    # 生成service实现类
    print('生成Service实现类...')
    base_service_impl = base_class_conf[BASE_DB_SERVICE_IMPL_KEY]
    service_impl_class_name = class_name + SERVICE_NAME_SUFFIX + IMPL_SUFFIX
    service_impl_package = package_path + SERVICE_PACKAGE_SUFFIX + IMPL_PACKAGE_SUFFIX
    service_impl_package_path = PACKAGE + SPACE + service_impl_package
    service_impl_class = service_impl_package_path + SEMICOLON + NEW_LINE * 2
    # 导包
    service_impl_class += IMPORT + SPACE + base_service_impl + SEMICOLON + NEW_LINE
    service_impl_class += IMPORT + SPACE + manager_package + POINT + manager_class_name + SEMICOLON + NEW_LINE
    service_impl_class += IMPORT + SPACE + model_package + POINT + class_name + SEMICOLON + NEW_LINE
    service_impl_class += IMPORT + SPACE + service_package + POINT + service_class_name + SEMICOLON + NEW_LINE
    service_impl_class += SERVICE_IMPL_CLASS_TEMP % (table_name, table_comment, current_user, current_date,
                                                     service_impl_class_name,
                                                     base_service_impl.split(POINT).pop(),
                                                     manager_class_name,
                                                     class_name, service_class_name)
    service_impl_file_path = base_java_path + separate + service_impl_package.replace(POINT, separate)
    if not os.path.exists(service_impl_file_path):
        os.makedirs(service_impl_file_path)
    service_impl_file_path += separate + service_impl_class_name + JAVA_CLASS_SUFFIX
    print('Service实现类文件路径:', service_impl_file_path)
    with open(service_impl_file_path, 'w', encoding='utf-8') as service_impl_file:
        service_impl_file.write(service_impl_class)
        
    print('OK')
