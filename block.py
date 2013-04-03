import sublime
import re

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

