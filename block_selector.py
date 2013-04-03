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
