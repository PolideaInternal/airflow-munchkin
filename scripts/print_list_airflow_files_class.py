# -*- coding: utf-8 -*-
"""
This scripts allows to print Markdown compatible list
of Airflow classes or files.

Moreover, it could narrow the result to only gcp related
stuff and add links to specific files on Polidea/airflow
repo.
"""

import re
import inspect
import pkgutil
import argparse

from functools import partial
from importlib import import_module

from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator

parser = argparse.ArgumentParser(
    description="Generates list of all classes or files in airflow."
)
parser.add_argument(
    "-gcp",
    "--g",
    action="store_true",
    dest="gcp",
    help="If set then only GCP related stuff is printed",
)
parser.add_argument(
    "-files",
    "--f",
    action="store_true",
    dest="file",
    help="If set then files names are printed instead of class names.",
)
parser.add_argument(
    "-links", "--l", action="store_true", dest="links", help="Add repo links to files."
)
parser.add_argument(
    "-verbose",
    "--v",
    action="store_true",
    dest="verbose",
    help="Verbosity, prints error when ModuleNotFoundError",
)

ARGS = parser.parse_args()


REPO_URL = "https://github.com/PolideaInternal/airflow/blob/master"


def is_google(doc):
    if not doc:
        return False

    for name in ["gcp", "gcs", "google"]:
        for variation in [name, name.upper(), name.capitalize()]:
            if variation in doc:
                return True
    return False


def find_clazzes(directory, base_class, gcp_related=True, verbose=False):
    found_classes = set()
    for module_finder, name, ispkg in pkgutil.iter_modules([directory]):
        if ispkg:
            continue

        package_name = module_finder.path.replace("/", ".")
        full_module_name = package_name + "." + name
        try:
            mod = import_module(full_module_name)
        except ModuleNotFoundError:
            if verbose:
                print("Error: ", full_module_name)
            continue
        clazzes = inspect.getmembers(mod, inspect.isclass)
        operators_clazzes = [
            clazz
            for name, clazz in clazzes
            if issubclass(clazz, base_class)
            and clazz.__module__.startswith(package_name)
        ]
        # print(name)
        for clazz in operators_clazzes:
            add = (not gcp_related) or (gcp_related and is_google(clazz.__doc__))
            if add:
                found_classes.add("%s.%s" % (clazz.__module__, clazz.__name__))

    return found_classes


def scan(
    directory,
    base_class,
    file_only=False,
    gcp_related=False,
    verbose=False,
    links=False,
):
    # This generates Markdown compatible list
    r = find_clazzes(directory, base_class, gcp_related)

    clazzes = sorted(r, key=lambda cls: cls.rsplit(".", 1)[::-1])

    if file_only:
        filenames = [re.findall(r"([a-z\._0-9]+)\.[A-Z]", f) for f in clazzes]
        filenames = {f[-1] for f in filenames if f}
        for filename in sorted(filenames):
            if links:
                url_part = filename.replace(".", "/")
                link = f"{REPO_URL}/{url_part}.py"
                print("- ", f"[{filename}]({link})")
            else:
                print("- ", filename)
    else:
        for clazz in clazzes:
            print("- ", clazz)


if __name__ == "__main__":
    par_scan = partial(
        scan,
        file_only=ARGS.file,
        gcp_related=ARGS.gcp,
        verbose=ARGS.verbose,
        links=ARGS.links,
    )

    print("## Operators")
    print("### airflow/operators")
    par_scan("airflow/operators", BaseOperator)
    print("### airflow/contrib/operators")
    par_scan("airflow/contrib/operators", BaseOperator)

    print("## Sensors")
    print("### airflow/sensors")
    par_scan("airflow/sensors", BaseOperator)
    print("### airflow/contrib/sensors")
    par_scan("airflow/contrib/sensors", BaseOperator)

    print("## Hooks")
    print("### airflow/hooks")
    par_scan("airflow/hooks", BaseHook)
    print("### airflow/contrib/hooks")
    par_scan("airflow/contrib/hooks", BaseHook)
