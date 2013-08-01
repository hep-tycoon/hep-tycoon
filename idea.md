# HEP Tycoon - Idea

A proposal for a project at the [CERN Summer Student Webfest 2013](http://www.citizencyberscience.net/wiki).

## Concept
The project aims to provide a (simulation) game in the style of the "Tycoon" games (e.g. GameDev Tycoon) where the player manages a research facility.

Start with simple tech; build up to more complex stuff.

 * Tech (detectors 'n' stuff)
     * costs **money**
     * produces **publications**
     * has a **lifespan** (after that it needs to either be upgraded or disposed)
     * building tech enables new tech…

The main cycle of the game would be:
 1. build **tech**
 2. publish **findings**
 3. acquire **funding**
 4. `goto 1`

So the actual game could be pretty easy but there is a lot of room for extensions.

## Possible additions
 * employ scientists → publication rate depending on #scientists; max. #scientists depending on tech
 * "hand build" detectors → choose components etc.; detector performance depends on how well they match, their quality, etc.
 * analysis software → choose to have it written either by a company or by some physicists; quality of software influences the publication rate
 * multiplayer
 * actual results → display and explain to the player what he found **importtant**

## What is needed?
 * tech-tree: names, costs, lifespans, publication-rate + educational texts and images
 * It would probably be clever to introduce an in-game currency that has nothing to do with the real world just to protect ourself against producing bs.
 * an actual game "engine"
 * some more buzzwords: bootstrap, local storage, canvas (?), JS, time, server-based (?) → python

## Who is needed?
 * **physicists**: build the tech-tree; make it realistic; provide the texts (& images); beta-testing; also programming
 * **computer scientists**: software design; programming; testing
 * **graphics/web designer**: UI; images

## The goal for the weekend
 * provide a running, playable version of the game that shows the basic idea
 * it should be made in such a way that it can be easily extended in the future (add more depth and functionality)

But the main goal is, of course, to have a lot of **fun** making something new and awesome that hopefully gets people interested in HEP and along the way explains (to some degree…) how research is conducted.

## Caveats
 * from scratch → a lot of work
 * unpredictable outcome (has not been done before)

## Open questions
(Only some of them)

 * How/when does the game end? (For the presentation, one could have it end as soon as the player finds the/a Higgs or a SUSY particle, then write something nice and motivating for the player to pursue a career in HEP and work on the problems in the "real" world.) 
 * How can the player "screw up"?
