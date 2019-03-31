# Python bytecode 2.6 (decompiled from Python 2.7)
# Embedded file name: scripts/common/Lib/CGIHTTPServer.py
# Compiled at: 2010-05-25 20:46:16
"""CGI-savvy HTTP Server.

This module builds on SimpleHTTPServer by implementing GET and POST
requests to cgi-bin scripts.

If the os.fork() function is not present (e.g. on Windows),
os.popen2() is used as a fallback, with slightly altered semantics; if
that function is not present either (e.g. on Macintosh), only Python
scripts are supported, and they are executed by the current process.

In all cases, the implementation is intentionally naive -- all
requests are executed sychronously.

SECURITY WARNING: DON'T USE THIS CODE UNLESS YOU ARE INSIDE A FIREWALL
-- it may execute arbitrary Python code or external programs.

Note that status code 200 is sent prior to execution of a CGI script, so
scripts cannot send other status codes such as 302 (redirect).
"""
__version__ = '0.4'
__all__ = ['CGIHTTPRequestHandler']
import os
import sys
import urllib
import BaseHTTPServer
import SimpleHTTPServer
import select

class CGIHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """Complete HTTP server with GET, HEAD and POST commands.
    
    GET and HEAD also support running CGI scripts.
    
    The POST command is *only* implemented for CGI scripts.
    
    """
    have_fork = hasattr(os, 'fork')
    have_popen2 = hasattr(os, 'popen2')
    have_popen3 = hasattr(os, 'popen3')
    rbufsize = 0

    def do_POST(self):
        """Serve a POST request.
        
        This is only implemented for CGI scripts.
        
        """
        if self.is_cgi():
            self.run_cgi()
        else:
            self.send_error(501, 'Can only POST to CGI scripts')

    def send_head(self):
        """Version of send_head that support CGI scripts"""
        if self.is_cgi():
            return self.run_cgi()
        else:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

    def is_cgi(self):
        """Test whether self.path corresponds to a CGI script,
        and return a boolean.
        
        This function sets self.cgi_info to a tuple (dir, rest)
        when it returns True, where dir is the directory part before
        the CGI script name.  Note that rest begins with a
        slash if it is not empty.
        
        The default implementation tests whether the path
        begins with one of the strings in the list
        self.cgi_directories (and the next character is a '/'
        or the end of the string).
        """
        path = self.path
        for x in self.cgi_directories:
            i = len(x)
            if path[:i] == x and (not path[i:] or path[i] == '/'):
                self.cgi_info = (path[:i], path[i + 1:])
                return True

        return False

    cgi_directories = ['/cgi-bin', '/htbin']

    def is_executable(self, path):
        """Test whether argument path is an executable file."""
        return executable(path)

    def is_python(self, path):
        """Test whether argument path is a Python script."""
        head, tail = os.path.splitext(path)
        return tail.lower() in ('.py', '.pyw')

    def run_cgi(self):
        """Execute a CGI script."""
        path = self.path
        dir, rest = self.cgi_info
        i = path.find('/', len(dir) + 1)
        while 1:
            if i >= 0:
                nextdir = path[:i]
                nextrest = path[i + 1:]
                scriptdir = self.translate_path(nextdir)
                dir, rest = os.path.isdir(scriptdir) and nextdir, nextrest
                i = path.find('/', len(dir) + 1)
            else:
                break

        i = rest.rfind('?')
        if i >= 0:
            rest, query = rest[:i], rest[i + 1:]
        else:
            query = ''
        i = rest.find('/')
        if i >= 0:
            script, rest = rest[:i], rest[i:]
        else:
            script, rest = rest, ''
        scriptname = dir + '/' + script
        scriptfile = self.translate_path(scriptname)
        if not os.path.exists(scriptfile):
            self.send_error(404, 'No such CGI script (%r)' % scriptname)
            return
        elif not os.path.isfile(scriptfile):
            self.send_error(403, 'CGI script is not a plain file (%r)' % scriptname)
            return
        else:
            ispy = self.is_python(scriptname)
            if not ispy:
                if not self.have_fork:
                    if not self.have_popen2:
                        if not self.have_popen3:
                            self.send_error(403, 'CGI script is not a Python script (%r)' % scriptname)
                            return
                        if not self.is_executable(scriptfile):
                            self.send_error(403, 'CGI script is not executable (%r)' % scriptname)
                            return
                    env = {}
                    env['SERVER_SOFTWARE'] = self.version_string()
                    env['SERVER_NAME'] = self.server.server_name
                    env['GATEWAY_INTERFACE'] = 'CGI/1.1'
                    env['SERVER_PROTOCOL'] = self.protocol_version
                    env['SERVER_PORT'] = str(self.server.server_port)
                    env['REQUEST_METHOD'] = self.command
                    uqrest = urllib.unquote(rest)
                    env['PATH_INFO'] = uqrest
                    env['PATH_TRANSLATED'] = self.translate_path(uqrest)
                    env['SCRIPT_NAME'] = scriptname
                    if query:
                        env['QUERY_STRING'] = query
                    host = self.address_string()
                    if host != self.client_address[0]:
                        env['REMOTE_HOST'] = host
                    env['REMOTE_ADDR'] = self.client_address[0]
                    authorization = self.headers.getheader('authorization')
                    if authorization:
                        authorization = authorization.split()
                        if len(authorization) == 2:
                            import base64, binascii
                            env['AUTH_TYPE'] = authorization[0]
                            if authorization[0].lower() == 'basic':
                                try:
                                    authorization = base64.decodestring(authorization[1])
                                except binascii.Error:
                                    pass
                                else:
                                    authorization = authorization.split(':')
                                    if len(authorization) == 2:
                                        env['REMOTE_USER'] = authorization[0]
                    if self.headers.typeheader is None:
                        env['CONTENT_TYPE'] = self.headers.type
                    else:
                        env['CONTENT_TYPE'] = self.headers.typeheader
                    length = self.headers.getheader('content-length')
                    if length:
                        env['CONTENT_LENGTH'] = length
                    referer = self.headers.getheader('referer')
                    if referer:
                        env['HTTP_REFERER'] = referer
                    accept = []
                    for line in self.headers.getallmatchingheaders('accept'):
                        if line[:1] in '\t\n\r ':
                            accept.append(line.strip())
                        else:
                            accept = accept + line[7:].split(',')

                    env['HTTP_ACCEPT'] = ','.join(accept)
                    ua = self.headers.getheader('user-agent')
                    if ua:
                        env['HTTP_USER_AGENT'] = ua
                    co = filter(None, self.headers.getheaders('cookie'))
                    if co:
                        env['HTTP_COOKIE'] = ', '.join(co)
                    for k in ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH', 'HTTP_USER_AGENT', 'HTTP_COOKIE', 'HTTP_REFERER'):
                        env.setdefault(k, '')

                    os.environ.update(env)
                    self.send_response(200, 'Script output follows')
                    decoded_query = query.replace('+', ' ')
                    if self.have_fork:
                        args = [script]
                        if '=' not in decoded_query:
                            args.append(decoded_query)
                        nobody = nobody_uid()
                        self.wfile.flush()
                        pid = os.fork()
                        pid, sts = pid != 0 and os.waitpid(pid, 0)
                        while 1:
                            if not (select.select([self.rfile], [], [], 0)[0] and self.rfile.read(1)):
                                break

                        sts and self.log_error('CGI script exit status %#x', sts)
                    return
                try:
                    try:
                        os.setuid(nobody)
                    except os.error:
                        pass

                    os.dup2(self.rfile.fileno(), 0)
                    os.dup2(self.wfile.fileno(), 1)
                    os.execve(scriptfile, args, os.environ)
                except:
                    self.server.handle_error(self.request, self.client_address)
                    os._exit(127)

            elif self.have_popen2 or self.have_popen3:
                import shutil
                if self.have_popen3:
                    popenx = os.popen3
                else:
                    popenx = os.popen2
                cmdline = scriptfile
                if self.is_python(scriptfile):
                    interp = sys.executable
                    if interp.lower().endswith('w.exe'):
                        interp = interp[:-5] + interp[-4:]
                    cmdline = '%s -u %s' % (interp, cmdline)
                if '=' not in query and '"' not in query:
                    cmdline = '%s "%s"' % (cmdline, query)
                self.log_message('command: %s', cmdline)
                try:
                    nbytes = int(length)
                except (TypeError, ValueError):
                    nbytes = 0

                files = popenx(cmdline, 'b')
                fi = files[0]
                fo = files[1]
                if self.have_popen3:
                    fe = files[2]
                if self.command.lower() == 'post' and nbytes > 0:
                    data = self.rfile.read(nbytes)
                    fi.write(data)
                while 1:
                    if not (select.select([self.rfile._sock], [], [], 0)[0] and self.rfile._sock.recv(1)):
                        break

                fi.close()
                shutil.copyfileobj(fo, self.wfile)
                if self.have_popen3:
                    errors = fe.read()
                    fe.close()
                    if errors:
                        self.log_error('%s', errors)
                sts = fo.close()
                if sts:
                    self.log_error('CGI script exit status %#x', sts)
                else:
                    self.log_message('CGI script exited OK')
            else:
                save_argv = sys.argv
                save_stdin = sys.stdin
                save_stdout = sys.stdout
                save_stderr = sys.stderr
                try:
                    save_cwd = os.getcwd()
                    try:
                        sys.argv = [scriptfile]
                        if '=' not in decoded_query:
                            sys.argv.append(decoded_query)
                        sys.stdout = self.wfile
                        sys.stdin = self.rfile
                        execfile(scriptfile, {'__name__': '__main__'})
                    finally:
                        sys.argv = save_argv
                        sys.stdin = save_stdin
                        sys.stdout = save_stdout
                        sys.stderr = save_stderr
                        os.chdir(save_cwd)

                except SystemExit as sts:
                    self.log_error('CGI script exit status %s', str(sts))
                else:
                    self.log_message('CGI script exited OK')

            return


nobody = None

def nobody_uid():
    """Internal routine to get nobody's uid"""
    global nobody
    if nobody:
        return nobody
    try:
        import pwd
    except ImportError:
        return -1

    try:
        nobody = pwd.getpwnam('nobody')[2]
    except KeyError:
        nobody = 1 + max(map(lambda x: x[2], pwd.getpwall()))

    return nobody


def executable(path):
    """Test for executable file."""
    try:
        st = os.stat(path)
    except os.error:
        return False

    return st.st_mode & 73 != 0


def test(HandlerClass=CGIHTTPRequestHandler, ServerClass=BaseHTTPServer.HTTPServer):
    SimpleHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()