"""A timeline graph

Create a timeline based on a list of events with dates.

This script required the following packages: 
    * plotly
    * numpy

This file contains the following functions:

    * graph - return a go.Figure object with the timeline graph
    * main - the main function of the script

"""

# Imports
import plotly.graph_objects as go
import numpy as np 


# Variables
UPPER1_POSITION = -100
UPPER1_YANCHOR = 'top'

UPPER2_POSITION = -200
UPPER2_YANCHOR = 'top'

DOWN1_POSITION = 100
DOWN1_YANCHOR = 'bottom'

DOWN2_POSITION = 200
DOWN2_YANCHOR = 'bottom'

# Color scales of the timeline
COLOR_SCALE_GREYS = px.colors.sequential.Greys

CONFIG_ANNOTATIONS_TIMELINE = {
    'arrowwidth': 2.5,
    'arrowhead': 6,
    'arrowcolor': COLOR_SCALE_GREYS[3],
    'ax': 0,
    'showarrow': True, 
    'font': {
        'color': COLOR_SCALE_GREYS[6], 
        'size': 12,
    },
    'bgcolor': "#FFFFFF", 
    'align': 'left',
    'xref': 'x',
    'yref': 'y',
    'xanchor': 'left',
    'yanchor': 'top',
    'width': 200,
    'borderpad': 4,
    'arrowsize': 0.8,
}

def graph(self, data_dict=None, back_config=None, data_events=None):
    """ Gets events data and return a go.Figure object with the timeline graph

    Parameters
    ----------

        data_dict: dict
            dict with axis configuration
        back_config: dict
            dict with background line data
        data_events: list
            list with events of timeline

    Returns
    -------

        go.Figure
            a go.Figure object with the graph


    """

    if data_dict is None:
         raise Exception("The data_dict parameter is required.")
    
    if data_events is None:
        raise Exception("The data_events parameter is required.")

    # Create a go.Figure object
    fig = go.Figure()

    # Set the y position of the timeline
    y_timeline = 1

    if back_config is not None:

        # Set the color of background marker
        initial_back_config = {
            'marker': {
                'color': layout.COLOR_SCALE_GREYS[2]
            }
        }

        # Update the background config with the default color
        back_config.update(initial_back_config)

        # Create background trace
        fig.add_trace(go.Scatter(back_config))

        # Change y position of the timeline based on background data
        y_timeline = back_config['y'].quantile(q=0.75)

    
    # Create a timeline trace
    fig.add_trace(go.Scatter(data_dict))

    # Configure x axis
    fig.update_xaxes(showgrid=False, zeroline=True,showticklabels=False,)

    # Configure y axis
    fig.update_yaxes(showgrid=False, zeroline=False,showline=False,showticklabels=False,visible=False)

    # Hidden legend
    fig.update_layout(showlegend=False)


    # List of annotations with events of timeline
    annotations = []

    # Create the annotations of timeline events
    for event in data_events:
        temp_annotation = layout.CONFIG_ANNOTATIONS_TIMELINE.copy()
        
        # Basic config of annotation
        temp_config = {
            'x': event['x'],
            'y': y_timeline,
            'text': event['text']
        }
        
        # Change the default width of annotation (Default: 150)
        if 'width' in event.keys():
            temp_config.update({'width': event['width']})
            
        # Change the default postion of annotation (Default: 100)
        # There are 4 options: upper1, upper2, down1, down2
        if 'position' in event.keys():
            
            if event['position'] == 'upper1':
                temp_config.update({'ay': UPPER1_POSITION})
                temp_config.update({'yanchor': UPPER1_YANCHOR})
            elif event['position'] == 'upper2':
                temp_config.update({'ay': UPPER2_POSITION})
                temp_config.update({'yanchor': UPPER2_YANCHOR})
            elif event['position'] == 'down1':
                temp_config.update({'ay': DOWN1_POSITION})
                temp_config.update({'yanchor': DOWN1_YANCHOR})
            elif event['position'] == 'down2':
                temp_config.update({'ay': DOWN2_POSITION})
                temp_config.update({'yanchor': DOWN2_YANCHOR})
            else:
                raise Exception("For different position, update ay value")
        
        # Update default config annotation
        temp_annotation.update(temp_config)

        # Insert annotation in annotation list
        annotations.append(temp_annotation)

    # Update fig with created annotations
    fig['layout']['annotations'] = annotations

    return fig

if __name__ == '__main__':
    



    fig = graph(data_dict, back_config, data_events)

