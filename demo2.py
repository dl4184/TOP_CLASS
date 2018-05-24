import numpy as np
import plotly.plotly as py
from plotly import tools as tls
from plotly.graph_objs import *
from scipy.spatial import Delaunay

tls.set_credentials_file(username='dom0308', api_key='ZVULiAArmFwwAvgntzMo')


def sq_norm(v):  # squared norm
    return np.linalg.norm(v) ** 2


def circumcircle(points, simplex):
    A = [points[simplex[k]] for k in range(3)]
    M = [[1.0] * 4]
    M += [[sq_norm(A[k]), A[k][0], A[k][1], 1.0] for k in range(3)]
    M = np.asarray(M, dtype=np.float32)
    S = np.array([0.5 * np.linalg.det(M[1:, [0, 2, 3]]), -0.5 * np.linalg.det(M[1:, [0, 1, 3]])])
    a = np.linalg.det(M[1:, 1:])
    b = np.linalg.det(M[1:, [0, 1, 2]])
    return S / a, np.sqrt(b / a + sq_norm(S) / a ** 2)  # center=S/a, radius=np.sqrt(b/a+sq_norm(S)/a**2)


def get_alpha_complex(alpha, points, simplexes):
    # alpha is the parameter for the alpha shape
    # points are given data points
    # simplexes is the  list of indices in the array of points
    # that define 2-simplexes in the Delaunay triangulation

    return filter(lambda simplex: circumcircle(points, simplex)[1] < alpha, simplexes)


pts = np.loadtxt('data2.txt')
pts = pts/pts.max(axis=0)
tri = Delaunay(pts)
colors = ['#C0223B', '#404ca0', 'rgba(173,216,230, 0.5)']


def Plotly_data(points, complex_s):
    # points are the given data points,
    # complex_s is the list of indices in the array of points defining 2-simplexes(triangles)
    # in the simplicial complex to be plotted
    X = []
    Y = []
    for s in complex_s:
        X += [points[s[k]][0] for k in [0, 1, 2, 0]] + [None]
        Y += [points[s[k]][1] for k in [0, 1, 2, 0]] + [None]
    return X, Y


def make_trace(x, y, point_color=colors[0], line_color=colors[1]):  # define the trace
    # for an alpha complex
    return Scatter(mode='markers+lines',  # set vertices and
                   # edges of the alpha-complex
                   name='',
                   x=x,
                   y=y,
                   marker=Marker(size=6.5, color=point_color),
                   line=Line(width=1.25, color=line_color),

                   )


def make_XAxis(axis_style):
    return XAxis(axis_style)


def make_YAxis(axis_style):
    return YAxis(axis_style)


figure = tls.make_subplots(rows=1, cols=2,
                           subplot_titles=('Delaunay triangulation', 'Alpha shape, alpha=0.15'),
                           horizontal_spacing=0.1,
                           )

pl_width = 800
pl_height = 460
title = 'Delaunay triangulation and Alpha Complex/Shape for a Set of 2D Points'

figure['layout'].update(title=title,
                        font=Font(family="Open Sans, sans-serif"),
                        showlegend=False,
                        hovermode='closest',
                        autosize=False,
                        width=pl_width,
                        height=pl_height,
                        margin=Margin(
                            l=65,
                            r=65,
                            b=85,
                            t=120
                        ),
                        shapes=[]
                        )

axis_style = dict(showline=True,
                  mirror=True,
                  zeroline=False,
                  showgrid=False,
                  showticklabels=True,
                  range=[-0.1, 1.1],
                  tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                  ticklen=5
                  )

for s in range(1, 3):
    figure['layout'].update({'xaxis{}'.format(s): make_XAxis(axis_style)})  # set xaxis style
    figure['layout'].update({'yaxis{}'.format(s): make_YAxis(axis_style)})  # set yaxis style

alpha_complex = get_alpha_complex(0.15, pts, tri.simplices)

X, Y = Plotly_data(pts, tri.simplices)  # get data for Delaunay triangulation
figure.append_trace(make_trace(X, Y), 1, 1)

X, Y = Plotly_data(pts, alpha_complex)  # data for alpha complex
figure.append_trace(make_trace(X, Y), 1, 2)

for s in alpha_complex:  # fill in the triangles of the alpha complex
    A = pts[s[0]]
    B = pts[s[1]]
    C = pts[s[2]]
    figure['layout']['shapes'].append(dict(path='M ' + str(A[0]) + ',' + str(A[1]) + ' ' + 'L ' + \
                                                str(B[0]) + ', ' + str(B[1]) + ' ' + 'L ' + \
                                                str(C[0]) + ', ' + str(C[1]) + ' Z',
                                           fillcolor='rgba(173,216,230, 0.5)',
                                           line=Line(color=colors[1], width=1.25),
                                           xref='x2',
                                           yref='y2'
                                           )
                                      )

py.plot(figure, filename='2D-AlphaS-ex', width=850)
