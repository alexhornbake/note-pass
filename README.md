
:warning: **Disclaimer:** :warning:
**WORK IN PROGRESS. USE AT YOUR OWN RISK.** *I am not a security or crypto expert. I'm just a software engineer/mechanic in search of a better password manager. This project solves for my needs and use cases. Maybe it will solve yours as well, or inspire another/better novel approach to managing passwords.*

# note-pass
Offline. Paper Password Manager.

**TLDR;** Generate a unique password using something phyiscal and something memorized. Paper "Salt" + Master Password (in your head) + Generation Policy = unique password.

### Why?

Security is all about increasing the cost of attack. The goal of this was to raise that cost to be quite high while still managing passwords in a sane way that is not a total pain in the ass to use.

First, LastPass, OnePassword and their ilk are great systems. Overall they have made users more security, and for most people are likely the "correct solution" at this time. However, this is an exploration of a non-centralized system. I have no doubt that they are cryptographically more secure of a system than "note-pass". That being said, imo, an internet based centralized password system is like a slot machine. As the system collects more and more passwords, the cost of attack remains sufficiently constant while the pay off increases with user growth. All systems are vulerable, and it's not a question of "if" it can be cracked, but a question of cost and potential payoff for an attacker. As these systems grow market share that payoff increases.

Goals/Requirements:
1) Passwords should not be stored digitally. This seemed like a good way to raise the cost of attack to the same level as a armed robbery. IE, you can have my password if you put a gun to my head.
2) Minimal effort to memorize anything
3) No special hardware required
4) Open Source
5) Portable (ie, in theory the process could be used on a smartphone).

note-pass will generate a password from the following pieces of information:
1. A Master Password you keep in your head. This can be shared across all passwords, or unique to services. It's up to you.
2. A Pattern written in a book. Currently an 11x11 grid drawn by hand on dot or graph paper. This should be unique to each service.
3. A Policy. This is a json file that defines the rules of the password. Policies can be written to suite whatever boneheaded rules a service comes up with.

Shoutout to: https://github.com/duffn/dumb-password-rules. This was invaluable when thinking through how to write a policy to describe some of these bad ideas.

The policy is public, the password and pattern are private.

### Usage

`python process_webcam.py <MasterPassword>`

### Master Password

The longer the better. Something memorable is good. [Like This](https://xkcd.com/936/)

### Pattern

![Pattern Image](/test_pattern_5.jpg?raw=true)

Think of it as a hand drawn QR code. Why hand drawn? 

The lines on an a grid can store 2*(n*(n+1)) bits. For example. A 2x2 grid has 12 lines, or 12bits.
The current version uses an 11x11 grid. The corners (where markers are stored for tracking the image) eat up 16 of those bits.
The outer edges are unreliable, so effectively the grid is 9x9 or 180bits. The grid should be expanded to 13x13, giving a true
area of 11x11 grid, 264bits or 33 bytes.

The pattern is essentially a "salt". It is used as such in the password generation process.

**Alternatives storage methods considered**
1) Usb key. Probably a good alternative. Easier to make backups.
2) QR codes. Less fun. Need to be printed/generated on demand, or pregenerated. A pregenerated book of codes would be easier to backup and keep in a safe, but How to bind a nice book? Possible to sell pregreneated books in a secure way? Meh... Generating source of passowrd uniqueness is outside scope of project.
3) Images. How to quantize reliably? How to collect?

Why hand drawn, paper patterns? Fun. Novel. Cameras are ubiquitous. Dot paper is portable, printers are the worst. Difficult to steal/copy. Pattern is dumb (can be decoded by hand if needed) and actually very stable in testing.
 
### Policies
Currently Supported policy rules:
1. Password Length
2. Characters that should be used in constructing the password.
3. Character Types that MUST be in the password.
4. Maximum number of repeated characters. ie. "aaaaa"
5. Maximum number of consecutive characters. ie. "abcd" or "1234"

### How it works.

1. Detection. The pattern is read by your webcam and turned in to bits.
2. Your master password and the resulting bits from reading this pattern are run through pbkdf2 using sha512 100k times.
3. This hash is used as your password seed.
4. Since this seed is going to contain all kinds of funky characters, we consult the policy and grab the usable character set.
5. We then translate the hash (an array of bytes) to an array of acceptable characters.
6. The password is checked against the rules.
7. If the password does not meet the rules, it is changed in a deterministic way. IE. characters are added to the front or incremented in place.
8. The password is checked and mutated recursively until it passes the rules. There is possibly a set of conditions that result in infinite recursion... I'm punting on this. Good problem to have. I can't wait to hit that edge case. My gut tells me that a very constrained policy and an "unlucky" password seed could trigger this... In which case your password is garbage anyway and you should just write it down in your book of pattterns.

### TODOs:

- [ ] More policies, and likely additional rules to interpret.
- [ ] A mobile version for use on iOS and android (kivy?? or port python opencv to C++ opencv common library).

