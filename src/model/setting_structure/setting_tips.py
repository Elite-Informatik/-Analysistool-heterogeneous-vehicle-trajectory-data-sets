from enum import Enum


class SettingTips(Enum):
    TRAJECTORY_SAMPLE_SIZE = "Sets the number of trajectories that are displayed on the map." \
                             "Selecting a value that is to large might decrease the performance of the application." \
                             "A save value is between 0 and 20."

    TRAJECTORY_STEP_SIZE = "Decides the step size of the trajectories. For example, if the step size is 3, " \
                           "every third datapoint of the trajectory is drawn on the map. This setting can be " \
                           "used to increase the performance of the application by reducing the amount " \
                           "of drawn datapoints for each trajectory."

    SHOW_LINE_SEGMENTS = "Can be used to enable and disable the line segments of the trajectories"

    COLOR_SETTINGS = "Defines the colorization schema of the trajectories. If the schema is set to parameter you" \
                     "need to additionally select a parameter to colorize the trajectories " \
                     "in the trajectory param setting. If you set the schema to uni color you can additionally " \
                     "select a uni color for all trajectories in the trajectory uni color setting"

    TRAJECTORY_UNI_COLOR = "The color which is used for all trajectories if the color schema is set to uni color"

    TRAJECTORY_PARAM_COLOR = "The parameter which is used for the colorization of the trajectories if the color " \
                             "schema is set to parameter. The color of each trajectory point and segment is " \
                             "calculated with the selected parameter "

    FILTER_GREYED = "Decides if the datapoints that did not pass the filter are greyed out or not shown at all." \
                    "If checked the datapoints will be greyed out. If set to false the points wont be shown at all " \
                    "which can increase the performance of the application"

    OFFSET = "This value decides which section of the dataset is displayed on the map. " \
             "The value must be between 0 and 1."

    RANDOM_SAMPLE = "If checked the application will randomly select the trajectories from the dataset." \
                    "If unchecked the trajectories will be selected as a continuous chunk from the dataset."

    RANDOM_SEED = "The random seed is used to determine the random sample."
