Welcome to fastgs
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Introduction

**This library is currently in *alpha*, neither the functionality nor
the API is stable**

This library provides geospatial multi-spectral image support for
fastai. FastAI already has extensive support for RGB images in the
pipeline. I try to achieve feature parity for multi-spectral images with
this library, specifically in the context of Sentinel 2 geospatial
imaging.

## Sample Notebooks

You can find demo usage of the library at

1.  On the kaggle [38-cloud/95-cloud landsat
    dataset](https://www.kaggle.com/code/restlessronin/fastgs-cloud-segmentation/)
2.  With a private [Sentinel 2
    dataset](https://www.kaggle.com/code/restlessronin/ld-2-trn-base)

These are boths works in progress and purposely designed to display the
features of the library.

## Install

``` sh
pip install -Uqq fastgs
```

``` sh
conda install -c restlessronin fastgs
```

## How to use

The low-level functionality is wrapped into a class that loads sets of
Sentinel 2 channels into a multi-spectral tensor (a
[`TensorImageMS`](https://restlessronin.github.io/fastgs/vision.core.html#tensorimagems)
subclass of `fastai` `TensorImage` which itself is a subclass of the
`pytorch` `Tensor`).

``` python
from fastgs.multispectral import *
```

The following code creates a class that can load 11 Sentinel 2 channels
into a
[`TensorImageMS`](https://restlessronin.github.io/fastgs/vision.core.html#tensorimagems).

``` python
from fastgs.vision.testio import * # defines read_multichan_files_as_tensor

sentinel2 = createSentinel2Descriptor()

snt_12 = MSData(
    sentinel2,
    ["B02","B03","B04","B05","B06","B07","B08","B8A","B11","B12","AOT"],
    [sentinel2.rgb_combo["natural_color"], ["B07","B06","B05"],["B12","B11","B8A"],["B08"]],
    get_channel_filenames,
    read_multichan_files
)
```

The second parameter is a list of 4 channel sets that are minimally
required to visualize all the individual channels.

``` python
img_12 = snt_12.load_image(66)
img_12.show()
```

    [<AxesSubplot:>, <AxesSubplot:>, <AxesSubplot:>, <AxesSubplot:>]

![](index_files/figure-gfm/cell-4-output-2.png)

## Acknowledgements

This library is inspired by the following notebooks (and related works
by the authors)

- https://dpird-dma.github.io/blog/MSData-image-classification-Transfer-Learning/
- https://github.com/cordmaur/Fastai2-Medium/blob/master/01_Create_Datablock.ipynb
