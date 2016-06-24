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
    data = [
        ['gender', 'money', 'swear','foreign/immigrants', 'race', 'government'],
##        ('clinton', [[1.155838875830177, 0.7779387043963781, 1.2795927001903848, 0.5863674231788782, 0.7583868129606828, 0.996437786101984]]),
##        ('sanders', [[0.9895147460357561, 2.1034472075717243, 0.8593679329254473, 0.8645994745124583, 1.4435920563220055, 1.6077128486785472]]),
##        ('cruz',[[1.327126762207415, 0.3694232879232219, 0.8309768228183629, 1.3332658723316742, 1.271294252242121, 1.5860842101336636]]),
##        ('trump', [[0.8012401250942027, 0.8093273193689485, 0.8190875213338745, 1.7661060600014233, 0.8295643963119217, 0.2357825534002732]])
##          ('kasich', [[0.8815750536574646, 0.7446553400129148, 0.7850428979323989, 1.8932136802067627, 0.685155912668317, 1.0555232757607556]]),
##          ('carson', [[1.1721553666787043, 0.47084886362713674, 0.7850428979323989, 0.21921250925838087, 0.6045608122232917, 1.1286262389303894]]),
##          ('bush', [[0.7268053472490086, 0.6028113485185329, 0.7850428979323989, 1.1922933741761712, 0.7808897403193965, 1.0328904418980804]]),
##          ('omalley', [[0.9123816006372405, 0.7849431576403177, 0.9567071002346942, 0.8828991510594183, 1.642982169108432, 0.6297198559014993]])
         ('christie', [[0.9455485598433537, 0.2636578091335524, 0.7850428979323989, 0.3007772207379934, 0.6351282364543827, 1.0460604663068873]]),
         ('paul', [[1.151180160233277, 1.2353031100781078, 1.1538665153242516, 0.9784038730175091, 1.3817047185507672, 1.628145856957288]]),
        ('robio', [[0.8280724648553695, 0.3716998621131601, 0.7850428979323989, 0.9324128547888144, 0.7291718552996223, 0.9763847156573949]])

##        ('carson', [[1.2464102232777976, 0.8626365754781126, 0.7921829141064941, 0.21836558535067874, 0.6069363147587958]]),
##        ('bush', [[0.6495905661462491, 0.5377911467930026, 0.7921829141064941, 0.8130045925225663, 0.783685966802142]]),
##        ('omalley', [[0.9512164217210985, 0.6558048260493001, 0.9670403294732143, 1.0353361343983098, 1.6478353634037939]]),
##        ('christie', [[1.0516401739455477, 0.38435671511890523, 0.7921829141064941, 0.34532947469748665, 0.6375766734058013]])
##        ('paul', [[1.1676969455339903, 0.993276694286207, 1.1678672070365705, 0.8170487968437165, 1.3859345002188839]]),
##        ('rubio',[[0.7718392061772485, 0.44005859738679254, 0.7921829141064941, 1.175624250240182, 0.7318446819921947]]),
##        ('kasich', [[0.7718392061772485, 0.44005859738679254, 0.7921829141064941, 1.175624250240182, 0.7318446819921947]])
##        ('fiorina', [[1.2630760296270518, -0.061065930839907745, 0.7921829141064941, 0.21836558535067874, 0.3621403431308957]]),
    ]
    return data


if __name__ == '__main__':
    N = 6
    theta = radar_factory(N, frame='polygon')

    data = example_data()
    spoke_labels = data.pop(0)

    fig = plt.figure(figsize=(9, 9))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate axes
    for n, (title, case_data) in enumerate(data):
        ax = fig.add_subplot(2, 2, n + 1, projection='radar')
        plt.rgrids([0.5, 1.0, 1.5])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        ax.set_ylim(top = 2.5)
        ax.set_ylim(bottom = 0)
        
        for d, color in zip(case_data, colors):
            print d, theta
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
