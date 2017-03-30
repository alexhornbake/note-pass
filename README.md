# note-pass
Offline. Secure Paper Password Manager

WORK IN PROGRESS. USE AT YOUR OWN RISK.

### What and Why?

This is intended to be an alternative to a digital password manager like LastPass or OnePassword.

Security is all about increasing the cost of attack. The goal of this was to raise that cost to be quite high while still managing passwords in a sane way,
that is not a total pain in the ass to use.

This tool will generate a password from the following pieces of information:
1. A Master Password you keep in your head. This can be shared across all passwords, or unique to services. It's up to you.
2. A Pattern written in a book. Currently an 11x11 grid drawn by hand on dot or graph paper. This should be unique to each service.
3. A Policy. This is a json file that defines the rules of the password. Policies can be written to suite whatever boneheaded rules a service comes up with. [Chase is what was used to model the example.json](https://github.com/duffn/dumb-password-rules)

The policy is public, the password and pattern are private.

### Usage

`python process_webcam.py <MasterPassword>`

### Master Password

The longer the better. Something memorable is good. [Like This](https://xkcd.com/936/)

### Pattern

Think of it as a hand drawn QR code. Why hand drawn? Because printers are evil vile devices, and this should be simple and portable.

The lines on an a grid can store 2*(n*(n+1)) bits. For example. A 2x2 grid has 12 lines, or 12bits.
The current version uses an 11x11 grid. The corners (where markers are stored for tracking the image) eat up 16 of those bits.
The outer edges are unreliable, so effectively the grid is 9x9 or 180bits. The grid should be expanded to 13x13, giving a true
area of 11x11 grid, 264bits or 33 bytes.

In password generation, the pattern is essentially a "salt".

### Policies
Currently Supported policy rules:
1. Password Length
2. Characters that should be used in constructing the password.
3. Character Types that MUST be in the password.
4. Maximum number of repeated characters. ie. "aaaaa"
5. Maximum number of consecutive characters. ie. "abcd" or "1234"

### How it works.

1. Detection. The pattern is read by your webcam and turned in to bits.
2. Your master password and the pattern (salt) are run through pbkdf2 using sha512 100k times.
3. This hash is used as your password seed.
4. Since this seed is going to contain all kinds of funky characters, we consult the policy and grab the usable character set.
5. We then translate the hash (an array of bytes) to an array of acceptable characters.
6. The passowrd is checked against the rules.
7. If the password does not meet the rules, it is changed in a deterministic way. IE. characters are added to the front or incremented in place.
8. The password is checked and augmented recursively until it passes the rules.

### TODOs:

- [ ] More policies, and likely additional rules to interpret.
- [ ] A mobile version for use on iOS and android (kivy?? or port python opencv to C++ opencv common library).

