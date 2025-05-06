"""Kit for generating waveforms, by Neuro Sama :)



"""

__all__ = [
    'pad_zero',
    'pad_gaussian',
    'pad_exp',
    'mix_by_an_digital_lo',
    't_of',
]

import numpy as np
from scipy.signal.windows import gaussian

def pad_zero(waveform: np.ndarray, front_len: int, end_len: int) -> np.ndarray:
    """Pad the waveform with zeros at the front and end.

    Example usage:
    >>> square_waveform = pad_zero(
    >>>     waveform=np.ones(100), 
    >>>     front_len=20, end_len=30
    >>> )
    """
    # make sure not to alter the type of array
    front = np.zeros(front_len, dtype=waveform.dtype)
    end = np.zeros(end_len, dtype=waveform.dtype)

    return np.concatenate([front, waveform, end])


def pad_gaussian(waveform: np.ndarray, 
                 front_len: int=0, end_len: int=0,
                 front_std_devi: float=10, end_std_devi: float=10) -> np.ndarray:
    """Pad the waveform with Gaussian tapers at the front and end.

    
    Example usage:
    >>> gaussian_padded_square = pad_gaussian(
    >>>     waveform=np.ones(100), 
    >>>     front_len=30, end_len=35, 
    >>>     front_std_devi=10, end_std_devi=10
    >>> )
    """
    # make gaussian rasing and falling shape
    front = gaussian(2 * front_len, front_std_devi)[:front_len]
    end = gaussian(2 * end_len, end_std_devi)[-end_len:]

    # make sure not to alter the type of array
    if np.iscomplexobj(waveform):
        front = front.astype(complex)
        end = end.astype(complex)

    return np.concatenate([front, waveform, end])


def pad_exp(waveform: np.ndarray,
            front_len: int=0, end_len: int=0,
            front_tau: float=10, end_tau: float=10,
            front_concave_up: bool = True, end_concave_up: bool = True) -> np.ndarray:
    """Pad the waveform with exponential rising (front) and decaying (end) envelopes.
    
    Example usage:
    >>> exp_padded_square = pad_exp(
    >>>     waveform=np.ones(100), 
    >>>     front_len=40, end_len=35, front_tau=5, end_tau=10,
    >>>     front_concave_up=False, end_concave_up=True
    >>> )
    """
    t_front = np.arange(front_len)
    if front_concave_up:
        front = np.exp(-t_front / front_tau)[::-1]
    else:
        front = 1 - np.exp(-t_front / front_tau)

    t_end = np.arange(end_len)
    if end_concave_up:
        end = np.exp(-t_end / end_tau)
    else:
        end = (1 - np.exp(-t_front / front_tau))[::-1]

    # Cast to complex if needed
    if np.iscomplexobj(waveform):
        front = front.astype(complex)
        end = end.astype(complex)

    return np.concatenate([front, waveform, end])

def mix_by_an_digital_lo(waveform, lo_frequency, lo_phase=0, sampling_rate=2e+9):
    """Mix the waveform in a digital way. (simulate what an LO do)

    Example usage:
    >>> SAMPLING_RATE = 2e+9
    >>> # IQ modulation
    >>> carrier_freq = 50e+6
    >>> iqmod_waveform = mix_by_an_digital_lo(
    >>>     waveform, lo_frequency=carrier_freq, sampling_rate=SAMPLING_RATE
    >>> )
    >>> # IQ demodulation
    >>> demod_freq = -carrier_freq
    >>> iqdemod_waveform = mix_by_an_digital_lo(
    >>>     iqmod_waveform, lo_frequency=demod_freq, sampling_rate=SAMPLING_RATE
    >>> )
    """
    t = np.arange(len(waveform)) * 1/sampling_rate
    carrier = np.exp(1j* 2*np.pi* lo_frequency * t + lo_phase)
    mixed = waveform * carrier
    return mixed

def t_of(waveform, t0=0, sampling_rate=2e+9):
    """Return time array for a waveform.
    
    Example usage:
    >>> plt.plot(t_of(waveform), np.abs(waveform))
    """
    n_pts = len(waveform)
    return np.arange(n_pts) * 1/sampling_rate + t0