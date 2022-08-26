"""
Git SCM backend for Digress.
"""

from subprocess import Popen, PIPE, STDOUT
import re

from digress.errors import SCMError

GIT_BRANCH_EXPR = re.compile("[*] (.*)")

def checkout(revision):
    """
    Checkout a revision from git.
    """
    proc = Popen([
        "git",
        "checkout",
        "-f",
        revision
    ], stdout=PIPE, stderr=STDOUT)

    output = proc.communicate()[0].strip()
    if proc.returncode != 0:
        raise SCMError(f"checkout error: {output}")

def rev_parse(ref):
    proc = Popen([
        "git",
        "rev-parse",
        ref
    ], stdout=PIPE, stderr=STDOUT)

    output = proc.communicate()[0].strip()
    if proc.returncode != 0:
        raise SCMError(f"rev-parse error: {output}")
    return output

def current_rev():
    """
    Get the current revision.
    """
    return rev_parse("HEAD")

def current_branch():
    """
    Get the current branch.
    """
    proc = Popen([
        "git",
        "branch",
        "--no-color"
    ], stdout=PIPE, stderr=STDOUT)

    output = proc.communicate()[0].strip()
    if proc.returncode != 0:
        raise SCMError(f"branch error: {output}")
    branch_name = GIT_BRANCH_EXPR.findall(output)[0]
    return branch_name != "(no branch)" and branch_name or None

def revisions(rev_a, rev_b):
    """
    Get a list of revisions from one to another.
    """
    proc = Popen(
        ["git", "log", "--format=%H", f"{rev_a}...{rev_b}"],
        stdout=PIPE,
        stderr=STDOUT,
    )


    output = proc.communicate()[0].strip()
    if proc.returncode != 0:
        raise SCMError(f"log error: {output}")
    return output.split("\n")

def stash():
    """
    Stash the repository.
    """
    proc = Popen([
        "git",
        "stash",
        "save",
        "--keep-index"
    ], stdout=PIPE, stderr=STDOUT)

    output = proc.communicate()[0].strip()
    if proc.returncode != 0:
        raise SCMError(f"stash error: {output}")

def unstash():
    """
    Unstash the repository.
    """
    proc = Popen(["git", "stash", "pop"], stdout=PIPE, stderr=STDOUT)
    proc.communicate()

def bisect(*args):
    """
    Perform a bisection.
    """
    proc = Popen((["git", "bisect"] + list(args)), stdout=PIPE, stderr=STDOUT)
    output = proc.communicate()[0]
    if proc.returncode != 0:
        raise SCMError(f"bisect error: {output}")
    return output

def dirty():
    """
    Check if the working tree is dirty.
    """
    proc = Popen(["git", "status"], stdout=PIPE, stderr=STDOUT)
    output = proc.communicate()[0].strip()
    if proc.returncode != 0:
        raise SCMError(f"status error: {output}")
    return "modified:" in output
