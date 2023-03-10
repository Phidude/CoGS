import streamlit as st
import numpy as np
import plotly.graph_objects as go
from Gamry_analyser_backend import convert, convert_to_string, try_float
from Plot_OCP import get_salient_data

# To run website in a virtual browser type following into the terminal:         py -m streamlit run main.py

# The different variables that change when selecting and plotting the different Gamry test
column_containing_X_axis_data = 0
column_containing_Y_axis_data = 0
skip_lines = 0
X_axis_title = 'null'
Y_axis_title = 'null'
selected_type = 'null'
show_legend = True
data = 'null'

st.title('Swansea University Corrosion Software (SUCS)')
# button to select which Gamry test is being analysed
chosen_gamry_test = st.radio(
    'Choose one of the following Gamry tests to analyse:',
    ('OCP', 'Potentiodynamic polarization', 'EIS'))
hide_legend = st.checkbox('Hide legend (to make the graph a uniform shape)')

if hide_legend:
    show_legend = False

# The different values required for the to select and plot the OCP data
if chosen_gamry_test == 'OCP':
    column_containing_X_axis_data = 1
    column_containing_Y_axis_data = 2
    skip_lines = 48
    X_axis_title = '<b>Time (s)</b>'
    Y_axis_title = '<b>E<sub>corr</sub> vs SHE (V)</b>'
    selected_type = 'linear'
# The different values required for the to select and plot the potentiodynamic polarization data
if chosen_gamry_test == 'Potentiodynamic polarization':
    column_containing_X_axis_data = 2
    column_containing_Y_axis_data = 3
    skip_lines = 55
    X_axis_title = '<b>E<sub>corr</sub> vs SHE (V)</b>'
    Y_axis_title = '<b>Current Density log(i/A cm<sup>-2</sup>)</b>'
    selected_type = 'log'
# The different values required for the to select and plot the EIS data
if chosen_gamry_test == 'EIS':
    column_containing_X_axis_data = 3
    column_containing_Y_axis_data = 4
    skip_lines = 60
    X_axis_title = '<b>Z\'</b>'
    Y_axis_title = '<b>-Z\'\'</b>'
    selected_type = 'linear'

if hide_legend == "":
    show_legend = False

xs_data = []
ys_data = []

# Open files using streamlit website
multiple_uploaded_files = st.file_uploader('Choose files', accept_multiple_files=True)
figure = go.Figure()  # makes a figure Object in plotly to be presented
for my_file in multiple_uploaded_files:  # loops through files, extracting and adding the x and y data to The figure
    if my_file is not None:
        content = my_file.getvalue().decode('ascii', 'ignore').splitlines()  # changes the downloaded file from bytes to
        # a list of strings. The method decode ignores any unknown ascii characters (e.g.°) and splits each line.
        content = get_salient_data(content, skip_lines)  # skips the meta data in the Gamry file
        data = convert(content).transpose()  # converts data and flips lines to columns
        x_data = data[column_containing_X_axis_data]  # gets data to plot on the axis
        y_data = data[column_containing_Y_axis_data]
        if chosen_gamry_test == 'EIS':
            y_data = np.abs(y_data)  # converts data to absolute values
        figure.add_trace(go.Scatter(x=x_data, y=y_data, name=my_file.name))  # adds data to The figure
        figure.update_layout(font=dict(family="Times New Roman", size=12, color="black"))
        figure.update_layout(autosize=False, width=800, height=500, )
        figure.update_layout(showlegend=show_legend)
        figure.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                              'paper_bgcolor': 'rgba(0,0,0,0)'})  # fig.update_layout(width=<VALUE> Type: number greater than or equal to 10Default: 700 Sets the plot's width (in px).

        figure.update_xaxes(title_text=X_axis_title, tickformat=',', showline=True, linewidth=1, linecolor="black",
                            mirror=True)
        figure.update_yaxes(title_text=Y_axis_title, showline=True, linewidth=1,
                            linecolor="black",
                            mirror=True,
                            type=selected_type,
                            exponentformat="power")  # selected-type is a variable which changes depending on Gamry test

        xs_data.append(x_data)
        ys_data.append(y_data)

#if chosen_gamry_test == 'Potentiodynamic polarization':

# Presents figure in streamlit and allows data download
st.plotly_chart(figure)

if xs_data:
    print(len(xs_data))
    print(len(xs_data[0]))
    data = [val for pair in zip(xs_data, ys_data) for val in pair]
    print(np.array(data).ndim)
    content_ = []
    for line in np.transpose(data):
        content_.append(",".join(['%E' % value for value in line]))
    content_ = "\n".join(content_)
    st.download_button('Download', content_)
