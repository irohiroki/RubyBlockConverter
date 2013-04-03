import tokenize
import io
import re
import sublime, sublime_plugin


class ToggleDoEndToBraceCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    content = self.view.substr(sublime.Region(0, self.view.size()))
    tokenizer = RubyBlockTokenizer(content)
    blocks = []
    for block_coord in tokenizer.find_ruby_block_coords():
      blocks.append( Block.build_from_block_coord(block_coord, self.view) )

    for block in BlockSelector(self.view.sel(), blocks).filtered_sorted_blocks_with_selections():
      BlockEditor(self.view, edit, block).toggle_block()


class RubyBlockType(object):
  (CURLY_BRACES, DO_END) = ("curly_braces", "do_end")


class BlockCoord(object):

  def __init__(self, type, outer_opening, inner_opening, inner_closing, outer_closing):
    self.type = type
    self.outer_opening = outer_opening
    self.inner_opening = inner_opening
    self.inner_closing = inner_closing
    self.outer_closing = outer_closing

  def __repr__(self):
    return "BlockCoord[%s:%s-%s,%s-%s]" % (self.type, self.outer_opening, self.inner_opening, self.inner_closing, self.outer_closing)


class Block(object):
  def __init__(self, type, outer_opening, inner_opening, inner_closing, outer_closing):
    self.type = type
    self.outer_opening = outer_opening
    self.inner_opening = inner_opening
    self.inner_closing = inner_closing
    self.outer_closing = outer_closing
    self.block_vars = ''
    self.indentation = 0
    self.number_of_lines = 0

  @classmethod
  def build_from_block_coord(klass, block_coord, view):
    transform_to_point = lambda coord: view.text_point(coord[0] - 1, coord[1])
    block = klass(
      block_coord.type,
      transform_to_point(block_coord.outer_opening),
      transform_to_point(block_coord.inner_opening),
      transform_to_point(block_coord.inner_closing),
      transform_to_point(block_coord.outer_closing)
      )

    content = view.substr(block.inner_region())
    block_vars = re.search('^ *\|[^\|]+\| *', content)
    if block_vars:
      block.block_vars = block_vars.group(0)

    first_line = view.substr(view.line(block.outer_opening))
    indent = re.search('^ *', first_line)
    if indent:
      block.indentation = len(indent.group(0))

    block.number_of_lines = len(view.lines(block.inner_region()))

    return block

  def size(self):
    return self.inner_closing - self.inner_opening

  def needs_collapsing_on_curly_braces(self):
    return self.number_of_lines <= 3

  def needs_expanding_on_do_end(self):
    return self.number_of_lines == 1

  def is_shorter_than(self, other):
    return self.size() < other.size()

  def does_surround_position(self, position):
    return self.inner_opening <= position and position <= self.inner_closing

  def contains_any_of(self, other_blocks):
    for other_block in other_blocks:
      if self == other_block: continue
      if self.inner_region().contains(other_block.inner_region()):
        return True
    return False

  def inner_region(self):
    return sublime.Region(self.inner_opening, self.inner_closing)

  def __repr__(self):
    return "Block[%s:%s-%s,%s-%s]" % (self.type, self.outer_opening, self.inner_opening, self.inner_closing, self.outer_closing)


class RubyBlockTokenizer(object):

  def __init__(self, content):
    self.content = content

  def tokenize_whole_document(self):
    return tokenize.generate_tokens(io.StringIO(self.content).readline)
 
  def find_block_coords_of_matching_tokens(self, type):
    opening_stack = []
    found_block_coords = []

    criteria = self.criteria_for_block_type(type)

    for type_of_token, value_of_token, begin_coords, end_coords, _ in self.tokenize_whole_document():
      if type_of_token == criteria['required_type_of_token']:
        if value_of_token == criteria['look_for_opening_token']:
          opening_stack.append([begin_coords, end_coords])
        elif value_of_token == criteria['look_for_closing_token']:
          if opening_stack:
            matching_opening = opening_stack.pop()
            found_block_coords.append(BlockCoord(type, matching_opening[0], matching_opening[1], begin_coords, end_coords))
    return found_block_coords

  def find_ruby_block_coords(self):
    return (self.find_block_coords_of_matching_tokens(RubyBlockType.CURLY_BRACES)
          + self.find_block_coords_of_matching_tokens(RubyBlockType.DO_END))

  def criteria_for_block_type(self, type):
    if type == RubyBlockType.CURLY_BRACES:
      return {'required_type_of_token': tokenize.OP, 
              'look_for_opening_token': '{',
              'look_for_closing_token': '}'}
    elif type == RubyBlockType.DO_END:
      return {'required_type_of_token': tokenize.NAME, 
              'look_for_opening_token': 'do',
              'look_for_closing_token': 'end'}

class BlockEditor(object):

  def __init__(self, view, edit, block):
    self.view = view
    self.edit = edit
    self.block = block
    self.line_endings = "\r\n" if (self.view.line_endings() == "Windows") else "\n"

  def toggle_block(self):
    if self.block.type == RubyBlockType.CURLY_BRACES:
      self.toggle_do_end_block_to_curly_braces()
    elif self.block.type == RubyBlockType.DO_END:
      self.toggle_curly_braces_block_to_do_end()

  def toggle_do_end_block_to_curly_braces(self):
    self.view.insert(self.edit, self.block.outer_closing, "end")
    if (self.block.needs_expanding_on_do_end()):
      self.view.insert(self.edit, self.block.outer_closing, "%s%s" % (self.line_endings, ' ' * self.block.indentation))
    self.view.erase(self.edit, sublime.Region(self.block.inner_closing, self.block.outer_closing))
    if (self.block.needs_expanding_on_do_end()):
      self.view.insert(self.edit, self.block.inner_opening + len(self.block.block_vars), "%s%s" % (self.line_endings, ' ' * (self.block.indentation + 2)))
    self.view.replace(self.edit, sublime.Region(self.block.outer_opening, self.block.inner_opening), "do")

  def toggle_curly_braces_block_to_do_end(self):
    self.view.insert(self.edit, self.block.outer_closing, "}")
    self.view.erase(self.edit, sublime.Region(self.block.inner_closing, self.block.outer_closing))
    if self.block.needs_collapsing_on_curly_braces():
      self.erase_line_feeds()
    self.view.replace(self.edit, sublime.Region(self.block.outer_opening, self.block.inner_opening), "{")

  def erase_line_feeds(self):
    for _ in range(2):
      line_feed_coords = self.view.find("%s\s*" % (self.line_endings), self.block.outer_opening)
      if line_feed_coords is not None:
        self.view.erase(self.edit, line_feed_coords)

class BlockSelector(object):

  def __init__(self, selections, blocks):
    self.selections = selections
    self.blocks = blocks

  def filtered_sorted_blocks_with_selections(self):
    filtered = self.filtered_blocks_with_selections()
    return list(reversed(sorted(filtered, key=lambda b: b.outer_opening)))

  def filtered_blocks_with_selections(self):
    blocks = self.blocks_with_selections()
    return filter(lambda b: not b.contains_any_of(blocks), blocks)

  def blocks_with_selections(self):
    result = []
    for selection in self.selections:
      block = self.smallest_block_surrounding_selection(selection)
      if block is not None:
        result.append(block)
    return result

  def smallest_block_surrounding_selection(self, selection):
    candidate = None
    for block in self.all_blocks_surrounding_selection(selection):
      if candidate is None or block.is_shorter_than(candidate):
        candidate = block
    return candidate

  def all_blocks_surrounding_selection(self, selection):
    return filter(lambda b: b.does_surround_position(selection.begin()), self.blocks)


# TODOs:
# better blocks like in BracketHighlighter
# handle spaces around `|x|`