#!/usr/bin/env python
# vim:set softtabstop=4 shiftwidth=4 tabstop=4 expandtab:

import os
import subprocess
from sys import stderr

GIT_COMMAND="git"


class SCM(object):
    def __init__(self):
        pass
    
    def runCommand(self, cmdList):
        # Raises OSError if command doesn't exist
        proc = subprocess.Popen(cmdList, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=os.getcwd())
        stdout, stderr = proc.communicate()
        return stdout, stderr, proc.returncode


class Git(SCM):
    def __init__(self, gitCmd=GIT_COMMAND):
        self.ranStatus = False
        self.command = gitCmd
        self.cwd = None
        self.branch = ""
        self.remoteBranch = ""
        self.staged = ""
        self.changed = ""
        self.untracked = ""
        self.unmerged = ""
        self.ahead = ""
        self.behind = ""


    def __getattribute__(self, name):
        """
        If we have not yet run a status call then run one before
        attempting to get the attribute. _runStatus() is also called
        again if the working directory has changed.
        """
        if not object.__getattribute__(self, "ranStatus") or object.__getattribute__(self, "cwd") != os.getcwd():
            self.cwd = os.getcwd()
            self.ranStatus = True
            self._runStatus()
        return object.__getattribute__(self, name)


    def _runStatus(self):
        try:
            (stdout, stderr, returncode) = self.runCommand([self.command, "status", "--porcelain", "-b"])
        except OSError:
            # Git command not found
            self.installed = False
            self.isRepo = False
            return
        
        if returncode == 0:
            # Successful git status call
            self.installed = True
            self.isRepo = True
            (self.branch, 
            self.remoteBranch, 
            self.staged,
            self.changed, 
            self.untracked, 
            self.unmerged,
            self.ahead, 
            self.behind) = self._git_status(stdout)
        else:
            if "Not a git repository" in stderr:
                # The directory is not a git repo
                self.installed = True
                self.isRepo = False
            else:
                # Some other error?
                self.installed = False
                self.isRepo = False


    def _git_status(self, result):
        """
        Originally taken from https://github.com/dreadatour/dotfiles
        
        Get git status.
        """
        branch = remote_branch = ''
        staged = changed = untracked = unmerged = ahead = behind = 0
        for line in result.splitlines():
            line = line.decode('utf-8')
            prefix = line[0:2]
            line = line[3:]
    
            if prefix == '##':  # branch name + ahead & behind info
                branch, remote_branch, ahead, behind = self._parse_git_branch(line)
            elif prefix == '??':  # untracked file
                untracked += 1
            elif prefix in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):  # unmerged
                unmerged += 1
            else:
                if prefix[0] in ('M', 'A', 'D', 'R', 'C'):  # changes in index
                    staged += 1
                if prefix[1] in ('M', 'D'):  # changes in work tree
                    changed += 1
    
        return (branch, remote_branch, staged, changed, untracked, unmerged,
                ahead, behind)


    def _parse_git_branch(self, line):
        """
        Originally taken from https://github.com/dreadatour/dotfiles
        
        Parse 'git status -b --porcelain' command branch info output.
    
        Possible strings:
        - simple: "## dev"
        - detached: "## HEAD (no branch)"
        - ahead/behind: "## master...origin/master [ahead 1, behind 2]"
    
        Ahead/behind format:
        - [ahead 1]
        - [behind 1]
        - [ahead 1, behind 1]
        """
        branch = remote_branch = ''
        ahead = behind = 0
    
        if line == 'HEAD (no branch)':  # detached state
            branch = '#' + self._git_commit()
        elif '...' in line:  # ahead of or behind remote branch
            if ' ' in line:
                branches, ahead_behind = line.split(' ', 1)
            else:
                branches, ahead_behind = line, None
            branch, remote_branch = branches.split('...')
    
            if ahead_behind and ahead_behind[0] == '[' and ahead_behind[-1] == ']':
                ahead_behind = ahead_behind[1:-1]
                for state in ahead_behind.split(', '):
                    if state.startswith('ahead '):
                        ahead = state[6:]
                    elif state.startswith('behind '):
                        behind = state[7:]
        else:
            branch = line
    
        return branch, remote_branch, ahead, behind


    def _git_commit(self):
        """
        Originally taken from https://github.com/dreadatour/dotfiles
        
        Get git HEAD commit hash.
        """
        git_cmd = [self.command, 'rev-parse', '--porcelain', '--short', 'HEAD']
        return self.runCommand(git_cmd)


#--------------------------
# Prompty functions
#--------------------------
def isgitrepo(status):
    return status.git.isRepo

def gitbranch(status):
    return status.git.branch

