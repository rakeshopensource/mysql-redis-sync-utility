import redis
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

MYSQL_SETTINGS = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "mysql"
}

ONLY_Tables = {
	'table_name'
}


def diff(first, second):
    KEYNOTFOUND = '<KEYNOTFOUND>'       # KeyNotFound for dictDiff
    diff = {}
  
    for key in first.keys():
        if (not second.has_key(key)):
            diff[key] = (first[key], KEYNOTFOUND)
        elif (first[key] != second[key]):
            diff[key] = (first[key], second[key])
   
    for key in second.keys():
        if (not first.has_key(key)):
            diff[key] = (KEYNOTFOUND, second[key])
    return diff

def updateRediSCache(insertupdate,prefix,keys, row):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for key in keys:	    
	cacheKey = prefix + key
	if insertupdate: 	
	    cacheValue = row[key]
	    r.set(cacheKey,cacheValue);
            print "Updated Cache -> " +  cacheKey  + " : " + cacheValue
	else:
	    r.delete(cacheKey)
	    print "Updated Cache -> " +  cacheKey  + " Removed "	

def main():
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,server_id=1,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],only_tables=ONLY_Tables)

    for binlogevent in stream:       
	prefix = "%s-%s-" % (binlogevent.schema, binlogevent.table)
        for row in binlogevent.rows:
            if isinstance(binlogevent, DeleteRowsEvent):
                vals = row["values"]
		print "[Delete] SQLBinLog Row :" + str(row)
                updateRediSCache(False,prefix,vals.keys(),vals) 
            elif isinstance(binlogevent, UpdateRowsEvent):
		before_values = row["before_values"]
		after_values = row["after_values"]
		print "[Update] SQLBinLog Row :" + str(row)	
		updateRediSCache(True,prefix,diff(before_values,after_values).keys(),after_values)
            elif isinstance(binlogevent, WriteRowsEvent):
                vals = row["values"]
		print "[Insert] SQLBinLog Row :" + str(row)		
		updateRediSCache(True,prefix,vals.keys(),vals)            

    stream.close()


if __name__ == "__main__":
    main()
			
