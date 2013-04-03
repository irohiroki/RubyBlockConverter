import tokenize
import io
from block import BlockCoord, RubyBlockType

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
