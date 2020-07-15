# coding=utf-8
"""
常量类
"""
# 默认字符集
DEFAULT_ENCODING = 'utf8'
# 表相关配置文件文件
TABLE_CONFIG_FILE = 'config.json'
# 类型相关配置文件
TYPE_CONFIG_FILE = 'type_config.json'
# 查询建表语句的sql模板
SHOW_CREATE_TABLE_SQL_TEMP = 'show CREATE table %s'
# 配置文件中表配置的key
TABLE_KEY = 'table'
# 配置文件中表名的key
TABLE_NAME_KEY = 'table_name'
# 配置文件中包配置的key
PACKAGE_KEY = 'package'
# 配置文件各基类全类名配置的key
BASE_CLASS_KEY = 'base_class'
# 配置文件中base包名配置的key
BASE_PACKAGE_KEY = 'base_package'
# java全路径配置的key
JAVA_FULL_PATH_KEY = 'java_full_path'
# 配置中baseModel全路径的key
BASE_MODEL_KEY = 'base_model'
# 配置中BaseDao全路径的key
BASE_DAO_KEY = 'base_dao'
# 配置中baseManager全路径的key
BASE_DB_MANAGER_KEY = 'base_db_manager'
# 配置中baseManagerImpl全路径的key
BASE_DB_MANAGER_IMPL_KEY = 'base_db_manager_impl'
# 配置中baseService全路径的key
BASE_DB_SERVICE_KEY = 'base_db_service'
# 配置中baseServiceImpl全路径的key
BASE_DB_SERVICE_IMPL_KEY = 'base_db_service_impl'
# 配置中java文件文件夹的key
BASE_JAVA_FOLDER_KEY = 'base_java_folder'
# 配置中mapper文件文件夹的key
BASE_MAPPER_FOLDER_KEY = 'base_mapper_folder'
# 配置中BaseModel字段集合的key
BASE_MODEL_FIELDS_KEY = 'base_model_fields'
# 配置中的application_package的key
APPLICATION_PACKAGE_KEY = 'application_package'
# sql中的comment
SQL_COMMENT = 'COMMENT'


# 重音符
GRAVE_ACCENT = '`'
# 空格
SPACE = ' '
# 空字符串
EMPTY = ''
# 逗号
COMMA = ","
# 左括号
LEFT_PARENTHESES = '('
# 右括号
RIGHT_PARENTHESES = ')'
# 左大括号
LEFT_BIG_PARENTHESES = '{'
# 右大括号
RIGHT_BIG_PARENTHESES = '}'
# 星号
ASTERISK = '*'
# 分号
SEMICOLON = ';'
# 点
POINT = '.'
# 换行符
NEW_LINE = '\n'

# 各种包路径后缀
MODEL_PACKAGE_SUFFIX = '.model'
DAO_PACKAGE_SUFFIX = '.dao'
MANAGER_PACKAGE_SUFFIX = '.manager'
SERVICE_PACKAGE_SUFFIX = '.service'
IMPL_PACKAGE_SUFFIX = '.impl'

# java文件后缀
JAVA_CLASS_SUFFIX = '.java'
# xml文件后缀
XML_FILE_SUFFIX = '.xml'

# DAO名后缀
DAO_NAME_SUFFIX = 'Dao'
# manager名后缀
MANAGER_NAME_SUFFIX = 'Manager'
# service名后缀
SERVICE_NAME_SUFFIX = 'Service'
# Impl名后缀
IMPL_SUFFIX = 'Impl'

# 一个tab=4个空格
TAB = SPACE * 4

# package
PACKAGE = 'package'
# private
PRIVATE = 'private'
# public
PUBLIC = 'public'
# import
IMPORT = 'import'
# set
SET = 'set'
# get
GET = 'get'

# 字段文档注释模版
WORD_COMMENT_TEMP = """    /**
     * %s
     */
"""

# 类注释
CLASS_COMMENT_TEMP = """/**
 * %s 表 (%s)
 * @author %s create by class_gen.py
 * @date %s
 */
 """

# set方法模版
SET_TEMP = """    public %s set%s(%s %s) {
        this.%s = %s;
        return this;
    }
"""
# get方法模版
GET_TEMP = """    public %s get%s() {
        return %s;
    }
"""
# model类模版
MODEL_CLASS_TEMP = """public class %s extends %s<%s> {
%s}"""

# DAO类模版
DAO_CLASS_TEMP = """/**
 * %s 表 (%s)
 * @author %s create by class_gen.py
 * @date %s
 */
public interface %s extends %s<%s> {
}"""

# mapper.xml模版
MAPPER_TEMP = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="%s">

</mapper>"""

# manager接口模板
MANAGER_CLASS_TEMP = """/**
 * %s 表 (%s)
 * @author %s create by class_gen.py
 * @date %s
 */
public interface %s extends %s<%s> {
}"""

# manager实现类模板
MANAGER_IMPL_CLASS_TEMP = """import org.springframework.stereotype.Repository;

/**
 * %s 表 (%s)
 * @author %s create by class_gen.py
 * @date %s
 */
@Repository
public class %s extends %s<%s, %s> implements %s {
}"""

# service接口模版
SERVICE_CLASS_TEMP = """/**
 * %s 表 (%s)
 * @author %s create by class_gen.py
 * @date %s
 */
public interface %s extends %s<%s, %s> {
}"""

# service实现类模版
SERVICE_IMPL_CLASS_TEMP = """import org.springframework.stereotype.Service;

/**
 * %s 表 (%s)
 * @author %s create by class_gen.py
 * @date %s
 */
 @Service
public class %s extends %s<%s, %s> implements %s {
}"""