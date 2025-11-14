from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("attendance_anonymised-1.csv")
df = df.rename(columns={'Unit Instance Code': 'Module Code', 
                        'Calocc Code': 'Year', 
                        'Long Description': 'Module Name', 
                        'Register Event ID': 'Event ID', 
                        'Register Event Slot ID': 'Event Slot ID',
                        'Planned Start Date': 'Date', 
                        'is Positive': 'Has Attended', 
                        'Postive Marks': 'Attended', 
                        'Negative Marks': 'NotAttended', 
                        'Usage Code': 'Attendance Code'})
df['Date'] = pd.to_datetime(df['Date'])
module_choices = sorted(df['Module Name'].dropna().unique())

ui = ui.page_fluid(
    ui.h2("Attendance Rate"),
    ui.input_select("module", "Select module", choices = module_choices, selected = module_choices[0]),
    ui.output_text("header"),
    ui.output_plot("attendance_plot"),)

# Making the app interactive - allowing the user to select the module to plot

def server(input, output, session): 
    @render.text
    def header():
        return f"Attendance Rate - {input.module()}"
    
    @render.plot
    def attendance_plot():
        module = input.module()
        subset = df[df['Module Name'] == module]
        attendance = subset.groupby(subset['Date'].dt.date)['Attended'].mean()
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(attendance.index, attendance.values, marker='o', linestyle='-')
        ax.set_title(f'Average {module} Attendance Rate Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Attendance Rate')
        plt.setp(ax.get_xticklabels(), rotation=90)
        ax.grid(True)
        return fig

app = App(ui, server)