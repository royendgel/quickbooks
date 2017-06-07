
log_file = 'C:\\ProgramData\\Intuit\QuickBooks\\qbsdklog.txt'
def get_log(log_file):
    with open(log_file, 'r',) as f:
        line_n = 0
        lines = []
        answer = None
        lines = f.readlines()
        for line in lines:
            line_n += 1


            occurence = line.find('================')
            if occurence != -1:
                answer = line_n
        if answer:
            return "".join(lines[answer:len(lines)])
    return False