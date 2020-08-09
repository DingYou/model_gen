## 定制过的mybatis-plus代码生成器
**环境准备**
1. python3  
    *python3.6/python3.7/python3.8都可以正常使用*
2. pymysql  
    *使用最新版即可, 可以使用pip3进行安装:*
    ```shell script
   pip3 install PyMySQL
   ```
**使用方法**  
1. 确保项目使用了mybatis-plus  
    *如果没有使用mybatis-plus使用本生成器只能减少写models的时间, 意义可能不大.*
2. 引入本生成器
3. 准备好各层的Base类  
    **
4. 配置config.json
5. 生成代码  
    ```shell script
    cd $PROJECT_DIR/src/model_gen && sh do_gen.sh
    ```