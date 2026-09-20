Ruby Block Converter for Sublime Text 2 and 3
==============================
A command plugin that enables to toggle ruby blocks between braces and `do end`.

How It Works
--------------
Place the cursor in the block and run the command:

```ruby
# original
foo { bar }

# run "brace_to_do_end"
foo do
  bar
end

# run "do_end_to_brace"
foo { bar }
```

do_end_to_brace shrinks a block in a line when the block traverses at most 3 lines.

```ruby
# original
foo {|a|
  a.bar
}

# run "brace_to_do_end"
foo do |a|
  a.bar
end

# but when revert with "do_end_to_brace",
foo {|a| a.bar }
```

When a block has more than 3 lines, do_end_to_brace leaves those lines untouched.

```ruby
# original
foo do
  bar
  baz
end

# run "do_end_to_brace"
foo {
  bar
  baz
}
```

Install
-------
Use [Package Control](http://wbond.net/sublime_packages/package_control) and search for "Ruby Block Converter."

Key Binding
-----------
By default,
`ctrl+shift+[` do_end_to_brace
`ctrl+shift+]` brace_to_do_end

Compatibility
-------------
- Mac: Sublime Text 3 ready!
- Linux: Sublime Text 3 ready!
- Other: Not tested

Testing
-------
The tests live in `tests` and run inside Sublime Text, because the commands
call the sublime API and leave indentation to the built-in `reindent` command.

1. Clone this repository into your `Packages` directory.
2. Install [UnitTesting](https://github.com/SublimeText/UnitTesting) with Package Control.
3. Run "UnitTesting: Test Current Package" from the command palette.

Each pair of `tests/before-*.rb` and `tests/after-*.rb` is one test case. In a
before file, `@` marks a cursor: the markers are stripped before the text goes
into the buffer and their positions become the selection. The command runs once
with every cursor set, and the whole buffer is compared with the after file.

To add a case, append the source to a before file with `@` where the cursor
belongs, and append the expected result to the matching after file.

Future
------
I have a plan to conbine these two commands. That should behave like TextMate.

Contributors
------------
- [@dsandstrom](https://github.com/dsandstrom)

License
-------
All of Ruby Block Converter for Sublime Text is licensed under the MIT license.

Copyright (c) 2013 Hiroki Yoshioka

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
