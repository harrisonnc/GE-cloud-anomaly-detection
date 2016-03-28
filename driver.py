from flask import Flask, render_template
from log_analysis import log_analysis
from log_graphs import graphics
app = Flask(__name__)

@app.route('/')
def dashboard():
#    conf_file=data_logs.retrieve_conf_file()
#    log_location=data_logs.retrieve_log_location(conf_file)
#    file_type=data_logs.retrieve_file_type(conf_file)
#    master_log=data_logs.retrieve_data(log_location,file_type)
#    column_headings=data_logs.retrieve_column_headings(conf_file)
#    formatted_log=data_logs.format_data(master_log,column_headings)

    logFile=log_analysis()
    topLogins=logFile.log_links(logFile.top_logins(15))
    topSuccessfulLogins=logFile.log_links(logFile.top_successful_logins(15))
    topFailedLogins=logFile.log_links(logFile.top_failed_logins(15))
    return render_template('dashboard.html', logins=topLogins.to_html(escape=False),
                           successful=topSuccessfulLogins.to_html(escape=False),
                           failed=topFailedLogins.to_html(escape=False))
                           #sample=logFile.formatted_log.head().to_html())


@app.route('/<username>')
def individual_log(username):
    logFile=log_analysis()
    return render_template('search_results.html',search_results=logFile.search_log(username).to_html())


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sample')
def sample():
    logFile=log_analysis()
    return logFile.formatted_log.head(100).to_html()



if __name__ == '__main__':
    app.debug=True
    graphics.main(graphics)
    app.run()