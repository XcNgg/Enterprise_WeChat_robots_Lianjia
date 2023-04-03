import pandas as pd
import time
def save_excel(dic_data):
    """
    :param dic_data: 数据列表
    :return:  保存的文件名称
    """
    print(dic_data)
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(dic_data))
    # 指定生成的Excel表格名称
    file_name = 'lianjia_' + time.strftime("%Y%m%d_%H", time.localtime())
    file_path = pd.ExcelWriter(f'./data/{file_name}.xlsx')
    # file_csv_path = pd.read_csv("compound.csv")
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # pf.to_csv(file_csv_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()
    return file_name