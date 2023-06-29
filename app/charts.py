
from io import BytesIO
import base64
import pandas as pd
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
        buf = BytesIO()
        self.fig.savefig(buf, format="png", bbox_inches='tight')
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        self.name = f"data:image/png;base64,{data}"
        return self.name

class Piechart(Chart):
    def make_pie_chart(self):
        value_labels = []
        for label, value in zip(self.labels, self.data):
            formatted_label = f'{label} {value:}'
            value_labels.append(formatted_label)
        explode = []
        for values in value_labels:
            explode.append(0.01)

        ax=self.fig.subplots()
        ax.pie(self.data, startangle=90, explode=explode)
        ax.legend(value_labels, fontsize=18, loc='center left', bbox_to_anchor=(0, 0))
        centre_circle = plt.Circle((0,0),0.80,fc='white')
        self.fig.gca().add_artist(centre_circle)

class Barchart(Chart):
    def __init__(self, data, labels, name, fig, constantsList, y_axis):
        super().__init__(data, labels, name, fig)
        self.constantsList = constantsList
        self.y_axis = y_axis

    def make_bar_chart(self):
        averagesDf = pd.DataFrame({
            'Meat type': self.data.index,
            'userAverage': self.data.values,
            'constantsAverage': self.constantsList
            })
        data_melted = pd.melt(averagesDf, id_vars='Meat type', var_name='variable', value_name=self.y_axis)
        ax = sns.barplot(x='Meat type', y=self.y_axis, hue='variable', data=data_melted)
        ax.legend(title=None, fontsize = 14)
        for t, l in zip(ax.legend_.texts, self.labels):
            t.set_text(l)
