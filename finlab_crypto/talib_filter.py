from finlab_crypto.strategy import Strategy, Filter
import inspect
import pandas as pd
import numpy as np

def TalibFilter(talib_function_name, condition=None, **additional_parameters):
    from talib import abstract
    import talib
    f = getattr(abstract, talib_function_name)
    ff = getattr(talib, talib_function_name)

    @Filter(condition=condition, **f.parameters, additional_parameters=additional_parameters)
    def ret(ohlcv):
        parameters = {pn: (getattr(ret, pn)) for pn, val in f.parameters.items()}
        try:
            o = f(ohlcv, **parameters)
        except:
            o = ff(ohlcv.close, **parameters)
            if isinstance(o, list) or isinstance(o, tuple):
                o = pd.DataFrame(np.array(o).T, index=ohlcv.index, columns=f.output_names)

        if isinstance(o, np.ndarray):
            o = pd.Series(o, index=ohlcv.index)

        ret.condition
        if len(inspect.getargspec(ret.condition)[0]) == 2:
            signals = ret.condition(ohlcv, o)
        else:
            signals = ret.condition(ohlcv, o, ret.additional_parameters)

        figures = {}
        group = 'overlaps' if f.info['group'] == 'Overlap Studies' else 'figures'
        figures[group] = {f.info['name']: o}

        return signals, figures
    return ret
