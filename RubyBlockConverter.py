import StringIO
import tokenize
import re
import sublime, sublime_plugin

def find(collection, f):
  for i in collection:
    if f(i):
      return i
  return None

def search_points_to_replace(command):
  points_to_replace = set()
  for region in command.view.sel():
    opening_point = find(command.opening_points, lambda p: p <= region.b)
    if opening_point:
      points_to_replace.add(opening_point)
      points_to_replace.add(command.blocks[opening_point])

  return list(points_to_replace)

def match_blocks(command, toknum, opening, closing):
  view = command.view
  opening_points = []
  blocks = {}

  content = view.substr(sublime.Region(0, view.size()))
  tokens = tokenize.generate_tokens(StringIO.StringIO(content).readline)
  for num, val, start, _, _ in tokens:
    if num == toknum:
      start_point = view.text_point(start[0] - 1, start[1])
      if val == opening:
        opening_points.append(start_point)
      elif val == closing:
        if opening_points:
          blocks[opening_points.pop()] = start_point

  return blocks

class BraceToDoEndCommand(sublime_plugin.TextCommand):
  lines_to_reindent = set()

  def reserve_reindent(self, line):
    self.lines_to_reindent = set(map(lambda l: l + 1, self.lines_to_reindent))
    self.lines_to_reindent.add(line)

  def reindent(self):
    view = self.view
    sel = view.sel()
    dirty_lines = set()
    for line in self.lines_to_reindent:
      line_end = sublime.Region(view.line(view.text_point(line, 0)).b)
      if not sel.contains(line_end):
        sel.add(line_end)
        dirty_lines.add(line)
    view.run_command('reindent', {'force_indent': False})
    for line in dirty_lines:
      sel.subtract(sublime.Region(view.line(view.text_point(line, 0)).b))

  def run(self, edit):
    view = self.view
    self.blocks = match_blocks(self, tokenize.OP, '{', '}')

    self.opening_points = self.blocks.keys()
    self.opening_points.sort(None, None, True)  # reverse

    points_to_replace = search_points_to_replace(self)
    points_to_replace.sort(None, None, True)

    for p in points_to_replace:
      if p in self.opening_points:
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
        if m.group('exp'):
          newline = '\n'
          self.reserve_reindent(view.rowcol(p)[0] + 1)
        else:
          newline = ''
        region = sublime.Region(p, p + len(m.group('opening')))
        view.replace(edit, region, '%sdo%s%s%s' % (heading, following, m.group('args') or '', newline))
      else:
        # a }
        # a}
        # }
        m = re.search('(?P<exp>[^ \t]*)(?P<spaces>[ \t]*)}$', view.substr(sublime.Region(view.line(p).a, p + 1)))
        if m.group('exp'):
          newline = '\n'
          self.reserve_reindent(view.rowcol(p)[0] + 1)
        else:
          newline = ''
        replace_start = p - (len(m.group('spaces')) if m.group('exp') and m.group('spaces') else 0)
        view.replace(edit, sublime.Region(replace_start, p + 1), '%send' % newline)

    self.reindent()

class DoEndToBraceCommand(sublime_plugin.TextCommand):
  def row_span(self, point):
    return self.view.rowcol(self.blocks[point])[0] - self.view.rowcol(point)[0]

  def run(self, edit):
    view = self.view
    self.blocks = match_blocks(self, tokenize.NAME, 'do', 'end')

    self.opening_points = self.blocks.keys()
    self.opening_points.sort(None, None, True)  # reverse

    points_to_replace = search_points_to_replace(self)
    points_to_replace.sort(None, None, True)

    for p in points_to_replace:
      if p in self.opening_points:
        if self.row_span(p) in [1, 2]:
          inner_region = sublime.Region(p + 2, self.blocks[p])
          view.replace(edit, inner_region, re.sub('[ \t]*[\r\n]+[ \t]*', ' ', view.substr(inner_region)))
        replace_end = p + 3 if view.substr(sublime.Region(p + 2, p + 4)) == ' |' else p + 2
        view.replace(edit, sublime.Region(p, replace_end), '{')
      else:
        view.replace(edit, sublime.Region(p, p + 3), '}')
