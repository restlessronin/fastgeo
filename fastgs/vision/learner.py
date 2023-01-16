# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/21a_vision.learner.ipynb.

# %% ../../nbs/21a_vision.learner.ipynb 1
from __future__ import annotations

# %% auto 0
__all__ = ['show_results', 'plot_top_losses']

# %% ../../nbs/21a_vision.learner.ipynb 3
from fastai.vision.all import *
from .core import *

# %% ../../nbs/21a_vision.learner.ipynb 6
def _get_sample_ctxs(nimgs: int, nsamples: int, mskovl: bool, title: str=None, figsize=None):
    nrows = 2 * nsamples if mskovl else nsamples
    ncols = nimgs if mskovl else nimgs + 2

    ctxs = get_grid(nrows * ncols, nrows, ncols, figsize=figsize, title=title)
    chksize = 2 * nimgs if mskovl else nimgs + 2
    return [ctxs[pos : pos + chksize] for pos in range(0, len(ctxs), chksize)]

# %% ../../nbs/21a_vision.learner.ipynb 7
def _show_one_result(img: TensorImageMS, msk: TensorMask, out: TensorMask, row, mskovl: bool, **kwargs):
    if mskovl:
        rowl: int = len(row) // 2
        return [msk.show(ctx=c, **kwargs) for c in img.show(ctxs=row[:rowl],**kwargs)] + [out.show(ctx=c,**kwargs) for c in img.show(ctxs=row[rowl:],**kwargs)]
    else:
        nimgs: int = img.num_images()
        return img.show(ctxs=row[:nimgs],**kwargs) + [msk.show(ctx=row[nimgs],title="Target",**kwargs)] + [out.show(ctx=row[nimgs+1],title="Prediction",**kwargs)]

# %% ../../nbs/21a_vision.learner.ipynb 17
@typedispatch
def show_results(x:TensorImageMS, y:TensorMask, samples, outs, ctxs=None, max_n=6,
                 nrows:int=None, ncols:int=None, figsize=None, mskovl:bool=True, **kwargs):
    assert nrows is None and ncols is None and ctxs is None
    rwcx = _get_sample_ctxs(x.num_images(), min(len(samples),max_n), mskovl, figsize)
    imgs,msks,otps = samples.itemgot(0),samples.itemgot(1),outs.itemgot(0)
    return [_show_one_result(img, msk, otp[0], row, mskovl, **kwargs) for img,msk,otp,row in zip(imgs, msks, outs, rwcx)]

# %% ../../nbs/21a_vision.learner.ipynb 19
@typedispatch
def plot_top_losses(x:TensorImageMS, y:TensorMask, samples, outs, raws, losses, nrows=None, ncols=None, figsize=None, mskovl: bool=True, **kwargs):
    assert nrows is None and ncols is None
    rwcx = _get_sample_ctxs(x.num_images(), len(samples), mskovl, figsize)
    [_show_one_result(s[0], s[1], o[0], row, mskovl, **kwargs) for row,s,o,l in zip(rwcx, samples, outs, losses)]

# %% ../../nbs/21a_vision.learner.ipynb 22
@patch
def fastgs_reinit_weights(self:nn.Conv2d, reweight:str=None):
    w = self.weight.data
    if reweight in ["avg","avgall"]:
        avg = torch.mean(w[:,:3],1,True)
        if reweight == "avg":
            w[:,3:] = avg
        else:
            w = avg
        w = w * (3.0 / w.shape[1])
