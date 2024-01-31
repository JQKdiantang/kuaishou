import configparser


class IniManager:
    def __init__(self, filepath):
        """ 初始化IniManager类，加载指定路径的ini文件 """
        self.filepath = filepath
        self.config = configparser.ConfigParser()
        self.config.read(self.filepath, encoding='GBK')

    def get_sections(self):
        """ 获取ini文件所有section（块）名称列表 """
        return self.config.sections()

    def get_options(self, section):
        """ 获取指定section下的所有选项（项）名称列表 """
        return self.config.options(section)

    def get_items(self, section):
        """ 获取指定section下的所有键值对 """
        return self.config.items(section)

    def get_value(self, section, option):
        """ 获取指定section下指定option的值 """
        return self.config.get(section, option)

    def set_value(self, section, option, value):
        """ 设置或修改指定section下指定option的值 """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        self.write_to_file()

    def add_section(self, section):
        """ 添加新的section到ini文件中 """
        self.config.add_section(section)
        self.write_to_file()

    def remove_section(self, section):
        """ 删除ini文件中的指定section """
        if self.config.has_section(section):
            self.config.remove_section(section)
            self.write_to_file()

    def remove_option(self, section, option):
        """ 删除指定section下的指定option """
        if self.config.has_section(section) and self.config.has_option(section, option):
            self.config.remove_option(section, option)
            self.write_to_file()

    def write_to_file(self):
        """ 将修改后的配置写入ini文件 """
        with open(self.filepath, 'w') as configfile:
            self.config.write(configfile)


# 使用示例：
if __name__ == '__main__':
    ini_manager = IniManager('./config.ini')

    # 获取所有section
    sections = ini_manager.get_sections()
    print(sections)
