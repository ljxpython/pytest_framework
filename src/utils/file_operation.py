
"""
@author:李佳欣
@file: file_operation.py
@time: 2021/07/15
"""

'''
对文件的相关操作，可以使用该模块来完成
比如说，删除文件、创建新的文件夹、压缩文件、遍历文件夹、深层遍历文件夹、文件的打包压缩
'''

import os
import shutil
import tarfile
import zipfile


class FileOperation(object):
    def __init__(self):
        pass

    def iterates(self, path):
        '''
        文件夹的浅层遍历,只会遍历第一层
        这个得到的结果是浅层目录
        :param path:
        :return:
        '''
        return os.listdir(path)

    def iterates_feature(self, path, feature):
        '''
        文件夹的浅层遍历,并且把对应的feature list给到
        :param path:
        :param feature:
        :return:
        '''
        return [i for i in os.listdir(path) if i.split(".")[-1] == feature]

    def absolute_iterates(self, path):
        '''
        这个得到该目录下文件的绝对路径
        :param path:
        :return:
        '''
        return [os.path.join(path, i) for i in self.iterates(path)]  # 用一个简单的列表推倒式来完成，比较有成就感

    def filter_dir_or(self, path, feature: list):
        '''
        这个函数专门用来过滤我们需要的东西  该函数，实现的是，包含即可
        比如说，我们要这个文件夹中.jpg 结尾的图片，我们就可以输入一个文件夹和jpg这个参数
        只支持浅层文件夹，深层的暂时没有必要
        :param list_1:
        feature： 这个参数支持列表(todo)
        :return:
        '''
        list_1 = self.absolute_iterates(path)
        list_2 = []
        # 进行切找尾部有feature的东西
        for fac in list_1:
            if fac.split(".")[-1] in feature:
                list_2.append(fac)

        # print(list_2)

        return list_2  # 后期改成一个列表推倒式吧，看着更爽

    def filter_dir_and(self, path, feature: list):
        '''
        这个函数专门用来过滤我们需要的东西  该函数实现的是必须全部包含
        比如说，我们要这个文件夹中.jpg 结尾的图片，我们就可以输入一个文件夹和jpg这个参数
        只支持浅层文件夹，深层的暂时没有必要
        :param list_1:
        feature： 这个参数支持列表(todo)
        :return:
        '''
        list_1 = self.absolute_iterates(path)
        list_2 = []
        # 进行切找尾部有feature的东西
        for fac in list_1:
            if fac.split(".")[-1] in feature:
                list_2.append(fac)

        # print(list_2)

        return list_2  # 后期改成一个列表推倒式吧，看着更爽

    def mkdir(self, path):
        '''
        这个函数，先判断有没有该文件夹，如果没有该文件夹，创建
        支持深层创建
        注意，这里面是创建文件夹而不是文件，如果创建文件还需要另外写一个函数
        创建文件的函数可以先创建，然后用with open来写辅助，这个之后根据需求在完成吧。
        :param path:
        :return:
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass
            # self.logger.info("we had makedir {}".format(path))

        return None

    def move_file(self, old_path, new_path):
        '''
        文件/文件夹的移动或者重命名
        如果new_path 已经存在，就会存放到new_path里面
        如果new_path 不存在，old_path 就会重命名成新的new_path
        :param old_path:
        :param new_path:
        :return:
        '''
        return shutil.move(old_path, new_path)

    def move_floder(self, old_path, new_path):
        '''
        这个文件夹实现的是从一个文件夹中，将文件一个个转移到新文件夹的操作
        :param old_path: 是一个路径，我们会对他进行遍历
        :param new_path: 存放的新路径
        :return:
        '''
        list_1 = self.absolute_iterates(old_path)
        # print(list_1)
        for i in list_1:
            try:
                shutil.move(i, new_path)
            except:
                pass
                # self.logger.info("{} had exist in the path {}".format(i,new_path))

    def move_feature(self, old_path, new_path, feature):
        '''
        这个函数，实现，特定后缀的文件转移
        :param old_path:
        :param new_path:
        :param feature: 比如png   jpg 等特征
        :return:
        '''
        list_1 = []
        for i in self.absolute_iterates(old_path):
            if feature in os.path.splitext(i)[-1]:
                list_1.append(i)
        for i in list_1:
            try:
                shutil.move(i, new_path)
            except:
                pass
                # self.logger.info("{} had exist in the path {}".format(i, new_path))

    def copyfile(self, old_path, new_path):
        '''
        文件对文件
        :param old_path:
        :param new_path:
        :return:
        '''
        return shutil.copyfile(old_path, new_path)

    def copy(self, old_path, new_path):
        '''
        文件对文件夹
        :param old_path:
        :param new_path:
        :return:
        '''
        return shutil.copy(old_path, new_path)

    def remove_file(self, path):
        '''
        文件的递归删除
        :param path:
        :return:
        '''
        return shutil.rmtree(path)

    def del_feature(self, path, feature):
        '''
        删除指定文件夹内，含有特征值的文件
        :param feature:
        :return:
        '''
        # print(self.filter_dir(path,feature))
        for i in self.filter_dir(path, feature):
            os.remove(i)
            # shutil.rmtree(i)

    def zip_packge(self, filename, zipname):
        '''
                下面这个函数是单个文件的压缩
                这个，也对zipfile这个库进行一些说明吧
                参考文献： https://blog.csdn.net/guorong520/article/details/103927707
                注意这句： zip.write（filename[, arcname[, compress_type]]）
        filename代表文件完整路径；arcname代表需要保存的相对路径名称（\frontend\apple.txt），它意味着"apple.txt"在"frontent"目录中
                :param filename:
                :param zipname:
                :return:
        '''
        zf = zipfile.ZipFile(zipname, "a")
        # print(filename)
        os.path.split(filename)
        # print(os.path.split(filename)[-1])

        zf.write(filename, os.path.split(filename)[-1])
        zf.close()

    def zip_all(self, folderPath, compressPathName):
        '''
        这里面注意一个问题，一定不能把你压缩的文件写入到你要遍历的文件夹内，这个会造成一个
        无限遍历的问题，让程序跳不出去
        :param folderPath: 文件夹路径
        :param compressPathName: 压缩包路径 以 .zip 结尾

        :return:
        '''
        zip = zipfile.ZipFile(compressPathName, 'w')
        for path, dirNames, fileNames in os.walk(folderPath):
            fpath = path.replace(folderPath, '')  # replace 字符串的替换，把根目录那块字符替换成空字符串
            # print(fpath)
            for name in fileNames:
                fullName = os.path.join(path, name)

                # name = fpath + '\\' + name
                name = os.path.join(fpath, name)
                zip.write(fullName, name)
        zip.close()

    def tar_packge(self, output_filename, source_dir):
        '''
        文件以.tar.gz 结尾
        :param output_filename:  文件以.tar.gz 结尾
        :param source_dir:
        :return:
        '''
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            tar.close()

    def sort_feature(self, path, feature, revers=False):
        '''
        将文件夹中，浅层的文件遍历，排序，计入列表中
        默认升序
        :param path: 路径
        :param feature: jpg、png
        :return:
        '''
        list_1 = self.filter_dir(path, feature)
        list_1.sort(reverse=revers)
        return list_1

    def write_file_a(self, path, content):
        '''
        这个是写入文件内容的操作，只有追加，目前来说，只需要追加即可。
        :param path: 写入文件路径的地址
        :param content:
        :return:
        '''
        with open(path, mode="a", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")

    def write_file_w(self, path, content):
        '''
        这个是写入文件内容的操作，这个会覆盖之前写入的文件。
        :param path: 写入文件路径的地址
        :param content:
        :return:
        '''
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")

    def split(self, path):
        '''
        这边给一个路径，就会得到他的文件夹或者文件名字
        :param path:
        :return:
        '''
        return os.path.split(path)[-1]

    def file_name(self, path, feature):
        '''
        这个函数可以实现，给一个文件夹,根据对应的特征jpg png mp4 把文件的名字拿到
        比如file 目录有 a.mp4 b.mp4 那么我们就会得到[a,b]
        :param path: 这个是一个文件夹
        :return: 返回该文件夹中有特征值的文件名字
        '''
        return [os.path.splitext(os.path.split(i)[1])[0] for i in self.filter_dir(path, feature)]

    def listdir(self, path):
        '''
        这个函数，实现将一个文件夹下面所有的文件夹抓取出来
        :param path:
        :return:
        '''
        list_1 = []
        for i in os.listdir(path):
            # print(os.path.join(path,i))
            if os.path.isdir(os.path.join(path, i)):
                list_1.append(os.path.join(path, i))
            else:
                pass
        return list_1


file_opreator = FileOperation()

if __name__ == '__main__':
    fo = FileOperation()
