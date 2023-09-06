import math
import numpy as np

# import logging
# logger = logging.getLogger(__name__)

def fovs(fov_diagonal=np.deg2rad(84),
         resolution=[3840,2160]):
    '''
    Calculates the left-right and front-rear fields of view from the diagonal
    field of view and resolution.
    Inputs:
        fov_diagonal: float
            Diagonal field of view in radians.
        resolution: 2D array
            Resolution in pixels x pixels.
    Outputs:
        fov_lr: float
            Left-right field of view in radians.
        fov_fr: float
            Front-rear field of view in radians.
    '''

    # Resolution rate, i.e., field width divided by field length
    resolution_rate = resolution[0]/resolution[1]

    # 3:2 uses the entire sensor area
    if resolution_rate == 3/2:
        fov_lr = 2*math.atan(3/math.sqrt(13)*math.tan(fov_diagonal/2))
        fov_fr = 2*math.atan(2/math.sqrt(13)*math.tan(fov_diagonal/2))

    # 4:3 uses the entire height of sensor area, not the width
    elif resolution_rate == 4/3:
        fov_fr = 2*math.atan(2/math.sqrt(13)*math.tan(fov_diagonal/2))
        fov_lr = 2*math.atan(resolution_rate*math.tan(fov_fr/2))

    # 16:9 uses the entire width of sensor area, not the height
    elif resolution_rate == 16/9:
        fov_lr = 2*math.atan(3/math.sqrt(13)*math.tan(fov_diagonal/2))
        fov_fr = 2*math.atan(1/resolution_rate*math.tan(fov_lr/2))

    else:
        raise ValueError('Resolution rate not addressed.')

    return fov_lr,fov_fr

def count_frames(height=10,
                 speed=10,
                 fov_diagonal=84,
                 fps=60,
                 resolution=[3840,2160],
                 object_size=1):
    '''
    Counts how many frames contains an object.
    Inputs:
        height: float
            Height in meters (m).
        speed: float
            Speed in meters per second (m/s).
        fov_diagonal: float
            Diagonal field of view in degrees.
        fps: float
            Frame rate in frames per second.
        resolution: 2D array
            Resolution in pixels x pixels.
        object_size: float
            Object size in meters (m).
            Default 0 (zero).
    Outputs:
        frames: int
            Quantity of frames that contains the hole object.
    '''

    # Diagonal FOV measured in radians
    fov_diagonal_radians = np.deg2rad(fov_diagonal)

    # Left-right and front-rear FOVs
    fov_lr,fov_fr = fovs(fov_diagonal_radians,resolution)

    # Field width based on the height and front-rear FOV
    field_width = 2*height*math.tan(fov_fr/2)

    # Displacement of the drone covering the hole object
    displacement = field_width-object_size

    # Displacement time
    time = displacement/speed

    # Quantity of frames that contains the object
    frames = math.floor(fps*time)

    return frames
