import pandas as pd
import glob
import gc
import os

file_pathr = r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\DATA1\*.csv"  #45个longterm数据所在的文件夹（注意，此文件夹中只放45个longterm文件）
file_pathw= r'D:\MLAP\PRT2\write'
csv_listr = glob.glob(file_pathr)
for i in range(0, len(csv_listr)):
    with open(csv_listr[i]) as r:
        table1 = pd.read_csv(r)  #read long term data file
        table2 = table1[table1['determination_position'].isin([1])]  # 筛选出用移动数据定位的数据
        del table1  # 清除定义过的变量名
        gc.collect()  # 使用此代码可删除内存中所有的无效变量
        table3 = table2.drop(labels=['loading_state', 'loading_state_update', 'altitude', 'signal_quality_satellite',
                                     'determination_position', 'GNSS_velocity', 'timestamp_measure_position',
                                     'timestamp_transfer', 'movement_state', 'timestamp_measure_movement_state',
                                     'timestamp_index', 'provider'], axis=1)
        del table2  # 清除定义过的变量名
        gc.collect()  # 使用此代码可删除内存中所有的无效变量
        # 删除不需要的数据列

        # max_amount = float(table3['signal_quality_hdop'].max())
        # min_amount = float(table3['signal_quality_hdop'].min())
        table_goodsignal = table3[(table3['signal_quality_hdop'] <= 35)]

        table_goodsignal.loc[:, 'signal_quality'] = (35 - table_goodsignal['signal_quality_hdop'])
        lat2 = table_goodsignal['latitude']
        lon2 = table_goodsignal['longitude']
        quality = table_goodsignal["signal_quality"]
        del table3,table_goodsignal  # 清除定义过的变量名
        gc.collect()  # 使用此代码可删除内存中所有的无效变量
        dict2 = {'lat': lat2.values, 'lon': lon2.values,
                 "quality": quality.values}  # 利用前两个series文件的值创建字典，用于创建后续的dataframe
        df_lat_lon = pd.DataFrame(dict2, index=lat2.index)

        df_lat_lon.to_csv(os.path.join(file_pathw,'GNSSPreProcessed_' + str(i+17) + '.csv'),index=None)#单个生成并输出csv文件
        del dict2,df_lat_lon
        gc.collect()



