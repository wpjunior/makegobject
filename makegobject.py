#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2008 Wilson Pinto Júnior (N3RD3X) <n3rd3x@guake-terminal.org>
#  Copyright (C) 2008 Lincoln de Sousa <lincoln@minaslivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import time

HEADER = """\
/**
 * Copyright (C) %(year)s %(copyright_holder)s
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _%(upper_name)s_H
#define _%(upper_name)s_H

#define _GNU_SOURCE
#include <glib.h>
#include <glib-object.h>

G_BEGIN_DECLS
#define %(upper_name)s_TYPE                  (%(lower_name)s_get_type ())
#define %(upper_name)s(obj)                  (G_TYPE_CHECK_INSTANCE_CAST ((obj), %(upper_name)s_TYPE, %(capitalized_name)s))
#define %(upper_name)s_CLASS(klass)          (G_TYPE_CHECK_CLASS_CAST ((klass), %(upper_name)s_TYPE, %(capitalized_name)sClass))
#define IS_%(upper_name)s(obj)               (G_TYPE_CHECK_INSTANCE_TYPE ((obj), %(upper_name)s_TYPE))
#define IS_%(upper_name)s_CLASS(klass)       (G_TYPE_CHECK_CLASS_TYPE ((klass), %(upper_name)s_TYPE))
#define %(upper_name)s_GET_CLASS(obj)        (G_TYPE_INSTANCE_GET_CLASS ((obj), %(upper_name)s_TYPE, %(capitalized_name)sClass))

typedef struct _%(capitalized_name)s %(capitalized_name)s;
typedef struct _%(capitalized_name)sClass %(capitalized_name)sClass;

struct _%(capitalized_name)s
{
  /*< private >*/
  GObject parent;
};

struct _%(capitalized_name)sClass
{
  /*< private >*/
  GObjectClass parent;
};

GType %(lower_name)s_get_type (void) G_GNUC_CONST;
%(capitalized_name)s *%(lower_name)s_new (void);

G_END_DECLS

#endif /* _%(upper_name)s_H */
"""

SOURCE = """\
/**
 * Copyright (C) %(year)s %(copyright_holder)s
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <glib.h>
#include "%(header_filename)s"

G_DEFINE_TYPE (%(capitalized_name)s, %(lower_name)s, G_TYPE_OBJECT);

static void
%(lower_name)s_class_init (%(capitalized_name)sClass *klass)
{
}

static void
%(lower_name)s_init (%(capitalized_name)s *self)
{
  self = %(upper_name)s (self);
}

%(capitalized_name)s *
%(lower_name)s_new (void)
{
  %(capitalized_name)s *obj;
  obj = g_object_new (%(upper_name)s_TYPE, NULL);
  return obj;
}
"""


def main(ch, obj):
    data = {}
    data['copyright_holder'] = ch

    obj_name = obj
    
    if "-" in obj_name:
        names = obj_name.split("-")
    elif "_" in obj_name:
        names = obj_name.split("_")
    else:
        names = obj_name.split(" ")

    data['upper_name'] = "_".join(names).upper()
    data['lower_name'] = "_".join(names).lower()

    data['capitalized_name'] = ""
    for name in names:
        data['capitalized_name'] += name.capitalize()

    data['header_filename'] = data['lower_name'] + ".h"
    data['source_filename'] = data['lower_name'] + ".c"
    data['year'] = time.localtime()[0]

    open(data['header_filename'], 'wb').write(HEADER % data)
    print "Wrote %s" % data['header_filename']

    open(data['source_filename'], 'wb').write(SOURCE % data)
    print "Wrote %s"% data['source_filename']


if __name__ == '__main__':
    from optparse import OptionParser
    from pwd import getpwuid

    email = os.getenv('EMAIL') or getpwuid(os.getuid())[4].split(',')[0]

    parser = OptionParser()
    parser.usage += ' object-name'
    parser.add_option('-c', '--copyright-holder',
                      dest='copyright_holder',
                      action='store', default=email,
                      help='The copyright holder name and email')

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        parser.exit(-1)

    main(options.copyright_holder, args[0])
