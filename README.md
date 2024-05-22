# BigTabular


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This repo replicates much the functionality of the tabular data
application in the [fastai](https://docs.fast.ai/) library to work with
larger-than-memory datasets. Pandas, which is used for data
transformations in `fastai.tabular`, is replaced with [Dask
DataFrames](https://docs.dask.org/en/stable/dataframe.html).

Most of the Dask implementations were written as they were needed for a
personal project, but then refactored to match the fastai API more
closely. The flow of the Jupyter notebooks follows those from
`fastai.tabular` closely and most of the examples and tests were
replicated.

## When not to use BigTabular

Don’t use this library when you don’t need to use Dask. The [Dask
website](https://docs.dask.org/en/stable/dataframe.html) gives the
following guidance:

> Dask DataFrames are often used either when …
>
> 1.  Your data is too big
> 2.  Your computation is too slow and other techniques don’t work
>
> You should probably stick to just using pandas if …
>
> 1.  Your data is small
> 2.  Your computation is fast (subsecond)
> 3.  There are simpler ways to accelerate your computation, like
>     avoiding .apply or Python for loops and using a built-in pandas
>     method instead.

## Install

``` sh
pip install bigtabular
```

## How to use

Refer to the [tutorial](tutorial.html) for a more detailed usage
example.

Get a Dask DataFrame:

``` python
path = untar_data(URLs.ADULT_SAMPLE)
ddf = dd.from_pandas(pd.read_csv(path/'adult.csv'))
ddf.head()
```

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | age | workclass        | fnlwgt | education   | education-num | marital-status     | occupation      | relationship  | race               | sex    | capital-gain | capital-loss | hours-per-week | native-country | salary |
|-----|-----|------------------|--------|-------------|---------------|--------------------|-----------------|---------------|--------------------|--------|--------------|--------------|----------------|----------------|--------|
| 0   | 49  | Private          | 101320 | Assoc-acdm  | 12.0          | Married-civ-spouse | \<NA\>          | Wife          | White              | Female | 0            | 1902         | 40             | United-States  | \>=50k |
| 1   | 44  | Private          | 236746 | Masters     | 14.0          | Divorced           | Exec-managerial | Not-in-family | White              | Male   | 10520        | 0            | 45             | United-States  | \>=50k |
| 2   | 38  | Private          | 96185  | HS-grad     | NaN           | Divorced           | \<NA\>          | Unmarried     | Black              | Female | 0            | 0            | 32             | United-States  | \<50k  |
| 3   | 38  | Self-emp-inc     | 112847 | Prof-school | 15.0          | Married-civ-spouse | Prof-specialty  | Husband       | Asian-Pac-Islander | Male   | 0            | 0            | 40             | United-States  | \>=50k |
| 4   | 42  | Self-emp-not-inc | 82297  | 7th-8th     | NaN           | Married-civ-spouse | Other-service   | Wife          | Black              | Female | 0            | 0            | 50             | United-States  | \<50k  |

</div>

</div>

Create dataloaders. Some of the columns are continuous (like age) and we
will treat them as float numbers we can feed our model directly. Others
are categorical (like workclass or education) and we will convert them
to a unique index that we will feed to embedding layers. We can specify
our categorical and continuous column names, as well as the name of the
dependent variable in
[`DaskDataLoaders`](https://stefan027.github.io/bigtabular/data.html#daskdataloaders)
factory methods:

``` python
dls = DaskDataLoaders.from_csv(path/'adult.csv', path=path, y_names="salary",
    cat_names = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race'],
    cont_names = ['age', 'fnlwgt', 'education-num'],
    procs = [DaskCategorify, DaskFillMissing, DaskNormalize])
```

Create a `Learner`:

``` python
learn = dask_learner(dls, metrics=accuracy)
```

Train the model for one epoch:

``` python
learn.fit_one_cycle(1)
```

<style>
    /* Turns off some styling */
    progress {
        /* gets rid of default border in Firefox and Opera. */
        border: none;
        /* Needs to be in here for Safari polyfill so background images work as expected. */
        background-size: auto;
    }
    progress:not([value]), progress:not([value])::-webkit-progress-bar {
        background: repeating-linear-gradient(45deg, #7e7e7e, #7e7e7e 10px, #5c5c5c 10px, #5c5c5c 20px);
    }
    .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
        background: #F44336;
    }
</style>

<div>

| epoch | train_loss | valid_loss | accuracy | time  |
|-------|------------|------------|----------|-------|
| 0     | 0.361596   | 0.356745   | 0.834383 | 01:07 |

</div>

We can then have a look at some predictions:

``` python
learn.show_results()
```

<style>
    /* Turns off some styling */
    progress {
        /* gets rid of default border in Firefox and Opera. */
        border: none;
        /* Needs to be in here for Safari polyfill so background images work as expected. */
        background-size: auto;
    }
    progress:not([value]), progress:not([value])::-webkit-progress-bar {
        background: repeating-linear-gradient(45deg, #7e7e7e, #7e7e7e 10px, #5c5c5c 10px, #5c5c5c 20px);
    }
    .progress-bar-interrupted, .progress-bar-interrupted::-webkit-progress-bar {
        background: #F44336;
    }
</style>

<div>

|     | workclass | education | marital-status | occupation | relationship | race | education-num_na | age       | fnlwgt    | education-num | salary | salary_pred |
|-----|-----------|-----------|----------------|------------|--------------|------|------------------|-----------|-----------|---------------|--------|-------------|
| 0   | 5         | 8         | 3              | 0          | 6            | 5    | 1                | 0.761567  | -0.839855 | 0.750651      | 1      | 1           |
| 1   | 7         | 6         | 3              | 9          | 6            | 3    | 2                | 0.249361  | -1.020247 | -0.033453     | 0      | 0           |
| 2   | 5         | 12        | 3              | 4          | 1            | 5    | 1                | 0.542050  | 1.311756  | -0.425505     | 1      | 0           |
| 3   | 5         | 10        | 3              | 0          | 1            | 5    | 2                | -0.628705 | -1.276339 | -0.033453     | 1      | 0           |
| 4   | 5         | 1         | 3              | 8          | 1            | 5    | 2                | -0.043327 | -0.186926 | -0.033453     | 1      | 0           |
| 5   | 5         | 12        | 5              | 7          | 4            | 3    | 1                | -0.921394 | 5.277619  | -0.425505     | 0      | 0           |
| 6   | 5         | 12        | 4              | 0          | 4            | 3    | 2                | -0.701878 | 10.226764 | -0.033453     | 0      | 0           |
| 7   | 6         | 16        | 3              | 0          | 1            | 5    | 2                | 0.176189  | -0.367905 | -0.033453     | 0      | 1           |
| 8   | 5         | 10        | 3              | 5          | 1            | 5    | 1                | 0.468878  | 0.497894  | 1.142703      | 1      | 1           |

</div>
