# Cloud-Hosted-Recursion-compiler
A compiler from regular python to cloud hosted recursion architecture. Inspired by https://www.youtube.com/watch?v=jCvaV2aG2Sk
This is my first time doing anything even remotely close to this.

Ok so there are a lot of things that i need to say here

# MAIN THINGS YOU NEED TO KNOW:
- Cloud hosted part isn't implemented, as of now the sql is done locally because i was too lazy to learn how to set up postresql. Support for it is planned in a future update.
- If you have any questions, open an issue or something idk i'm not experienced with github
- this thing has a lot of limitations:
    1) any type you want to use has to support str conversion and be able to be evaled
    2) the parser i have rn is very bare bones, so with it come the next few limitations
    3) 2 functions with the same name aren't supported
    4) there can only be 1 function call per line
    5) there are a bunch of variable names that will already be used by the compiler, all of them are from the run file, except for os.getenv("RECURSION") variable, which denotes the recursion level 
    6) variable definitions can only be of a form {variable name} = {something}
    
