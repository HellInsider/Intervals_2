import os
from typing import List, Tuple
from matplotlib import pyplot as plt
from interval import Interval
from linear_regression import LinearRegression, Plotter
from numpy import random as rnd
from numpy import linspace


def is_float(value: str) -> bool:
    if value is None:
        return False
    
    try:
        float(value)
        return True
    except:
        return False


class DataSample:
    kPlus05 = 0,
    kPlus025 = 1,
    kMinus025 = 2,
    kMinus05 = 3,
    kZero = 4,

    _kDict = {
        kPlus05: '+0_5V',
        kMinus05: '-0_5V',
        kZero: 'ZeroLine'
    }

    @staticmethod
    def to_str(data_sample: int) -> str:
        return DataSample._kDict[data_sample]


class IntervalDataBuilder:
    def __init__(self, working_dir: str) -> None:
        self.working_dir = working_dir
        self.rnd = rnd.default_rng(42)

    def get_eps(self) -> float:
        return 1.0 / (1 << 14) * 100.0

    def load_sample(self, filename: str) -> Tuple[List[float], List[float], List[float]]:
        with open(f'{self.working_dir}\\{filename}') as f:
            #stop_position_str = f.readline()
            #stop_position = int(stop_position_str[stop_position_str.index('=') + 1:])
            str=-1
            data = []
            deltas = []
            errs = []
            for fileline in f.readlines():
                str +=1
                if(str <2) : 
                    continue
                numbers = fileline.split(',')
                floats = [float(number) for number in numbers if is_float(number)]

                data.append(floats[0])
                deltas.append(floats[1])
                errs.append(floats[2])
            
            return data, deltas, errs
        
    def load_data(self, data_sample: DataSample, sample_idx: int) -> Tuple[List[float], List[float]]:
        #data_subdir_name = DataSample.to_str(data_sample)
        #data = self.load_sample(f'{data_subdir_name}\\{data_subdir_name}_{sample_idx}.txt')

       # data, deltas, errs = 

        #deltas_subdir_name = DataSample.to_str(DataSample.kZero)
        #deltas = self.load_sample(f'{deltas_subdir_name}\\{deltas_subdir_name}_{sample_idx}.txt')

        return self.load_sample(f'poly_{sample_idx}.csv')
        
    def make_intervals(self, point_sample: List[float]) -> List[Interval]:
        eps = self.get_eps()
        return [Interval(x - eps, x + eps) for x in point_sample]
    

def median(sample: List[float]) -> float:
    return sorted(sample)[(len(sample) >> 1) + 1]


def main():
    working_dir = os.getcwd()
    working_dir = working_dir[:working_dir.rindex('')]
    database_dir = working_dir + '\\data\\'

    dataBuilder = IntervalDataBuilder(database_dir)

    data, deltas = [], []

    i=1
    samples = []
    samples_err = []
    dataArr, deltaArr = [], []
  
    
    while i<10:
        data, delta, sample_err = dataBuilder.load_data(DataSample.kPlus05, i)
        dataArr.append(data)
        deltaArr.append(delta)
        #dataArr+=data
        #deltaArr+=delta

        samples_err.append(sample_err)
        sample = [x_k - delta_k for x_k, delta_k in zip(data, sample_err)]
        #sample = [x_k - delta for x_k, delta in zip(data, delta)]
        samples.append(sample)
       
        
        sample_name = "sampleY"+str(i)
        ys = [Interval(x_k, x_k - err_k) for x_k, err_k in zip(data, sample_err)]
        #ys = [Interval(x_k, z_k) for x_k, z_k in zip(data, delta)]
        xs = linspace(-0.5, 0.5, len(ys))
        
        print(f'Jaccard Index of {sample_name}: {Interval.jaccard_index(ys)}')

        regression = LinearRegression(xs, ys)
        regression.build_point_regression()
        regression.build_inform_set()

        plotter = Plotter()
        plotter.plot_sample(xs, ys, True, sample_name)
        plotter.plot(regression, sample_name)

        plotter.plot_corridor(regression, predict=True, title=sample_name)

        points = [
            Plotter.Point(regression.regression_params[1], regression.regression_params[0], 'point regression')
            ]
        plotter.plot_inform_set(regression.inform_set, points, sample_name)
        i+=1


    # data, deltas = dataBuilder.load_data(DataSample.kPlus05, 0)
    # sample = [x_k - delta_k for x_k, delta_k in zip(data, deltas)]

    # dataP05, deltasP05 = dataBuilder.load_data(DataSample.kPlus05, 0)
    # dataP025, deltasP025 = dataBuilder.load_data(DataSample.kPlus025, 0)
    # dataM025, deltasM025 = dataBuilder.load_data(DataSample.kMinus025, 0)
    # dataM05, deltasM05 = dataBuilder.load_data(DataSample.kMinus05, 0)

    # sampleP05 = [x_k - d_k for x_k, d_k in zip(dataP05, deltasP05)]
    # sampleP025 = [x_k - d_k for x_k, d_k in zip(dataP025, deltasP025)]
    # sampleM025 = [x_k - d_k for x_k, d_k in zip(dataM025, deltasM025)]
    # sampleM05 = [x_k - d_k for x_k, d_k in zip(dataM05, deltasM05)]

    # sampleP05_err = [x_k for x_k in dataP05]
    # sampleP025_err = [x_k for x_k in dataP025]
    # sampleM025_err = [x_k  for x_k in dataM025]
    # sampleM05_err = [x_k for x_k in dataM05]

    #xs = [-0.5, -0.25, 0.25, 0.5]

    #sampels = [sampleM05, sampleM025, sampleP025, sampleP05]

    #ys_1 = [Interval(min(sample), max(sample)) for sample in samples]
    # ys_1 = [Interval(min(sample), max(sample)) for sample in samples]
    # ys_2 = []
    # for sample in samples:
    #     med = median(sample)
    #     ys_2.append(Interval(med - dataBuilder.get_eps(), med + dataBuilder.get_eps()))
    # #ys_3 = [Interval(min(sample), max(sample)) for sample in samples_err]
    # ys_3 = [Interval(min(sample), max(sample)) for sample in samples_err]

    # for ys, sample_name in zip([ys_1, ys_2, ys_3], ['Y1', 'Y2', 'Y3']):
    #     xs = linspace(-0.5, 0.5, len(ys))
    #     print(f'Jaccard Index of {sample_name}: {Interval.jaccard_index(ys)}')

    #     regression = LinearRegression(xs, ys)
    #     regression.build_point_regression()
    #     regression.build_inform_set()

    #     plotter = Plotter()
    #     plotter.plot_sample(xs, ys, True, sample_name)
    #     plotter.plot(regression, sample_name)

    #     plotter.plot_corridor(regression, predict=True, title=sample_name)

    #     points = [
    #         Plotter.Point(regression.regression_params[1], regression.regression_params[0], 'point regression')
    #         ]
    #     plotter.plot_inform_set(regression.inform_set, points, sample_name)


if __name__ == '__main__':
    main()
