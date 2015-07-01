#!/usr/bin/env python
"""
File containing the main classes of the commbot project.
"""
import datetime
from pprint import pprint
import sys
import time

class CommBot(object):
    def __init__(self, name):
        self.name = name
        self.log_name = 'heart_beats.log'
        self.conf_name = self.name + '.conf'
        self.sleep_interval = 6
        self.log_lines_remembered = 10
        self.known_commbots = []
        self.known_active_commbots = []
        self.watching_files = False
        self.watched_files = {}
        self.watching = True
        self.report = ''
        self.default_conf = """# commbot configuration file
sleep_interval=3
name={}
heartbeat_log_name=heart_beats.log
log_lines_remembered=10
""".format(name)
    def open_or_create_file(self, file_name, permissions):
        self.file_name = file_name
        self.new_file = False
        print "\nOpening " + file_name + "..."
        if permissions == 'read':
            try:
                self._file = open(file_name, 'r')
            except IOError:
                self.new_file = True
                print "No file " + file_name + " found. Creating file..."
                self._file = open(file_name, 'a')
        if permissions == 'append':
            self._file = open(file_name, 'a')
        return self._file

    def close_file(self):
        print "\nClosing " + self.file_name + "..."
        self._file.close()

    def open_or_create_log(self):
        self.update_log()
        self.close_file()

    def update_log(self):
        self.open_or_create_file(self.log_name, 'append')
        if str(self.file_name) == str(self.log_name):
            self._file.write(str(self.name) + " Heartbeat. " + str(datetime.datetime.utcnow()) + "\n")
            if self.report != '':
                self._file.write(str(self.name) + " Watched files, " + self.report)

    def open_or_create_conf(self):
        self.open_or_create_file(self.conf_name, 'read')
        if self.new_file == True:
            if str(self.file_name) == str(self.conf_name):
                self._file.write(self.default_conf)
                self.close_file()
                self._file = open(self.conf_name, 'r')
        self.conf = self._file.readlines()
        return self.conf

    def conf_dictify(self):
        if self.conf:
            print "Extracting configuration information from " + self.conf_name + "..."
            split_lines = []
            for line in self.conf:
                line = line.replace(' =', '=').replace('= ', '=').strip('\n')
                split_line = line.split('=')
                split_lines.append(split_line)
            self.conf_dict = {split_lines[i][0] : split_lines[i][1] for i in xrange(len(split_lines)) if split_lines[i][0][0] != '#'}
            print repr(self.conf_dict)
            return self.conf_dict
        else:
            print "No configuration information available."

    def read_conf(self):
        print "Reading configuration file..."
        if 'sleep_interval' in self.conf_dict:
            self.sleep_interval = int(self.conf_dict['sleep_interval'])
            print "Sleep_interval updated to " + str(self.sleep_interval)
        if 'name' in self.conf_dict:
            self.name = str(self.conf_dict['name'])
        if 'heartbeat_log_name' in self.conf_dict:
            self.log_name = self.conf_dict['heartbeat_log_name']
        if 'log_lines_remembered' in self.conf_dict:
            self.log_lines_remembered = self.conf_dict['log_lines_remembered']

    def sleeping(self):
        print "Sleeping for " + str(self.sleep_interval) + " seconds..."
        time.sleep(int(self.sleep_interval))

    def status_report(self):
        print "\r\n"
        stars = '*' * 5
        print stars + " Status report for " + str(self.name) + ": " + stars
        print "Name: " + str(self.name)
        print "Log File Name: " + str(self.log_name)
        print "Configuration File Name: " + str(self.conf_name)
        print "Sleep interval: " + str(self.sleep_interval)
        print "\r\n"

    def check_active_commbot(self):
        self.known_active_commbots = []
        self.open_or_create_file(self.log_name, 'read')
        self.known_log_lines = self._file.readlines()[-1 * int(self.log_lines_remembered):]
        self.close_file()
        print "\nReading the log..."
        pprint(self.known_log_lines)
        for line in self.known_log_lines:
            split_line = line.split()
            commbot_name = split_line[0]
            comm_type = split_line[1]
            comm_date = split_line[2]
            comm_time = split_line[3]
            if commbot_name != self.name:
                if commbot_name not in self.known_commbots:
                    self.known_commbots.append(commbot_name)
                if commbot_name not in self.known_active_commbots:
                    self.known_active_commbots.append(commbot_name)
        print "\nKnown commbots:"
        for commbot in self.known_commbots:
            print commbot
        print "\nKnown active commbots:"
        for commbot in self.known_active_commbots:
            print commbot

    def watch_files(self, filename_list=[]):
        file_changed = False
        changed_files = []
        for filename in filename_list:
            _file = open(filename, 'r')
            contents = ' '.join(_file.readlines())
            _file.close()
            if filename not in self.watched_files:
                self.watched_files[filename] = contents
            else:
                if self.watched_files[filename] != contents:
                    file_changed = True
                    changed_files.append(filename + ' discovered@UTC: ' + repr(datetime.datetime.utcnow()))
        return file_changed, changed_files

    def auto_watch(self):
        self.report = ''
        currently_watched = []
        for filename in self.watched_files:
            currently_watched.append(filename)
        file_changed, changed_files = self.watch_files(currently_watched)
        if file_changed:
            if len(changed_files) == 1:
                self.report = 'The following file was changed: ' + changed_files[0]
            else:
                self.report = 'The following files were changed: ' + ', '.join(changed_files)

    def stop_watching_files(self, filename_list=[]):
        for filename in filename_list:
            try:
                del self.watched_files[filename]
            except:
                print 'Unable to stop watching filename ' + repr(filename)

    def main_loop(self):
        self.open_or_create_log()
        self.open_or_create_conf()
        self.conf_dictify()
        self.read_conf()
        self.close_file()
        self.sleeping()
        self.status_report()
        if self.watching:
            self.auto_watch()
        self.check_active_commbot()
