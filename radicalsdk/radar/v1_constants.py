import os
import numpy as np

class TupperwearD435_0:
    F = np.load(os.path.join(os.path.dirname(__file__), 'v1_data/f_matrix.npy'))
    P = np.load(os.path.join(os.path.dirname(__file__), 'v1_data/p_matrix_original.npy'))

class TupperwearD435:
    F = np.load(os.path.join(os.path.dirname(__file__), 'v1_data/f_matrix.npy'))
    P = np.load(os.path.join(os.path.dirname(__file__), 'v1_data/p_matrix.npy'))
