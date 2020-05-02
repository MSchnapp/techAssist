import pymongo
import time
import sys
import pyautogui as py
import automation as TA
from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint


client = MongoClient('mongodb+srv://mschnapp:Astech0099!@techAssist-3kix2.mongodb.net/test?retryWrites=true&w=majority', 8000)
db = client.tools
collection = db['tools']
tool = collection.find_one({'toolName': 'gmpdc179'})['_id']
pprint(tool)

x = ObjectId('5eaa38d9b216569272d33cb3')

if x == tool:
    paired_status = {'_id': x, 'paired': False}
    updated_paired = { "$set": {'paired': True}}
    collection.update_one(paired_status, updated_paired)
    print('Paired Successfully')
    scan_to_do = None

    while scan_to_do is None:

        try:
            scantype_pre = collection.find_one(tool)['prescan']
            scantype_post = collection.find_one(tool)['postscan']
            scan_current = collection.find_one(tool)['scancurrent']
            error_current = collection.find_one(tool)['error']

            if scantype_pre == True and scan_current == False and error_current == False:
                print('Pre-Scan')

                current_scan = {'_id': x, 'scancurrent': False}
                set_true_scan = { "$set": {'scancurrent': True}}
                collection.update_one(current_scan, set_true_scan)

                TA.preScanSelection()
                print('Done with Scan')

                current = {'_id': x, 'prescan': True}
                set_true = { "$set": {'prescan': False}}
                collection.update_one(current, set_true)

                if TA.errorSet == 1:
                    status_current = {'_id': x, 'error': False}
                    status_set = { "$set": {'error': True}}
                    collection.update_one(status_current, status_set)

            elif scantype_post == True and scan_current == False and error_current == False:

                current_scan = {'_id': x, 'scancurrent': False}
                set_true_scan = { "$set": {'scancurrent': True}}
                collection.update_one(current_scan, set_true_scan)

                print('Completion-Scan')
                TA.completionScanSelection()
                print('Done with Scan')

                current = {'_id': x, 'postscan': True}
                set_true = { "$set": {'postscan': False}}
                collection.update_one(current, set_true)

                if TA.errorSet == 1:
                    status_current = {'_id': x, 'error': False}
                    status_set = { "$set": {'error': True}}
                    collection.update_one(status_current, status_set)

            elif scan_current == True and TA.report_finished == 1:
                current_scan = {'_id': x, 'scancurrent': True}
                set_true_scan = { "$set": {'scancurrent': False}}
                collection.update_one(current_scan, set_true_scan)
                TA.report_finished = 0

            elif scan_current == True and error_current == True:
                current_scan = {'_id': x, 'scancurrent': True}
                set_true_scan = { "$set": {'scancurrent': False}}
                collection.update_one(current_scan, set_true_scan)


            elif error_current == True and scan_current == False and scantype_post == False and scantype_pre == False and TA.report_finished == 0:
                py.alert("Please Resolve Issue then click OK")
                status_current = {'_id': x, 'error': True}
                status_set = { "$set": {'error': False}}
                collection.update_one(status_current, status_set)
                print('Cleared error')
                TA.errorSet = 0

            else:
                time.sleep(5)
                print('No Scan Found')

        except KeyboardInterrupt:
            paired_status = {'_id': x, 'paired': True}
            updated_paired = { "$set": {'paired': False}}
            collection.update_one(paired_status, updated_paired)
            status_current = {'_id': x, 'error': False}
            status_set = { "$set": {'error': True}}
            collection.update_one(status_current, status_set)
            print('Disconnected due to Keyboard Interrupt')
            sys.exit(-1)
        except OSError:
            paired_status = {'_id': x, 'paired': True}
            updated_paired = { "$set": {'paired': False}}
            collection.update_one(paired_status, updated_paired)
            status_current = {'_id': x, 'error': False}
            status_set = { "$set": {'error': True}}
            collection.update_one(status_current, status_set)
            print('Disconnected due to OSError')
            sys.exit(-1)
        except:
            paired_status = {'_id': x, 'paired': True}
            updated_paired = { "$set": {'paired': False}}
            collection.update_one(paired_status, updated_paired)
            time.sleep(1)
            scan_to_do = None
            print('Disconnected from Server')
else:
    print('Failed to Pair')
#serverStatusResult = db.command('serverStatus')
#pprint(serverStatusResult)

