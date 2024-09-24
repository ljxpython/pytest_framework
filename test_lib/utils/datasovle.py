"""


数据处理：
    如何添加数据
    如何统计数据
    如何过滤数据

    需要支持链式调用

    统计某一字段的P99 平均值
    根据某一个字段的某一个值进行过滤，统计总数，除了这个值的数量和这个值的数量
    过滤掉无用的字段，返回需要的数据

    一个真实的业务场景举例：
    统计表格中某一列的某个值出现的概率，及某一列的平均水平，99分位数，将其写入到一个csv文件中
    上述功能在下面的函数中中，都变成了原子能力，业务需求放在业务逻辑的模块进行书写。
"""

import os
from typing import Union

import numpy as np
import pandas as pd

from conf.constants import logs_dir
from test_lib.utils.log_moudle import logger


class DataSovle(object):
    def __init__(self):
        self.df: pd.DataFrame = pd.DataFrame()
        pass

    # @property
    def read_csv(self, *args, **kwargs):
        """
        可以直接给一个文件目录，也可以给一个或者多个文件地址
        读取csv文件，多个的话会合成为一个文件
        :param args:
        :param kwargs:
        :return:
        """
        # logger.info(*args)
        ## 判断args是str还是list，如果是str则走dir模式，如果是list则走file模式
        # logger.info(mode_a)
        if isinstance(*args, str):
            res = self.read_csv_dir_mode(*args, **kwargs)
        elif isinstance(*args, (list, tuple)):
            res = self.read_csv_file_mode(*args, **kwargs)
        else:
            raise ValueError(f" we nead mode deliver files or dir ")
        return res

    def read_csv_dir_mode(self, *args, **kwargs):
        all_data_frame = pd.DataFrame()
        # logger.info(args)
        all_csv_list = os.listdir(args[0])  # get csv list
        for i in all_csv_list:
            if os.path.splitext(i)[1] != ".csv":
                all_csv_list.remove(i)
        # logger.info(all_csv_list)
        for single_csv in all_csv_list:
            single_data_frame = pd.read_csv(
                os.path.join(args[0], single_csv), sep=",", encoding="utf-8"
            )
            #     print(single_data_frame.info())
            if single_csv == all_csv_list[0]:
                # print(single_csv)
                all_data_frame = single_data_frame
            else:  # concatenate all csv to a single dataframe, ingore index
                # print(single_csv)
                all_data_frame = pd.concat(
                    [all_data_frame, single_data_frame], ignore_index=True
                )
        self.df = all_data_frame
        # self.df_info()
        return all_data_frame

    def read_csv_file_mode(self, *args, **kwargs):
        args = list(set(args[0]))
        ## 声明一个空的dataframe
        all_data_frame = pd.DataFrame()
        # logger.info(args)
        for file_path in args:
            single_data_frame = pd.read_csv(file_path)
            if args.index(file_path) == 0:
                all_data_frame = single_data_frame
            else:
                all_data_frame = pd.concat(
                    objs=[all_data_frame, single_data_frame], ignore_index=True
                )
        # print(all_data_frame.index)
        # print(all_data_frame.head())
        self.df = all_data_frame
        return all_data_frame

    def createdaframe(self, dict_content):
        return pd.DataFrame(dict_content)

    # def sav

    def save_file(
        self,
        file: str = os.path.join(logs_dir, "tests.csv"),
        df: Union[dict, pd.DataFrame] = None,
    ):
        """
        其实这块应该一步到位，应该写一个函数，判断df是字典还是dataframe，如果都不是报异常
        如果是字典，那么按照字典的方式处理，如果是dataframe就按照dataframe的方式处理

        先判断文件在不在，如果不在，那么mode="w"
        如果存在，文件mode="a+",header=None
        :param file:
        :param df:
        :return:
        """
        if os.path.exists(file):
            if isinstance(df, pd.DataFrame):
                df.to_csv(file, mode="a+", header=None, index=False)
            elif isinstance(df, dict):
                df = pd.DataFrame(df)
                df.to_csv(file, mode="a+", header=None, index=False)
            else:
                raise ValueError("expect dict or dataframe")
        else:
            if isinstance(df, pd.DataFrame):
                df.to_csv(file, mode="w", index=False)
            elif isinstance(df, dict):
                df = pd.DataFrame(df)
                df.to_csv(file, mode="w", index=False)
            else:
                raise ValueError("expect dict or dataframe")

    def df_dtypes(self, df: pd.DataFrame = pd.DataFrame()):
        """
        展示表的列值有哪些
        :param df:
        :return:
        """

    def df_describe(self, df: pd.DataFrame = pd.DataFrame()):
        """
        表的概览
        行数，列数，列索引，列非空值个数，列类型，等等
        :param df:
        :return:
        """
        # logger.info(df.describe())
        if not df.empty:
            logger.info(df.describe())
        else:
            logger.info(self.df.describe())

    def df_info(self, df: pd.DataFrame = pd.DataFrame()):
        """
        表的概览
        行数，列数，列索引，列非空值个数，列类型，等等
        :param df:
        :return:
        """
        # logger.info(df.describe())
        if not df.empty:
            logger.info(df.info)
        else:
            logger.info(self.df.info)

    def df_mean(self, colunms):
        """
        拿到某一列的平均值
        :return:
        """
        np.mean(self.df.loc[:, colunms])
        logger.info(f"colunms :{colunms}  mean:  {np.mean(self.df.loc[:,colunms])}")
        return np.mean(self.df.loc[:, colunms])

    def df_percentile(self, colunms, num):
        """
        拿到某一列的分位数
        :return:
        """
        logger.info(
            f"colunms:{colunms} percentile:{num}  vaulue:  {np.percentile(self.df.loc[:,colunms],num)}"
        )
        return np.percentile(self.df.loc[:, colunms], num)

    def df_filter_not(
        self,
        columns,
        params,
    ):
        """
        过滤掉不符合要求的某一个的某个值
        :return:
        """
        self.df = self.df.loc[(self.df.loc[:, columns] != params)]
        return self

    def df_filter_is(
        self,
        columns,
        params,
    ):
        """
        过滤掉不符合要求的某一个的某个值
        :return:
        """
        # logger.info(datasolve.df.columns)
        self.df = self.df.loc[(self.df.loc[:, columns] == params)]
        return self

    def df_count_prentage(self, columns, params):
        """
        统计某一列中，某个字段出现的概率
        :return:
        """
        # logger.info(self.df.loc[:,columns].value_counts()[params])
        #
        # logger.info(self.df.loc[:,columns].count())
        res = (
            self.df.loc[:, columns].value_counts()[params]
            / self.df.loc[:, columns].count()
        )
        # logger.info(self.df.loc[:,columns].sum())
        # logger.info(self.df.loc[:,columns].head())
        logger.info(f"列名:{columns} 字段:{params} 出现的概率为{res}")
        return res


datasolve = DataSovle()
if __name__ == "__main__":
    pass
