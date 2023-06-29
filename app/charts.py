# These are used to save the save the chart in a png format.
from io import BytesIO
import base64
# Used for the handling of dataframes.
import pandas as pd
# Libraries used for charting.
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns




class Chart:
    def __init__(self, data, labels, name, fig):
        self.data = data
        self.labels = labels
        self.name = name
        self.fig = fig

    def save_chart(self):
        # Method used to save a chart to the png format. Available to all the Chart subclasses.
        buf = BytesIO()
        self.fig.savefig(buf, format="png", bbox_inches='tight')
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        self.name = f"data:image/png;base64,{data}"
        return self.name


class Piechart(Chart):
    # All the arguments required are the same as for the Chart super class.
    def make_pie_chart(self):
        # Method to generate a pie chart.
        # First the labels and values are joined to a tuple and then appended into an array, as this is the format required by the chart functions.
        value_labels = []
        for label, value in zip(self.labels, self.data):
            formatted_label = f'{label} {value:}'
            value_labels.append(formatted_label)

        # Creating an array for the explode parameter, which determines the distance pie chart slices have from the middle of the chart. With the for loop it will work with any number of values charted.
        explode = []
        for values in value_labels:
            explode.append(0.01)

        # Creating the chart figure.
        ax=self.fig.subplots()
        ax.pie(self.data, startangle=90, explode=explode)
        # Formatting the legend/
        ax.legend(value_labels, fontsize=18, loc='center left', bbox_to_anchor=(0, 0))
        # Adding a circle in the center of the chart, to turn it into a doughnut chart.
        centre_circle = plt.Circle((0,0),0.80,fc='white')
        self.fig.gca().add_artist(centre_circle)


class Barchart(Chart):
    # A Barchart object requires a few extra arguments compared to the Chart super class.
    def __init__(self, data, labels, name, fig, constantsList, y_axis):
        super().__init__(data, labels, name, fig)
        self.constantsList = constantsList
        self.y_axis = y_axis

    def make_bar_chart(self):
        # Method to generate a bar chart.
        # First a dataframe is created containing all the relevant information for the chart.
        averagesDf = pd.DataFrame({
            'Meat type': self.data.index,
            'userAverage': self.data.values,
            'constantsAverage': self.constantsList
            })
        # This dataframe is melted as is required by the charting functions.
        data_melted = pd.melt(averagesDf, id_vars='Meat type', var_name='variable', value_name=self.y_axis)
        # Seaborn is used to create the chart.
        ax = sns.barplot(x='Meat type', y=self.y_axis, hue='variable', data=data_melted)
        # The legend is formatted.
        ax.legend(title=None, fontsize = 14)
        # For loop to set the labels in the legend to the correct strings.
        for legend_text, labels in zip(ax.legend_.texts, self.labels):
            legend_text.set_text(labels)
