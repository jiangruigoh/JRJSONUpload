# raw query -> return dictionary result
def raw_query(querystr, param):
    from django.db import connection
    result = []
    with connection.cursor() as cursor:
        try:
            cursor.execute(querystr, param)
            dataset = cursor.fetchall()
    
            columnNames = [column[0] for column in cursor.description]
    
            for data in dataset:
                result.append( dict(zip( columnNames, data)))
        finally:
            cursor.close()
            
    return result


def panda_uuid():
    import uuid
    return str(uuid.uuid4().hex).upper()


def raw_query_0(querystr):
    from django.db import connection
    result = []
    with connection.cursor() as cursor:
        try:
            cursor.execute(querystr)
            dataset = cursor.fetchall()
    
            columnNames = [column[0] for column in cursor.description]
    
            for data in dataset:
                result.append( dict(zip( columnNames, data)))
        finally:
            cursor.close()
            
    return result

def panda_today():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def refno_seq_gen(curr_refno):
    # string slicing for refno
    sequence = curr_refno[-4:]
    #print("sequence: " + sequence)
    outlet_code = curr_refno[:4]
    #print("outlet_code: " + outlet_code)
    document_type = str(curr_refno[4:6])
    year = str(curr_refno[6:8]).zfill(2)
    #print("year: " + year)
    month = str(curr_refno[9:10]).zfill(2)
    #print("month: " + month)

    new_seq_temp = int(sequence) + 1
    new_seq = str(new_seq_temp)
    new_seq = new_seq.zfill(4)
    fin_refno = outlet_code + document_type + year + month + new_seq
    return fin_refno
