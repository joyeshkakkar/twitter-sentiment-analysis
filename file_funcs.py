import os


# remove file if it exists
def remove_file_if_exists(file_name):
    if os.path.exists(file_name):
        try:
            os.remove(file_name)
            print "Removed file %s" % file_name
        except OSError, exception:
            print ("Error: %s - %s." % (exception.filename, exception.strerror))