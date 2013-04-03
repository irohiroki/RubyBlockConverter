import sublime, sublime_plugin
from block import Block, BlockCoord, RubyBlockType
from block_editor import BlockEditor
from block_selector import BlockSelector
from ruby_block_tokenizer import RubyBlockTokenizer


class ToggleDoEndToBraceCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    content = self.view.substr(sublime.Region(0, self.view.size()))
    tokenizer = RubyBlockTokenizer(content)
    blocks = []
    for block_coord in tokenizer.find_ruby_block_coords():
      blocks.append( Block.build_from_block_coord(block_coord, self.view) )

    for block in BlockSelector(self.view.sel(), blocks).filtered_sorted_blocks_with_selections():
      BlockEditor(self.view, edit, block).toggle_block()
