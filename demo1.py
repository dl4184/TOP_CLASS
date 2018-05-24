import numpy as np
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

plotly.tools.set_credentials_file(username='dom0308', api_key='ZVULiAArmFwwAvgntzMo')
pts = np.loadtxt('data.txt')

x, y, z = zip(*pts)

points = Scatter3d(mode='markers',
                   name='',
                   x=x,
                   y=y,
                   z=z,
                   marker=Marker(size=2, color='#458B00')
                   )

simplexes = Mesh3d(alphahull=10.0,
                   name='',
                   x=x,
                   y=y,
                   z=z,
                   color='90EE90',  # set the color of simplexes in alpha shape
                   opacity=0.15
                   )

x_style = dict(zeroline=False, range=[-2.85, 4.25], tickvals=np.linspace(-2.85, 4.25, 5)[1:].round(1))
y_style = dict(zeroline=False, range=[-2.65, 1.32], tickvals=np.linspace(-2.65, 1.32, 4)[1:].round(1))
z_style = dict(zeroline=False, range=[-3.67, 1.4], tickvals=np.linspace(-3.67, 1.4, 5).round(1))

layout = Layout(title='Alpha shape of a set of 3D points. Alpha=0.1',
                width=500,
                height=500,
                scene=Scene(
                    xaxis=x_style,
                    yaxis=y_style,
                    zaxis=z_style
                )
                )

fig = Figure(data=Data([points, simplexes]), layout=layout)
py.plot(fig, filename='3D-AlphaS-ex')
