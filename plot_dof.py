import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap

DEFAULT_F_NUMBER_MM = 8.0
DEFAULT_FOCAL_LENGTH_MM = 16.0
DEFAULT_PIXEL_SIZE_M = 5.5e-6 # in meters, assuming 5.5um pixels
DEFAULT_PIXEL_SIZE_MM = DEFAULT_PIXEL_SIZE_M * 1000 # mm
PIXEL_COC_RATIO = 2.0 # just guessing that 2 pixels sizes is the acceptable range of focus (may want more)

# RED = np.array([1.0, 0.0, 0.0])
# GREEN = np.array([0.0, 1.0, 0.0])
# BLUE = np.array([0.0, 0.0, 1.0])

def magnification(focal_length, subject_distance):
    return focal_length / (subject_distance - focal_length)

def aperture(focal_length, f_number):
    return focal_length / f_number

def coc_size(pixel_size=DEFAULT_PIXEL_SIZE_MM):
    return pixel_size * PIXEL_COC_RATIO

def dof(focal_distance, focal_length=DEFAULT_FOCAL_LENGTH_MM, f_number=DEFAULT_F_NUMBER_MM, pixel_size=DEFAULT_PIXEL_SIZE_MM):
    return 2 * focal_distance**2 * f_number * coc_size(pixel_size) / focal_length**2

def blur(distance, focal_distance, focal_length=DEFAULT_FOCAL_LENGTH_MM, f_number=DEFAULT_F_NUMBER_MM):
    """Calculates the diameter of the blur disk at distance, when the camera is focused at focal_distance"""
    x_d = abs(distance - focal_distance)
    return aperture(focal_length, f_number) * magnification(focal_length, focal_distance) * x_d / distance

def hyperfocal_distance(focal_length, f_number, coc_limit):
    return focal_length**2 / (f_number * coc_limit) + focal_length


# f_nums = [1,2,4,8]

# fig, ax = plt.subplots(len(f_nums), 1, sharey=True)
# fig.suptitle("Depth of Field")
# x = np.arange(0.0, 10000.0, 10.0)

# for n, f_num in enumerate(f_nums):
#     ax[n].set_title(f"f/{f_num}")
#     ax[n].plot(x, dof(x, f_number=f_num))

# plt.tight_layout()
# plt.show()

focal_length = 12
f_number = 8
pixel_size = DEFAULT_PIXEL_SIZE_MM

coc_limit = coc_size(pixel_size)
hf_distance = hyperfocal_distance(focal_length, f_number, coc_limit)

focal_distance = 1500.0
# focal_distance = hf_distance

near_limit = focal_distance / 3.0
far_limit = max(focal_distance * 3.0, 3000)
step_size = (far_limit - near_limit) / 1000


x = np.arange(near_limit, far_limit, step_size)
y = blur(x, focal_distance=focal_distance, focal_length=focal_length, f_number=f_number)
in_focus = y < pixel_size
in_partial_focus = (y < coc_limit) & ~in_focus


plt.title(f"f={focal_length}mm, f/{f_number}, depth={focal_distance:.2f}, hyperfocal={hf_distance:.2f}")
plt.plot(x[~in_partial_focus], y[~in_partial_focus], c="red", linestyle="None", marker=".")
plt.plot(x[in_partial_focus & ~in_focus], y[in_partial_focus & ~in_focus], c="yellow", linestyle="None", marker=".")
plt.plot(x[in_focus], y[in_focus], c="green", linestyle="None", marker=".")

plt.show()