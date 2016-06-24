# Example of creating a radar chart (a.k.a. a spider or star chart) [1]_.
##
##Although this example allows a frame of either 'circle' or 'polygon', polygon
##frames don't have proper gridlines (the lines are circles instead of polygons).
##It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
##matplotlib.axis to the desired number of vertices, but the orientation of the
##polygon is not aligned with the radial axes.

## .. [1] http://en.wikipedia.org/wiki/Radar_chart
## """
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
import pandas as pd

def get_candidate_record():
    df = pd.read_csv("../data/speeches_mean_file.csv")
    g = df.groupby("candidate")
    d = g.get_group('trump')['dimention'].values
    data = g.groups

    return d,data

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def example_data():
    # The following data is from the Denver Aerosol Sources and Health study.
    # See  doi:10.1016/j.atmosenv.2008.12.017
    #
    # The data are pollution source profile estimates for five modeled
    # pollution sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical
    # species. The radar charts are experimented with here to see if we can
    # nicely visualize how the modeled source profiles change across four
    # scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase speciesis present...
    d,record = get_candidate_record()
    print type(record)
    data = [
        d,
        ('clinton',record['clinton']), 
        ('sanders',record['sanders']),
        ('cruz',record['ted_cruz']) ,
        ('trump',record['trump']) 
#        ('carson',record['carson']) 
#        ('bush',record['bush']) 
##        ('omalley',record['omalley']),
#        ('christie',record['christie']),
#        ('paul',record['paul']) 
#        ('rubio',record['rubio'])
#        ('kasich',record['kasish']) 
#        ('fiorina',record['fiorina'])
    ]
    N = len(d)
    return data,N


if __name__ == '__main__':
    #N = 6

    data,N = example_data()
    
    theta = radar_factory(N, frame='polygon')
    spoke_labels = data.pop(0)
    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate axes
    for n, (title, case_data) in enumerate(data):
        print title, case_data
        ax = fig.add_subplot(2, 2, n + 1, projection='radar')
        plt.rgrids([0.5, 1.0, 1.5])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        ax.set_ylim(top = 2.5)
        ax.set_ylim(bottom = 0)
        
        for d, color in zip(case_data, colors):
            print theta,d
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    plt.subplot(2, 2, 1)
#    labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
#    legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
#    plt.setp(legend.get_texts(), fontsize='small')

    plt.figtext(0.5, 0.965, 'Frequency of concepts mentioned in speech. 1 = avg',
                ha='center', color='black', weight='bold', size='large')
    ax.set_ylim(top = 2)
    ax.set_ylim(bottom = 0)
    plt.show()
