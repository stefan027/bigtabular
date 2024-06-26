# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_data.ipynb.

# %% ../nbs/01_data.ipynb 2
from __future__ import annotations
from fastai.torch_basics import *
from fastai.data.all import *
from .core import *
import dask.dataframe as dd

# %% auto 0
__all__ = ['DaskDataLoaders']

# %% ../nbs/01_data.ipynb 7
class DaskDataLoaders(DataLoaders):
    "Basic wrapper around `DaskDataLoader` with factory methods for large tabular datasets with Dask"
    @classmethod
    @delegates(TabularDask.dataloaders, but=["dl_type", "dl_kwargs"])
    def from_ddf(cls, 
        ddf:dd.DataFrame, # A Dask dataframe
        path:str|Path='.', # Location of `df`, defaults to current working directory
        procs:list=None, # List of `TabularProc`s
        cat_names:list=None, # Column names pertaining to categorical variables
        cont_names:list=None, # Column names pertaining to continuous variables
        y_names:list=None, # Names of the dependent variables
        y_block:TransformBlock=None, # `TransformBlock` to use for the target(s)
        train_mask_func:callable=None, # A function that creates a train/validation mask over a DataFrame
        **kwargs
    ):
        "Create `TabularDataLoaders` from `df` in `path` using `procs`"
        if cat_names is None: cat_names = []
        if cont_names is None: cont_names = list(set(df)-set(L(cat_names))-set(L(y_names)))
        train_mask_func = RandomTrainMask() if train_mask_func is None else train_mask_func
        to = TabularDask(ddf, procs, cat_names, cont_names, y_names, train_mask_func=train_mask_func, y_block=y_block)
        return to.dataloaders(path=path, **kwargs)

    @classmethod
    def from_csv(cls,
        csv:str|Path|io.BufferedReader, # A csv of training data
        *args, skipinitialspace=True, header='infer', dtype_backend=None, storage_options=None, **kwargs
    ):
        "Create `TabularDataLoaders` from `csv` file in `path` using `procs`"
        return cls.from_ddf(dd.read_csv(csv, *args, skipinitialspace=True, header=header,
                                        dtype_backend=dtype_backend, storage_options=storage_options), **kwargs)

    def test_dl(self, 
        test_items, # Items to create new test `TabDataLoader` formatted the same as the training data
        rm_type_tfms=None, # Number of `Transform`s to be removed from `procs`
        process:bool=True, # Apply validation `TabularProc`s to `test_items` immediately
        inplace:bool=False, # Keep separate copy of original `test_items` in memory if `False`
        **kwargs
    ):
        "Create test `DaskDataLoader` from `test_items` using validation `procs`"
        to = self.train_ds.new(test_items)
        if process: to.process()
        return self.valid.new(to)

TabularDask._dbunch_type = DaskDataLoaders
DaskDataLoaders.from_csv = delegates(to=DaskDataLoaders.from_ddf)(DaskDataLoaders.from_csv)
