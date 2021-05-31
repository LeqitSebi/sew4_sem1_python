#!/usr/bin/python3.7

import re
import gzip


LINE_PATTERN = re.compile(r'^(\d+\.\d+)\s+(\d+) (.+?) (.+?)/(\d{3}) (\d+) (.+?) (https?)://([^/]+)(.+) - (.+?)/(.+?) (.+)$')
APACHE_LOG_PATTERN = re.compile(r'^([^ ]+) ([^ ]+) ([^ ]+) \[(.+?)\] "([^"]+)" (\d{3}) ([^ ]+) "(.+?)" "(.+?)"$')
APACHE_REQUEST_PATTERN = re.compile(r'^(.+?) (.+) HTTP/(\d\.\d)$')
URL_PATTERN = re.compile(r'(https?)://([^/]+)(.+)')
USER_AGENT_PATTERN = re.compile(r'^Mozilla/5.0 \(([^;)]+)[^)]*\)')

WINDOWS_VERSIONS = {
    '5.0': 'Windows 2000',
    '5.1': 'Windows XP',
    '6.0': 'Windows Vista',
    '10.0': 'Windows 10',
    '6.3': 'Windows 8.1',
    '6.1': 'Windows 7'
}


class Record:
    def __init__(self, line):
        m = re.match(APACHE_LOG_PATTERN, line)
        if not m:
            raise Exception('Illegal line format: <' + line + '>')
        self.source = m.group(1)
        self._2 = m.group(2)
        self.user = m.group(3)
        if self.user == '-':
            self.user = None
        self.timestamp = m.group(4)
        self.request = m.group(5)
        m2 = re.match(APACHE_REQUEST_PATTERN, self.request)
        if m2:
            self.method = m2.group(1)
            self.uri = m2.group(2)
            m3 = re.match(URL_PATTERN, self.uri)
            if m3:
                self.url = self.uri
                self.uri = m3.group(3)
                self.host = m3.group(2)
            else:
                self.host = 'localhost'
                self.url = 'http://' + self.host + self.uri
        else:
            self.method = None
            self.uri = None
            self.url = None
            self.host = None
        self.code = int(m.group(6))
        if m.group(7) == '-':
            self.transferred = 0
        else:
            self.transferred = int(m.group(7))
        self.referer = m.group(8)
        self.user_agent = m.group(9)
        m2 = re.match(USER_AGENT_PATTERN, self.user_agent)
        if m2:
            os = m2.group(1)
            if os.startswith('Windows NT'):
                version = os[11:]
                self.os = WINDOWS_VERSIONS.get(version, os)
            elif os == 'Linux':
                self.os = 'Linux'
            elif 'mac' in os.lower():
                self.os = 'Mac'
            else:
                self.os = 'bot'
        else:
            self.os = 'bot'


def open_files(filenames):
    for filename in filenames:
        if filename.endswith('.gz') or filename.endswith('.zip'):
            yield gzip.open(filename, 'r')
        else:
            yield open(filename, 'rb')


def read_lines(files):
    for file in files:
        for line in file.readlines():
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                line = line.decode('latin-1')
            yield line.strip()


def parse_lines(lines):
    for line in lines:
        yield Record(line)


def get_bytes(records):
    return sum(r.transferred for r in records)


def get_most_active_source(records):
    sources = {}
    for r in records:
        sources[r.source] = sources.get(r.source, 0) + 1
    max_req = 0
    max_source = None
    for k,v in sources.items():
        if v > max_req:
            max_req, max_source = v, k
    return max_source

def get_most_used_os(records):
    systems = {}
    for r in records:
        systems[r.os] = systems.get(r.os, 0) + 1
    max_req = 0
    max_os = None
    for k,v in systems.items():
        if v > max_req:
            max_req, max_os = v,k
    return max_os


def get_most_surfed_page(records):
    uris = {}
    for r in records:
        if r.code != 408:
            uris[r.uri] = uris.get(r.uri, 0) + 1
    max_req = 0
    max_uri = None
    for k,v in uris.items():
        if v > max_req:
            max_req, max_uri = v, k
    #print(max_req)
    return max_uri


if __name__ == '__main__':
    files = open_files(['../resources/access.log'])
    lines = read_lines(files)
    records = parse_lines(lines)
    print(get_most_used_os(records))