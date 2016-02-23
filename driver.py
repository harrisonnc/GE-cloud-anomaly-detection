from flask import Flask, render_template
from log_analysis import log_analysis
app = Flask(__name__)

@app.route('/')
def hello_world():
#    conf_file=data_logs.retrieve_conf_file()
#    log_location=data_logs.retrieve_log_location(conf_file)
#    file_type=data_logs.retrieve_file_type(conf_file)
#    master_log=data_logs.retrieve_data(log_location,file_type)
#    column_headings=data_logs.retrieve_column_headings(conf_file)
#    formatted_log=data_logs.format_data(master_log,column_headings)
    logFile=log_analysis()
    topLogins=logFile.top_logins()
    return render_template('dashboard.html', logins=topLogins.to_html(), sample=logFile.formatted_log.head().to_html())
    #return str(master_log.head())

@app.route('/asdf/')
def hello_world1():
    return 'Hello, Goodbye!!'

if __name__ == '__main__':
    app.run()