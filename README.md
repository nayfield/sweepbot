# Sweepbot

Sweepbot is a **very** simple slackbot written in python.

It takes actions on two events:

* A channel message matches a set of keywords
* A channel message is tagged with a specific emoji by a specific list of people

When either event matches, it does a third action:

* Posts that the event happened in a third channel

### Why should I use Sweepbot?

You probably shouldn't.  There are probably other full featured slackbots out there.

### But I really want to!

Ok.  Just understand that this is a single python file designed to do one thing only.

You might be better off with starting anew with the slack API.  Especially since RTM
is deprecated.  

