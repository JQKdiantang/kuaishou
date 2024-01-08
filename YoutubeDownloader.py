import chardet


def get_encoding(__file_path):
    with open(__file_path, 'rb') as f:
        data = f.read()
    result = chardet.detect(data)
    return result['encoding']


def replaceStr(__file_path, target_char, old_char):
    encoding = get_encoding(__file_path)
    # 步骤1：打开文件并读取内容（使用UTF-8编码）
    with open(__file_path, 'r', encoding=encoding) as file:
        content = file.read()

    # 步骤2：使用replace()方法将指定字符替换为目标字符
    new_content = content.replace(old_char, target_char)
    # 步骤3：将修改后的内容写回到文件（使用UTF-8编码）
    with open(__file_path, 'w', encoding=encoding) as file:
        file.write(new_content)
    file.close()


def SettingView(__file_path):
    replaceStr(__file_path, "Text=\"设置\"", "Text=\"Settings\"")

    replaceStr(__file_path, "自动更新", "Auto-updates")
    replaceStr(__file_path, "自动更新", "Auto-update")
    replaceStr(__file_path, "每次启动时执行自动更新", "Perform automatic updates on every launch")
    replaceStr(__file_path, "建议启用此选项，以确保该应用程序与最新版本的YouTube兼容",
               "it's recommended to leave this option enabled to ensure that the app is compatible with the latest version of YouTube")

    replaceStr(__file_path, "暗黑模式", "Dark mode")
    replaceStr(__file_path, "在UI中使用较深的颜色", "Use darker colors in the UI")

    replaceStr(__file_path, "保存身份验证", "Persist authentication")
    replaceStr(__file_path, "将身份验证cookie保存到文件中，以便它们可以在会话之间持久化",
               "Save authentication cookies to a file so that they can be persisted between sessions")

    replaceStr(__file_path, "插入媒体标签", "Inject media tags")
    replaceStr(__file_path, "将媒体标签插入下载的文件",
               "Inject media tags into downloaded files")

    replaceStr(__file_path, "跳过现有文件", "Skip existing files")
    replaceStr(__file_path, "选择要下载的多个视频时，请跳过目标目录中已经有匹配文件的视频",
               "When selecting multiple videos to download, skip those that already have matching files in the target directory")

    replaceStr(__file_path, "文件名模板", "File name template")
    replaceStr(__file_path, "用于为下载的视频生成文件名的模板",
               "Template used for generating file names for downloaded videos")
    replaceStr(__file_path, "可用示例", "Available tokens:")
    replaceStr(__file_path, "--视频在列表中的位置（如果适用）", "— video's position in the list (if applicable)")
    replaceStr(__file_path, "--视频ID", "— video ID")
    replaceStr(__file_path, "--视频标题", "— video title")
    replaceStr(__file_path, "--视频作者", "— video author")

    replaceStr(__file_path, "多线程上限", "Parallel limit")
    replaceStr(__file_path, "可以同时激活多少个下载项", "How many downloads can be active at the same time")

    replaceStr(__file_path, "Content=\"关闭\"", "Content=\"CLOSE\"")


def DownloadMultipleSetupView(__file_path):
    replaceStr(__file_path, "Text=\"容器：\"", "Text=\"Container:\"")
    replaceStr(__file_path, "Text=\"视频质量：\"", "Text=\"Video quality:\"")
    replaceStr(__file_path, "Text=\"下载\"", "Text=\"DOWNLOAD\"")
    replaceStr(__file_path, "Content=\"取消\"", "Content=\"CANCEL\"")


def DownloadSingleSetupView(__file_path):
    replaceStr(__file_path, "Text=\"格式：\"", "Text=\"Format:\"")
    replaceStr(__file_path, "Content=\"下载\"", "Content=\"DOWNLOAD\"")
    replaceStr(__file_path, "Content=\"取消\"", "Content=\"CANCEL\"")


def DashboardView(__file_path):
    replaceStr(__file_path, "Hint=\"URL或搜索查询\"", "Hint=\"URL or search query\"")
    replaceStr(__file_path, "ToolTip=\"设置\"", "ToolTip=\"Settings\"")
    replaceStr(__file_path, "ToolTip=\"身份验证\"", "ToolTip=\"Authentication\"")

    replaceStr(__file_path, "Header=\"文件\"", "Header=\"File\"")
    replaceStr(__file_path, "Header=\"状态\"", "Header=\"Status\"")
    replaceStr(__file_path, "Value=\"等待中...\"", "Value=\"Pending...\"")
    replaceStr(__file_path, "Value=\"✓ 完成\"", "Value=\"✓ Done\"")
    replaceStr(__file_path, "Value=\"✗ 已取消\"", "Value=\"✗ Canceled\"")
    replaceStr(__file_path, "Value=\"⚠ 失败\"", "Value=\"⚠ Failed\"")
    replaceStr(__file_path, "Value=\"单击复制错误消息\"", "Value=\"Click to copy the error message\"")

    replaceStr(__file_path, "Header=\"清除成功的下载\"", "Header=\"Remove successful downloads\"")
    replaceStr(__file_path, "Header=\"清除非活动下载\"", "Header=\"Remove inactive downloads\"")
    replaceStr(__file_path, "Header=\"重启失败的下载\"", "Header=\"Restart failed downloads\"")
    replaceStr(__file_path, "Header=\"取消所有下载\"", "Header=\"Cancel all downloads\"")

    replaceStr(__file_path, "ToolTip=\"显示文件\"", "ToolTip=\"Show file\"")
    replaceStr(__file_path, "ToolTip=\"播放\"", "ToolTip=\"Play\"")
    replaceStr(__file_path, "ToolTip=\"取消下载\"", "ToolTip=\"Cancel download\"")
    replaceStr(__file_path, "ToolTip=\"重启下载\"", "ToolTip=\"Restart download\"")

    replaceStr(__file_path, "Text=\"复制粘贴\"", "Text=\"Copy-paste a\"")
    replaceStr(__file_path, "Text=\"URL\"", "Text=\"URL\"")
    replaceStr(__file_path, "Text=\"或输入\"", "Text=\"or enter a\"")
    replaceStr(__file_path, "Text=\"搜索查询\"", "Text=\"search query\"")
    replaceStr(__file_path, "Text=\"开始下载\"", "Text=\"to start downloading\"")
    replaceStr(__file_path, "Text=\"按\"", "Text=\"Press\"")
    replaceStr(__file_path, "Text=\"Shift+Enter\"", "Text=\"Shift+Enter\"")
    replaceStr(__file_path, "Text=\"添加多个项目\"", "Text=\"to add multiple items\"")


def AuthSetupView(__file_path):
    replaceStr(__file_path, "Text=\"身份验证\"", "Text=\"Authentication\"")
    replaceStr(__file_path, "Content=\"关闭\"", "Content=\"CLOSE\"")


def RootViewModel(__file_path):
    replaceStr(__file_path, "//await ShowUkraineSupportMessageAsync();", "await ShowUkraineSupportMessageAsync();")
    replaceStr(__file_path, "未能执行应用程序更新", "Failed to perform application update")
    replaceStr(__file_path, "已下载更新，将在您退出时安装",
               "Update has been downloaded and will be installed when you exit")
    replaceStr(__file_path, "立即安装", "INSTALL NOW")
    replaceStr(__file_path, "正在下载{App.Name} v{updateVersion}更新...",
               "Downloading update to {App.Name} v{updateVersion}...")


def AssemblyInfo(__file_path):
    replaceStr(__file_path, "1.10.9", "1.10.8")


if __name__ == '__main__':
    path = r"D:\Download\IDM\YoutubeDownloader-master"

    file_path = path + r"\YoutubeDownloader\Views\Dialogs\SettingsView.xaml"
    SettingView(file_path)

    file_path = path + r"\YoutubeDownloader\Views\Dialogs\DownloadMultipleSetupView.xaml"
    DownloadMultipleSetupView(file_path)

    file_path = path + r"\YoutubeDownloader\Views\Dialogs\DownloadSingleSetupView.xaml"
    DownloadSingleSetupView(file_path)

    file_path = path + r"\YoutubeDownloader\Views\Components\DashboardView.xaml"
    DashboardView(file_path)

    file_path = path + r"\YoutubeDownloader\Views\Dialogs\AuthSetupView.xaml"
    AuthSetupView(file_path)

    file_path = path + r"\YoutubeDownloader\ViewModels\RootViewModel.cs"
    RootViewModel(file_path)
