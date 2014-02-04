Ruby Block Converter for Sublime Text 2 and 3
==============================
A command plugin that enables to toggle ruby blocks between braces and `do end`.

How It Works
--------------
Place the cursor in the block and run the command:

```ruby
# original
foo { bar }

# run "toggle_between_do_end_and_brace"
foo do
  bar
end

# run "toggle_between_do_end_and_brace"
foo { bar }
```

toggle_between_do_end_and_brace shrinks a block in a line when the block traverses at most 3 lines.

```ruby
# original
foo {|a|
  a.bar
}

# run "toggle_between_do_end_and_brace"
foo do |a|
  a.bar
end

# but when revert with "toggle_between_do_end_and_brace",
foo {|a| a.bar }
```

When a block has more than 3 lines, toggle_between_do_end_and_brace leaves those lines untouched.

```ruby
# original
foo do
  bar
  baz
end

# run "toggle_between_do_end_and_brace"
foo {
  bar
  baz
}
```

Install
-------
Use [Package Control](http://wbond.net/sublime_packages/package_control) and search for "Ruby Block Converter."

Command Palette
---------------
`ctrl+shift+p` and select 'Toggle between Ruby do-end and brace blocks' command. This is an easy way to memorize the key binding.

Key Binding
-----------
By default

 - `ctrl+shift+[` toggle_between_do_end_and_brace
 - `ctrl+shift+]` toggle_between_do_end_and_brace

Compatibility
-------------
- Mac: Sublime Text 3 ready!
- Linux: Sublime Text 3 ready!
- Other: Not tested

Contributors
------------
- [@orbanbotond](https://github.com/orbanbotond)
- [@dsandstrom](https://github.com/dsandstrom)

License
-------
All of Ruby Block Converter for Sublime Text is licensed under the MIT license.

Copyright (c) 2013 Hiroki Yoshioka

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
