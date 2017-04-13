from . import *
import argparse
import re
import sys
import json
import enum

class Output(enum.Flag):
    only_path = enum.auto()
    only_object = enum.auto()

    both = only_object | only_path

    default = only_object

class StrComparer:
    def __init__(self, target, is_regex):
        def re_compoile(string):
            if not is_regex:
                return re.compile(f'^{string}$', re.IGNORECASE)
            else:
                return re.compile(string, re.IGNORECASE)

        if isinstance(target, str):
            self.pats = [re_compoile(target)]
        else:
            self.pats = [re_compoile(t) for t in target]

    def __eq__(self, other):
        other = str(other)

        for p in self.pats:
            if p.match(other) is not None:
                return True
        return False

def main():
    args = parse(sys.argv[1:])

    if hasattr(args, 'func'):
        jsprint(args.func(args))
    else:
        parser.print_help()

def parse(args):
    parser = argparse.ArgumentParser(prog='PROG', description='cli tool for accessing data on http://ic.tpex.org.tw/')
    subparser = parser.add_subparsers(help='commands')

    # command `industry`
    parser_industry = subparser.add_parser('industry', help='search industry list')
    parser_industry.set_defaults(func=view_industry)
    set_opt(parser_industry)

    parser_industry.add_argument(
        'target',
        type=str,
        nargs='*',
        action='store',
        help='query target',
        default='.+'
    )

    # command `chain`
    parser_chain = subparser.add_parser('chain', help='view industry chain')
    parser_chain.set_defaults(func=view_chain)
    set_opt(parser_chain)

    parser_chain.add_argument(
        'target',
        type=str,
        nargs='+',
        action='store',
        help='query target',
    )

    # command `fire`
    parser_fire = subparser.add_parser('fire', help='fire query')
    parser_fire.set_defaults(func=fire_query)

    parser_fire.add_argument(
        'args',
        type=str,
        nargs='+',
        action='store',
        help='query args',
    )

    return parser.parse_args(args)

def set_opt(psr):
    psr.add_argument(
        '-f', '--field',
        action='append',
        help='specific search field(s)',
    )

    psr.add_argument(
        '-r', '--regex',
        action='store_true',
        help='use regex to match target',
        default=False
    )

    group_output = psr.add_mutually_exclusive_group()
    psr.set_defaults(output=Output.default)

    group_output.add_argument(
        '-p', '--path-only',
        help='output path only',
        action='store_const',
        dest='output',
        const=Output.only_path
    )

    group_output.add_argument(
        '-o', '--object-only',
        help='output object only',
        action='store_const',
        dest='output',
        const=Output.only_object
    )

    group_output.add_argument(
        '-b', '--both',
        help='output both infomations',
        action='store_const',
        dest='output',
        const=Output.both
    )

def jsprint(obj):
    if obj is None:
        return

    def dump(data):
        print(json.dumps(data, indent=4, ensure_ascii=False))

    if isinstance(obj, dict):
        return dump(obj)

    elif hasattr(obj, '__iter__'):
        return dump(list(obj))

    else:
        raise TypeError()

def search_industry(args):
    fields = set(args.field) if args.field else ['id', 'name']
    comparer = StrComparer(args.target, args.regex)

    def search(obj):
        for f in fields:
            if obj.get(f, None) == comparer:
                return [(str(obj), obj)]

        results = []
        for c in obj.children:
            founds = search(c)
            results.extend([(f'{obj}/{path}', find) for path, find in founds])

        return results

    return search(index())

def view_industry(args):
    for path, obj in search_industry(args):
        if args.output & Output.only_path:
            print(path)
        if args.output & Output.only_object:
            yield obj

def view_chain(args):
    for path, obj in search_industry(args):
        try:
            get = obj.fire_query()

            if args.output & Output.only_path:
                print(f'{path}/query')
            if args.output & Output.only_object:
                yield get

        except RuntimeError:
            if args.output & Output.only_path:
                print(f'{path}: query fail')

def fire_query(args):
    parse_ns = parse(args.args)
    if not hasattr(parse_ns, 'func'):
        return

    founded_dat = parse_ns.func(parse_ns)
    for f in founded_dat:
        try:
            yield f.fire_query()
        except RuntimeError:
            pass

if __name__ == '__main__':
    main()
