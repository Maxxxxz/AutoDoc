# AutoDoc

This was originally a class project for CS3560 at Ohio University, but the original repo had a lot of unused code and went untouched for quite a while until I came back to it. The original look of the project was very messy and unorganized, so I decided to remake the GUI using my [Python Window Template](https://github.com/Maxxxxz/PythonWindowTemplate).

# Why use it?

I intend on making this tool incredibly customizable so that you can easily take all of the repetitive work out of documenting your code

# Features

* Multiple File Support
    * Document multiple files in sequence
* Add arbitrary languages
    * Edit regular expressions for already existing languages

# Todo

* Backend
    * Implement all regexes for main supported languages
        * Improve regexes to cover all data types (and custom)
    * ~Multiple file support~
    * ~Strip all useless functions from the backend~
    * ~Create backup files before editing the file~
* Frontend
    * Read json for languages in dropdown
    * Read json for comment formatting rather than use hardcoded strings
    * ~Remove child windows by using lift/place and Page classes~
* CLI
    * Create CLI class functions
    * Determine the best way to request multiline comments from user