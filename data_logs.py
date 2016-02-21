import pandas as pd
import re
def retrieve_conf_file():
    conf_file = open('./Configuration/log.conf')
    return conf_file
def retrieve_log_location(conf_file):
    for line in conf_file:
        if re.match('source_file', line):
            return line.split('\'', 1)[1].split('\'',1)[0]
def retrieve_file_type(conf_file):
    for line in conf_file:
        if re.match('source_file_type', line):
            return line.split('\'', 1)[1].split('\'',1)[0]
 #   return re.search('source_file',conf_file)
def retrieve_data(log_location, file_type):
    if file_type == 'csv':
        log_data = pd.read_csv(log_location)
        return log_data
    else:
        return 'invalid data type'
def retrieve_column_headings(conf_file):
    column_keys=['standardized_time','human_readable_time','source_ip','destination_ip','login_account',
                 'log_source_device','log_message']
    column_headings={}
    for key in column_keys:
        for line in conf_file:
            print(key)
            if re.match(key, line):
                column_headings[key]=line.split('\'', 1)[1].split('\'',1)[0]
                break
    for line in conf_file:
        if re.match('custom[01-99]', line):
            column_headings[line.split('=', 1)[0]]=line.split('\'', 1)[1].split('\'',1)[0]
    return column_headings
#def format_data():
#def analyze_data():

def main():
    conf_file=retrieve_conf_file()
    log_location=retrieve_log_location(conf_file)
    file_type=retrieve_file_type(conf_file)
    master_log=retrieve_data(log_location,file_type)
    print(len(master_log))
    column_headings=retrieve_column_headings(conf_file)
    print(column_headings)
    print(column_headings.__len__())
#    print(master_log.head())
if __name__ == "__main__":
    main()