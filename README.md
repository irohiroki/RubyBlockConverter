Ruby Block Converter for Sublime Text 2
==============================
A command plugin that enables to convert ruby blocks in brace to `do end` and vice versa.

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

Future
------
I have a plan to conbine these two commands. That should behave like TextMate.

License
-------
All of Ruby Block Converter for Sublime Text 2 is licensed under the MIT license.

Copyright (c) 2013 Hiroki Yoshioka

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
