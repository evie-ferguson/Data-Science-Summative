from shiny import App, ui, render, reactive
import pandas as pd
import matplotlib.pyplot as plt

ui = ui.page_fluid(
    ui.output_text("header"),
    ui.output_plot("attendance_plot"),)

# history module attendance rate

def server(input, output, session):
    @render.text
    def header():
        return "Attendance Rate"
    
    @render.plot
    def attendance_plot():
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
        history_df = df[df['Module Name'] == 'History']
        history_attendance = history_df.groupby(history_df['Date'].dt.date)['Attended'].mean()
        plt.figure(figsize=(10,6))
        plt.title('Average History Module Attendance Rate Over Time')
        plt.xlabel('Date')
        plt.ylabel('Attendance Rate')
        plt.xticks(rotation=90) 
        plt.grid()
        fig = plt.plot(history_attendance, marker='o', linestyle='-')
        return fig

app = App(ui, server)