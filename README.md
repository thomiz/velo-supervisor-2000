# velo-supervisor-2000
Program to monitor bicycle service intervals

Join the work, fork the repo and contribue with PRs!

Known limitations:
Rides deleted from Strava are not deleted in velo supervisor upon sync
Data validation happens frontend, so if you use only APIs make your own validation rules
Offset is to be set manually to adjust for distance not registered
Component type must be defined in order to prefill component details to work for component type


Use semver for tagging. For exmaple: git tag -a v0.8 -m "Version 0.8"
Remember to push tags to repo: git push --tags

Changelog - fix layout
0.9.x
Getting data from Strava in the background
Configuration page
Improved component detail page (added bacn button and delete button)
Sorting of component types
Bugfixes

0.8.x
Introduced versioning
Working program, with some bugs

