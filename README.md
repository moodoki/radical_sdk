# RaDICaL Dataset SDK
> The RaDICaL Dataset: A synchronized and calibrated low-level Radar, RGB-D and IMU dataset.


![CI](https://github.com/moodoki/radical_sdk/workflows/CI/badge.svg)

This is pre-alpha research quality code, and is being actively developed on.
Anything may change at anytime. Please check back here often.

Bug reports are very much appreciated.

# TODO

 - [ ] Radar config reader
 - [x] Read from aligned H5 dataset
 - [ ] Read from raw bags (to produce aligned/unaligned H5 datasets)
 - [x] Polar to Cartesian Projection
 - [ ] Camera/Radar coordinate transforms

## Install

`python -m pip install git+https://github.com/moodoki/radical_sdk.git`

## How to use
> Dataset is currently under review and will be made available soon.

Download the dataset at our [project page](https://publish.illinois.edu/radicaldata/).
A small sample to try things our can be found [here]().


Reading and displaying depth and RGB is easy

```python
#skip
import matplotlib.pyplot as plt
import numpy as np

from radicalsdk.h5dataset import H5DatasetLoader

data = H5DatasetLoader('../samples/indoor_sample.h5')


frame_idx = 1
plt.figure()
plt.imshow(data['rgb'][frame_idx])
plt.title(f'RGB frame {frame_idx}@{data["rgb_timestamp"][frame_idx]}')
plt.show()
plt.figure()
plt.imshow(data['depth'][frame_idx])
plt.title(f'Depth frame {frame_idx}@{data["depth_timestamp"][frame_idx]}')
plt.show()
```


![png](docs/images/output_7_0.png)



![png](docs/images/output_7_1.png)


The radar data is a 3D array arranged slow_time, antenna, fast_time.

`RadarFrame` encapsulates the necessary processing

```python
#skip

from radicalsdk.radar.config_v1 import read_radar_params
from radicalsdk.radar.v1 import RadarFrame

# Read config and configure RadarFrame object
radar_config = read_radar_params('../samples/indoor_human_rcs.cfg')
rf = RadarFrame(radar_config)

#Set raw cube to the required frame from the hdf5 file
rf.raw_cube = data['radar'][1]

# The desired view of the radar frame is now available
```

### Range Azimuth in Polar Coordinates

```python
# skip
plt.figure()
plt.imshow(np.log(np.abs(rf.range_azimuth_capon)))
plt.show()
```


![png](docs/images/output_11_0.png)


### Projecting to cartesian

```python
#skip
from radicalsdk.geometry import PolarToCartesianWarp

p2c = PolarToCartesianWarp()

cartesian_radar = p2c(np.abs(rf.range_azimuth_capon)[np.newaxis, ..., np.newaxis])
plt.figure()
plt.imshow(np.log(cartesian_radar[0, ...]))
plt.show()
```

    WARNING:tensorflow:Layer polar_to_cartesian_warp is casting an input tensor from dtype float64 to the layer's dtype of float32, which is new behavior in TensorFlow 2.  The layer has dtype float32 because its dtype defaults to floatx.
    
    If you intended to run this layer in float32, you can safely ignore this warning. If in doubt, this warning is likely only an issue if you are porting a TensorFlow 1.X model to TensorFlow 2.
    
    To change all layers to have dtype float64 by default, call `tf.keras.backend.set_floatx('float64')`. To change just this layer, pass dtype='float64' to the layer constructor. If you are the author of this layer, you can disable autocasting by passing autocast=False to the base Layer constructor.
    


    /home/moodoki/.venvs/radical/lib/python3.8/site-packages/tensorflow_addons/utils/resource_loader.py:72: UserWarning: You are currently using TensorFlow 2.3.1 and trying to load a custom op (custom_ops/image/_resampler_ops.so).
    TensorFlow Addons has compiled its custom ops against TensorFlow 2.2.0, and there are no compatibility guarantees between the two versions. 
    This means that you might get segfaults when loading the custom op, or other kind of low-level errors.
     If you do, do not file an issue on Github. This is a known limitation.
    
    It might help you to fallback to pure Python ops with TF_ADDONS_PY_OPS . To do that, see https://github.com/tensorflow/addons#gpucpu-custom-ops 
    
    You can also change the TensorFlow version installed on your system. You would need a TensorFlow version equal to or above 2.2.0 and strictly below 2.3.0.
     Note that nightly versions of TensorFlow, as well as non-pip TensorFlow like `conda install tensorflow` or compiled from source are not supported.
    
    The last solution is to find the TensorFlow Addons version that has custom ops compatible with the TensorFlow installed on your system. To do that, refer to the readme: https://github.com/tensorflow/addons
      warnings.warn(
    <ipython-input-4-8eb05fa747bc>:7: RuntimeWarning: divide by zero encountered in log
      plt.imshow(np.log(cartesian_radar[0, ...]))



![png](docs/images/output_13_2.png)

