import StringIO
import tokenize
import re
import sublime, sublime_plugin

class BraceToDoEndCommand(sublime_plugin.TextCommand):
  def find(self, collection, f):
    for i in collection:
      if f(i):
        return i
    return None

  def braces(self):
    view = self.view
    opening_points = []
    braces = {}

    content = view.substr(sublime.Region(0, view.size()))
    tokens = tokenize.generate_tokens(StringIO.StringIO(content).readline)
    for num, val, start, _, _ in tokens:
      if num == tokenize.OP:
        start_point = view.text_point(start[0] - 1, start[1])
        if val == '{':
          opening_points.append(start_point)
        elif val == '}':
          if opening_points:
            braces[opening_points.pop()] = start_point

    return braces

  def run(self, edit):
    view = self.view
    sel = view.sel()
    braces = self.braces()

    opening_points = braces.keys()
    opening_points.sort(None, None, True)  # reverse

    points_to_replace = set()
    for region in sel:
      opening_point = self.find(opening_points, lambda p: p <= region.b)
      if opening_point:
        points_to_replace.add(opening_point)
        points_to_replace.add(braces[opening_point])

    points_to_replace = list(points_to_replace)
    points_to_replace.sort(None, None, True)

    lines_to_reindent = set()
    for p in points_to_replace:
      if p in opening_points:
        # f{          f do
        # f{|a|       f do |a|
        # f{ |a|      f do |a|
        # f{a}        f do\n
        # f{|a|a}     f do |a|\n
        # f{ |a|a}    f do |a|\n
        # f{|a| a}    f do |a|\n
        # f{ |a| a}   f do |a|\n
        # f { |a| a}  f do |a|\n
        opening_pattern = re.compile('(?P<heading>[ \t])?(?P<opening>\{ *(?P<args>\|[ ,()\w\t]*\|)?[ \t]*)(?P<exp>.*)')
        m = opening_pattern.search(view.substr(sublime.Region(p - 1, view.line(p).b)))
        heading   = ''   if m.group('heading') else ' '
        following = ' '  if m.group('args')    else ''
        newline   = '\n' if m.group('exp')     else ''
        region = sublime.Region(p, p + len(m.group('opening')))
        view.replace(edit, region, '%sdo%s%s%s' % (heading, following, m.group('args') or '', newline))
      else:
        # a }
        # }
        m = re.search('[^ \t]+[ \t]*}$', view.substr(sublime.Region(view.line(p).a, p + 1)))
        newline = '\n' if m else ''
        view.replace(edit, sublime.Region(p, p + 1), '%send' % newline)

      if newline:
        lines_to_reindent = set(map(lambda l: l + 1, lines_to_reindent))
        lines_to_reindent.add(view.rowcol(p)[0] + 1)

    for line in lines_to_reindent:
      sel.add(sublime.Region(view.text_point(line, 0)))
    view.run_command('reindent', {'force_indent': False})
