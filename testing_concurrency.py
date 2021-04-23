import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import nibabel as nib
from os import path
import os.path
from functools import partial
from tic_toc import tic, toc
from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import time

def load_image(path):
    return nib.load(path).get_fdata()

def flatten_image(image):
    return image.flatten()

def test_multiprocessing(func, iterable, num_processes, **kwargs):
    results = []
    with multiprocessing.Pool(num_processes) as pool:
        for result in pool.map(partial(func, **kwargs), iterable):
            results.append(result)
    return results

def test_multithreading(func, iterable, num_threads, **kwargs):
    results = []
    with ThreadPoolExecutor(num_threads) as executor:
        for result in executor.map(partial(func, **kwargs), iterable):
            results.append(result)
    return results

def main(func, iterable, concurrency_order, **kwargs):
    tic()
    times = {'multiprocessing':{}, 'multithreading':{}}
    results = []
    for i in tqdm(concurrency_order, desc='Concurrency order - multiprocessing'):
        results.append(test_multiprocessing(func, iterable, i, **kwargs))
        times['multiprocessing'][i] = toc(restart=True, print_to_screen=False)
    time.sleep(2)
    results = []
    for i in tqdm(concurrency_order, desc='Concurrency order - multithreading'):
        results.append(test_multithreading(func, iterable, i, **kwargs))
        times['multithreading'][i] = toc(restart=True, print_to_screen=False)
    
    times_df = pd.DataFrame(times)
    times_df.to_csv(f'~/speed_tests/{func.__name__}.csv')
    print(results)
    print(times_df)

if __name__ == '__main__':
    image_path = 'path/to/image.nii.gz'
    func              = load_image
    iterable          = [image_path]*20
    concurrency_order = list(range(1,21)) + [25]
    kwargs            = {}
    main(func, iterable, concurrency_order, **kwargs)
    
    image = load_image(image_path)
    func              = flatten_image
    iterable          = [image]*20
    concurrency_order = list(range(1,21)) + [25]
    kwargs            = {}
    main(func, iterable, concurrency_order, **kwargs)
