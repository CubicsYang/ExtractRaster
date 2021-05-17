# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。

import os

import rasterio as rio;
import rasterio.mask;
from geopandas import *;
from tqdm import tqdm


def read_file(path, file_type):  # path 是指需要提取的文件夹所在路径;file_type是指文件的拓展名;txt格式的文件则输入‘.txt’
    filenames = os.listdir(path)
    filenames1 = []
    for filename in filenames:
        if os.path.splitext(filename)[1] == file_type:
            filenames1.append(filename)
    return filenames1


def extract(shpfilepath, rasterfilepath, outpath):
    # shpdatafile = 'data/grid_1/1.shp'
    # rasterfile = 'data/tif_13.tif'
    # out_file = 'data/1.tif'
    shpdatafile = shpfilepath
    rasterfile = rasterfilepath
    out_file = outpath
    shpdata = GeoDataFrame.from_file(shpdatafile)
    rasterdata = rio.open(rasterfile)

    # 投影变换，使矢量数据与栅格数据投影参数一致
    shpdata = shpdata.to_crs(rasterdata.crs)

    for i in range(0, len(shpdata)):
        # 获取矢量数据的features
        geo = shpdata.geometry[i]
        feature = [geo.__geo_interface__]
        # 通过feature裁剪栅格影像
        out_image, out_transform = rio.mask.mask(rasterdata, feature, all_touched=True, crop=True,
                                                 nodata=rasterdata.nodata)
        # 输出属性信息
        out_meta = rasterdata.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform,
                         "crs": rasterdata.crs}
                        )
        with rasterio.open(out_file, "w", **out_meta) as dest:
            dest.write(out_image)


# 按间距中的绿色按钮以运行脚本
if __name__ == '__main__':
    # path = '/Users/cubics/PycharmProjects/ExtractRaster/data/grid_1'  # 指定文件所在路径
    rasterPath = '/Users/cubics/PycharmProjects/ExtractRaster/raster'
    resultBasePath = '/Users/cubics/PycharmProjects/ExtractRaster/result'
    # year = resultBasePath.split('_')[1]
    pathPres = ['grid_13_1', 'grid_13_2', 'grid_13_5', 'grid_21_1', 'grid_21_2', 'grid_21_5']
    filetype = '.shp'  # 指定文件类型
    # file_names = read_file(path, filetype)
    for pathPre in tqdm(pathPres):
        year = pathPre.split('_')[1]
        file_names = read_file(resultBasePath + '/' + pathPre + 'fenge', filetype)
        for file_name in tqdm(file_names):
            extract(resultBasePath + '/' + pathPre + 'fenge/' + file_name,
                    rasterPath + "/tif_" + year + ".tif",
                    resultBasePath + '/' + pathPre + 'extract/' + os.path.splitext(file_name)[
                        0] + ".tif")

    # for file_name in file_names:
    #     # print(file_name)
    #     print("data/" + file_name)
    #     print("extract/" + os.path.splitext(file_name)[0])
    #     extract("/Users/cubics/PycharmProjects/ExtractRaster/data/grid_1/" + file_name,
    #             "/Users/cubics/PycharmProjects/ExtractRaster/data/tif_13.tif",
    #             "/Users/cubics/PycharmProjects/ExtractRaster/data/extract/" + os.path.splitext(file_name)[0] + ".tif")
    #     print("suc")

    # extract("/Users/cubics/PycharmProjects/ExtractRaster/data/grid_1/" + "1.shp",
    #         "/Users/cubics/PycharmProjects/ExtractRaster/data/tif_13.tif",
    #         "/Users/cubics/PycharmProjects/ExtractRaster/extract/" +"1.tif")
