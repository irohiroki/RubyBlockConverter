import sublime
from block import RubyBlockType

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
