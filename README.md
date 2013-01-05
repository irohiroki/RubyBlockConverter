Ruby Block Converter for Sublime Text 2
==============================
A command plugin that enables to convert ruby blocks in brace to `do end`.

How It Works
--------------
Place the cursor in the block and run the command:

```ruby
# from
foo { bar }

# to
foo do
  bar
end
```

with arguments:

```ruby
# from
foo {|a| a.bar }

# to
foo do |a|
  a.bar
end
```

multiline:

```ruby
# from
foo {|a|
  a.bar
}

# to
foo do |a|
  a.bar
end
```

white spaces are naturally rearranged.

Install
-------
Clone this repository in your Sublime Text "Package" directory:

```bash
git clone https://github.com/irohiroki/RubyBlockConverter.git
```

...or wait for support of [Package Control](http://wbond.net/sublime_packages/package_control).

Key Binding
-----------
Bind `brace_to_do_end` to any key conbination of your choice, e.g.

```
{ "keys": ["alt+d"], "command": "brace_to_do_end" }
```

License
-------
All of Ruby Block Converter for Sublime Text 2 is licensed under the MIT license.

Copyright (c) 2013 Hiroki Yoshioka

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
